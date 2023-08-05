# Copyright (c) 2016 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" A high-level control interface for scheduling and allocating jobs and
managing hardware in a collection of SpiNNaker machines.
"""
from collections import namedtuple, OrderedDict, defaultdict
from datetime import datetime
from enum import IntEnum
import logging
from logging.handlers import TimedRotatingFileHandler
from threading import RLock
from time import time as timestamp
from functools import partial
from pytz import utc
from spinn_machine import SpiNNakerTriadGeometry
from .coordinates import (
    board_to_chip, chip_to_board, triad_dimensions_to_chips, WrapAround)
from .job_queue import JobQueue
from .async_bmp_controller import AsyncBMPController, AtomicRequests

job_log = logging.Logger("jobs")
job_log.propagate = False
job_log_handler = TimedRotatingFileHandler(
    "spalloc_jobs.log", when="D")
job_log_formatter = logging.Formatter('%(asctime)s: %(message)s')
job_log_handler.setFormatter(job_log_formatter)
job_log.addHandler(job_log_handler)


class Controller(object):
    """ An object which allocates jobs to machines and manages said machines'
    hardware.

    This object is intended to form the core of a server which manages the
    queueing and execution of jobs on several SpiNNaker machines at once using
    a :py:class:`~spalloc_server.job_queue.JobQueue` and interacts with
    the hardware of said machines using
    :py:class:`~spalloc_server.async_bmp_controller.AsyncBMPController`.

    'Jobs' may be created using the :py:meth:`.create_job` and are allocated a
    unique ID. Jobs are then queued, allocated and destroyed according to
    machine availability and user intervention. The state of a job may be
    queried using methods such as :py:meth:`.get_job_state`. When a job changes
    state it is added to the :py:attr:`.changed_jobs` set. If a job's state is
    changed due to a background process (rather than in response to calling a
    :py:class:`.Controller` method), :py:attr:`.on_background_state_change` is
    called.

    :py:class:`~spalloc_server.job_queue.JobQueue` calls callbacks in
    this object when queued jobs are allocated to machines
    (:py:meth:`._job_queue_on_allocate`), allocations are freed
    (:py:meth:`._job_queue_on_free`) or cancelled without being allocated
    (:py:meth:`._job_queue_on_cancel`). These callback functions implement the
    bulk of the functionality of this object by recording state changes in
    jobs and triggering the sending of power/link commands to SpiNNaker
    machines.

    Machines may be added, modified and removed at any time by modifying the
    :py:attr:`.machines` attribute. If a machine is removed or changes
    significantly, jobs running on the machine are cancelled, otherwise
    existing jobs should continue to execute or be scheduled on any new
    machines as appropriate.

    Finally, once the controller is shut down (and outstanding BMP commands are
    flushed) using :py:meth:`.stop` and :py:meth:`.join` methods, it may be
    :py:mod:`pickled <pickle>` and later unpickled to resume operation of the
    controller from where it left off before it was shut down.

    Users should, at a regular interval call :py:meth:`.destroy_timed_out_jobs`
    in order to destroy any queued or running jobs which have not been kept
    alive recently enough.

    Unless otherwise indicated, all methods are thread safe.

    Attributes
    ----------
    max_retired_jobs : int
        Maximum number of retired jobs to retain the state of.
    machines : {name: \
            :py:class:`~spalloc_server.configuration.Machine`, ...} \
            or similar OrderedDict
        Defines the machines now available to the controller.
    changed_jobs : set([job_id, ...])
        The set of job_ids whose state has changed since the last time this set
        was accessed. Reading this value clears it.
    changed_machines : set([machine_name, ...])
        The set of machine names whose state has changed since the last time
        this set was accessed. Reading this value clears it. For example,
        machines are marked as changed if their tags are changed, if they are
        added or removed or if a job is allocated or freed on them.
    on_background_state_change : function() or None
        A function which is called (from any thread) when any state changes
        occur in a background process and not as a direct result of calling a
        method of the controller.

        The callback function *must not* call any methods of the controller
        object.

        Note that this attribute is not pickled and unpicking a controller sets
        this attribute to None.
    """

    def __init__(self, next_id=1, max_retired_jobs=1200,
                 on_background_state_change=None,
                 seconds_before_free=30):
        """
        Parameters
        ----------
        next_id : int, optional
            The next Job ID to assign
        max_retired_jobs : int, optional
            See attribute of same name.
        on_background_state_change : function, optional
            See attribute of same name.
        seconds_before_free : int
            The number of seconds between a board being freed and it becoming
            available again
        """
        # The next job ID to assign
        self._next_id = next_id

        self._on_background_state_change = on_background_state_change

        # The job queue which manages the scheduling and
        # allocation of all jobs.
        self._job_queue = JobQueue(self._job_queue_on_allocate,
                                   self._job_queue_on_free,
                                   self._job_queue_on_cancel,
                                   seconds_before_free)

        # The machines available.
        # {name: Machine, ...}
        self._machines = OrderedDict()

        # The jobs which are currently queued or allocated.
        # {id: _Job, ...}
        self._jobs = OrderedDict()

        # Stores the reasons that jobs have been destroyed, e.g. freed or
        # killed. This may be periodically cleared. Up to
        # _max_retired_jobs jobs are retained (after which their
        # entry in this dict is removed).
        # {id: reason, ...}
        self._max_retired_jobs = max_retired_jobs
        self._retired_jobs = OrderedDict()

        # Underlying sets containing changed jobs and machines
        self._changed_jobs = set()
        self._changed_machines = set()

        # All the attributes set below are "dynamic state" and cannot be
        # pickled. They are initialised by calling to _init_dynamic_state and
        # cleared by calling _del_dynamic_state.

        # The lock which must be held when manipulating any internal state
        self._lock = None

        # The connections to BMPs in the system.
        # {machine_name: {(c, f): AsyncBMPController, ...}, ...}
        self._bmp_controllers = None

        self._init_dynamic_state()

    def __getstate__(self):
        """ Called when pickling this object.

        This object may only be pickled once :py:meth:`.stop` and
        :py:meth:`.join` have returned.
        """
        state = self.__dict__.copy()

        # Do not keep the reference to any state-change callbacks
        state["_on_background_state_change"] = None

        # Do not keep references to unpickleable dynamic state
        state["_bmp_controllers"] = None
        state["_lock"] = None

        return state

    def __setstate__(self, state):
        """ Called when unpickling this object.

        Note that though the object must be pickled when stopped, the unpickled
        object will start running immediately.
        """
        self.__dict__.update(state)

        # Restore callback function pointers in JobQueue (removed by JobQueue
        # when pickling as Python 2.7 cannot reliably pickle method
        # references).
        self._job_queue.on_allocate = self._job_queue_on_allocate
        self._job_queue.on_free = self._job_queue_on_free
        self._job_queue.on_cancel = self._job_queue_on_cancel

        self._init_dynamic_state()

    def stop(self):
        """ Request that all background threads stop.

        This will cause all outstanding BMP commands to be flushed.

        .. warning::

            Apart from :py:meth:`.join`, no methods of this controller object
            may be called once this method has been called.

        See Also
        --------
        join: to wait for the threads to actually terminate.
        """
        # Stop the BMP controllers
        for machine in self._machines:
            for controller in self._bmp_controllers[machine].values():
                controller.stop()

    def join(self):
        """ Block until all background threads have halted and all queued BMP
        commands completed.
        """
        # Wait for the BMP controller threads
        for controllers in self._bmp_controllers.values():
            for controller in controllers.values():
                controller.join()

    @property
    def on_background_state_change(self):
        with self._lock:
            return self._on_background_state_change

    @on_background_state_change.setter
    def on_background_state_change(self, value):
        with self._lock:
            self._on_background_state_change = value

    @property
    def max_retired_jobs(self):
        with self._lock:
            return self._max_retired_jobs

    @max_retired_jobs.setter
    def max_retired_jobs(self, value):
        with self._lock:
            self._max_retired_jobs = value
            while len(self._retired_jobs) > self._max_retired_jobs:
                self._retired_jobs.pop(next(iter(self._retired_jobs)))

    @property
    def machines(self):
        with self._lock:
            return self._machines.copy()

    @machines.setter
    def machines(self, machines):
        """ Update the set of machines available to the controller.

        Attempt to update the information about available machines without
        destroying jobs where possible. Machines are matched with existing
        machines by name and are only recreated if dimensions or connectivity
        information is altered.

        Note that changing the tags, set of dead boards or set of dead links
        does not destroy any already-allocated jobs but will influence new
        ones.

        This function blocks while any removed machine's BMP controllers
        are shut down. This helps prevent collisions e.g. when renaming a
        machine.

        Parameters
        ----------
        machines : {name: \
                :py:class:`~spalloc_server.configuration.Machine`, \
                ...} or similar OrderedDict
            Defines the machines now available to the controller.
        """
        shut_down_controllers = list()
        with self._lock:
            before = set(self._machines)
            after = set(machines)

            # Match old machines with new ones by name
            added = after - before
            removed = before - after
            changed = before.intersection(after)

            # Filter the set of 'changed' machines, ignoring machines which
            # have not changed and marking machines with major changes for
            # re-creation.
            for name in changed.copy():
                old = self._machines[name]
                new = machines[name]
                if old == new:
                    # Machine has not changed, ignore it
                    changed.remove(name)
                elif (old.name != new.name or  # Not really needed
                      old.width != new.width or
                      old.height != new.height or
                      old.board_locations != new.board_locations or
                      old.bmp_ips != new.bmp_ips or
                      old.spinnaker_ips != new.spinnaker_ips):
                    # Machine has changed in a major way, recreate it
                    changed.remove(name)
                    removed.add(name)
                    added.add(name)

            # Make all changes to the job queue atomically to prevent jobs
            # getting scheduled on machines which then immediately change.
            with self._job_queue:
                # Remove all removed machines, accumulating a list of all the
                # AsyncBMPControllers which have been shut down.
                for name in removed:
                    # Remove the machine from the queue causing all jobs
                    # allocated on it to be freed and all boards powered down.
                    self._job_queue.remove_machine(name)

                    # Remove the board and its BMP connections
                    old = self._machines.pop(name)
                    shut_down_controllers.extend(
                        self._bmp_controllers.pop(name).values())

                # Shut-down the now defunct controllers
                for controller in shut_down_controllers:
                    controller.stop()

                def wait_for_old_controllers_to_shutdown():
                    # All new BMPControllers must wait for all the old
                    # controllers to shut-down first
                    for controller in shut_down_controllers:
                        controller.join()

                # Update changed machines
                for name in changed:
                    new = machines[name]
                    self._job_queue.modify_machine(name,
                                                   tags=new.tags,
                                                   dead_boards=new.dead_boards,
                                                   dead_links=new.dead_links)
                    self._machines[name] = new

                # Add new machines
                for name in added:
                    new = machines[name]

                    self._machines[name] = new
                    self._create_machine_bmp_controllers(
                        new, wait_for_old_controllers_to_shutdown)
                    self._job_queue.add_machine(name,
                                                width=new.width,
                                                height=new.height,
                                                tags=new.tags,
                                                dead_boards=new.dead_boards,
                                                dead_links=new.dead_links)

                # Re-order machines to match the specification
                for name in machines:
                    self._machines.move_to_end(name)
                    self._job_queue.move_machine_to_end(name)

            # Mark all effected machines as changed
            self._changed_machines.update(added)
            self._changed_machines.update(changed)
            self._changed_machines.update(removed)

    @property
    def changed_jobs(self):
        with self._lock:
            changed_jobs = self._changed_jobs
            self._changed_jobs = set()
            return changed_jobs

    @property
    def changed_machines(self):
        with self._lock:
            changed_machines = self._changed_machines
            self._changed_machines = set()
            return changed_machines

    def create_job(self, ownerhost, *args, **kwargs):
        """ Create a new job (i.e. allocation of boards).

        This function is a wrapper around
        :py:meth:`JobQueue.create_job()
        <spalloc_server.job_queue.JobQueue.create_job>` which
        automatically selects (and returns) a new job_id. As such, the
        following *additional* (keyword) arguments are accepted:

        Parameters
        ----------
        owner : str
            **Required.** The name of the owner of this job.
        keepalive : float or None
            *Optional.* The maximum number of seconds which may elapse between
            a query on this job before it is automatically destroyed. If None,
            no timeout is used. (Default: 60.0)

        Returns
        -------
        job_id : int
            The Job ID assigned to the job.
        """
        job_log.info("create_job(%s,%s) from %s", args, kwargs, ownerhost)
        # Extract non-allocator arguments
        owner = kwargs.pop("owner")
        keepalive = kwargs.pop("keepalive")

        with self._lock:
            # Generate a job ID
            job_id = self._next_id
            self._next_id += 1

            kwargs["job_id"] = job_id

            # Create job and begin attempting to allocate it
            job = _Job(_id=job_id, owner=owner,
                       keepalive=keepalive,
                       lasthost=ownerhost,
                       args=args, kwargs=kwargs)
            self._jobs[job_id] = job
            self._job_queue.create_job(*args, **kwargs)

            self._changed_jobs.add(job_id)

            return job_id

    def job_keepalive(self, clienthost, job_id):
        """ Reset the keepalive timer for the specified job.

        Note all other job-specific functions implicitly call this method.
        """
        with self._lock:
            job = self._jobs.get(job_id, None)
            if job is not None:
                job.update_keepalive(clienthost)

    def get_job_state(self, clienthost, job_id):
        """ Poll the state of a running job.

        Returns
        -------
        :py:class:`.JobStateTuple`
        """
        with self._lock:
            self.job_keepalive(clienthost, job_id)

            job = self._jobs.get(job_id)
            host = None
            if job is not None:
                # Job is live
                state = job.state
                power = job.power
                keepalive = job.keepalive
                reason = None
                start_time = job.start_time
                host = job.lasthost
                # Note that we update the keepalive after the readout
            elif job_id in self._retired_jobs:
                # Job has been destroyed at some point
                state = JobState.destroyed
                power = None
                keepalive = None
                reason = self._retired_jobs[job_id]
                start_time = None
            else:
                # Job ID not recognised
                state = JobState.unknown
                power = None
                keepalive = None
                reason = None
                start_time = None

        return JobStateTuple(state, power, keepalive, reason, start_time, host)

    def get_job_machine_info(self, clienthost, job_id):
        """ Get information about the machine the job has been allocated.

        Returns
        -------
        :py:class:`.JobMachineInfoTuple`
        """
        with self._lock:
            self.job_keepalive(clienthost, job_id)

            job = self._jobs.get(job_id, None)
            if job is not None and job.boards is not None:
                return JobMachineInfoTuple(
                    job.width, job.height,
                    job.connections,
                    job.allocated_machine.name,
                    job.boards)
        # Job doesn't exist or no boards allocated yet
        return JobMachineInfoTuple(None, None, None, None, None)

    def power_on_job_boards(self, clienthost, job_id):
        """ Power on (or reset if already on) boards associated with a job.
        """
        job_log.info("power_job(%s,On) from %s", job_id, clienthost)
        with self._lock:
            self.job_keepalive(clienthost, job_id)

            job = self._jobs.get(job_id)
            if job is not None and job.boards is not None:
                self._set_job_power_and_links(
                    job, power=True, link_enable=False)

    def power_off_job_boards(self, clienthost, job_id):
        """ Power off boards associated with a job.
        """
        job_log.info("power_job(%s,Off) from %s", job_id, clienthost)
        with self._lock:
            self.job_keepalive(clienthost, job_id)

            job = self._jobs.get(job_id)
            if job is not None and job.boards is not None:
                self._set_job_power_and_links(
                    job, power=False, link_enable=None)

    def destroy_job(self, clienthost, job_id, reason=None):
        """ Destroy a job.

        When the job is finished, or to terminate it early, this function
        releases any resources consumed by the job and removes it from any
        queues.

        Parameters
        ----------
        reason : str or None, optional
            A human-readable string describing the reason for the
            job's destruction.
        """
        if clienthost is None:
            clienthost = "internal"
        if reason is None:
            job_log.info("destroy_job(%s) from %s", job_id, clienthost)
        else:
            job_log.info("destroy_job(%s,%s) from %s",
                         job_id, reason, clienthost)
        with self._lock:
            job = self._jobs.get(job_id, None)
            if job is not None:
                # Free the boards used by the job (the JobQueue will then call
                # _job_queue_on_free which will trigger power-down and removal
                # of the job from self._jobs).
                self._job_queue.destroy_job(job_id, reason)

    def list_jobs(self):
        """ Enumerate all current jobs.

        Returns
        -------
        jobs : [:py:class:`.JobTuple`, ...]
            A list of allocated/queued jobs in order of creation from oldest
            (first) to newest (last).
        """
        with self._lock:
            job_list = []
            for job in self._jobs.values():
                # Strip "job_id" which is only used internally
                kwargs = {k: v for k, v in job.kwargs.items()
                          if k != "job_id"}

                # Machine may not exist
                allocated_machine_name = None
                if job.allocated_machine is not None:
                    allocated_machine_name = job.allocated_machine.name

                job_list.append(JobTuple(
                    job.id, job.owner, job.start_time, job.keepalive,
                    job.state, job.power, job.args, kwargs,
                    allocated_machine_name, job.boards,
                    str(job.lasthost) if job.lasthost is not None else ""))

            return job_list

    def list_machines(self):
        """ Enumerates all machines known to the system.

        Returns
        -------
        machines : [:py:class:`.MachineTuple`, ...]
            The list of machines known to the system in order of priority from
            highest (first) to lowest (last).
        """
        with self._lock:
            return [
                MachineTuple(machine.name, machine.tags,
                             machine.width, machine.height,
                             machine.dead_boards, machine.dead_links)
                for machine in self._machines.values()
            ]

    def get_board_position(self, machine_name, x, y, z):
        """ Get the physical location of a specified board.

        Parameters
        ----------
        machine_name : str
            The name of the machine containing the board.
        x, y, z : int
            The logical board location within the machine.

        Returns
        -------
        (cabinet, frame, board) or None
            The physical location of the board at the specified location or
            None if the machine/board are not recognised.
        """
        with self._lock:
            machine = self._machines.get(machine_name, None)
            if machine is None:
                return None
            return machine.board_locations.get((x, y, z), None)

    def get_board_at_position(self, machine_name, cabinet, frame, board):
        """ Get the logical location of a board at the specified physical
        location.

        Parameters
        ----------
        machine_name : str
            The name of the machine containing the board.
        cabinet, frame, board : int
            The physical board location within the machine.

        Returns
        -------
        (x, y, z) or None
            The logical location of the board at the specified location or None
            if the machine/board are not recognised.
        """
        with self._lock:
            machine = self._machines.get(machine_name, None)
            if machine is None:
                return None
            # NB: Assuming this function is only called very rarely,
            # constructing and maintaining a reverse lookup is not worth
            # the trouble so instead we just search.
            for (x, y, z), (c, f, b) in machine.board_locations.items():
                if (c, f, b) == (cabinet, frame, board):
                    return (x, y, z)
        # No board found
        return None

    def _job_for_location(self, machine, x, y, z):
        """ Determine what job is running on the given board.
        """
        for job_id, job in self._jobs.items():
            # NB: If machine is defined, boards must also be defined.
            if (job.allocated_machine == machine and (x, y, z) in job.boards):
                return job_id, job
        # No job is allocated to the board
        return None, None

    def _where_is_by_logical_triple(self, machine_name, x, y, z):
        """ Helper for :py:meth:`where_is`
        """
        with self._lock:
            # Get the actual Machine
            machine = self._machines.get(machine_name, None)
            if machine is None:
                return None

            chip_x, chip_y = board_to_chip(x, y, z)

            # Compensate chip coordinates for wrap-around
            chip_w, chip_h = triad_dimensions_to_chips(
                machine.width, machine.height, WrapAround.both)
            chip_x %= chip_w
            chip_y %= chip_h

            # Determine the chip within the board
            board_chip = SpiNNakerTriadGeometry.get_spinn5_geometry()\
                .get_local_chip_coordinate(chip_x, chip_y)

            # Determine the logical board coordinates (and compensate for
            # wrap-around)
            x, y, z = chip_to_board(chip_x, chip_y, chip_w, chip_h)

            # Determine the board's physical location (fail if board does not
            # exist)
            cfb = machine.board_locations.get((x, y, z), None)
            if cfb is None:  # pragma: no cover
                return None
            cabinet, frame, board = cfb

            # Determine what job is running on that board
            job_id, job = self._job_for_location(machine, x, y, z)

            return {
                "machine": machine_name,
                "logical": (x, y, z),
                "physical": (cabinet, frame, board),
                "chip": (chip_x, chip_y),
                "board_chip": board_chip,
                "job_id": job_id,
                "job_chip": self._get_job_chip(job, x, y, z, board_chip)
            }

    def _where_is_by_physical_triple(self, machine_name, cabinet, frame,
                                     board):
        """ Helper for :py:meth:`where_is`
        """
        with self._lock:
            # Get the actual Machine
            machine = self._machines.get(machine_name, None)
            if machine is None:
                return None

            xyz = self.get_board_at_position(machine_name, cabinet, frame,
                                             board)
            if xyz is None:
                return None
            chip_x, chip_y = board_to_chip(*xyz)

            # Compensate chip coordinates for wrap-around
            chip_w, chip_h = triad_dimensions_to_chips(
                machine.width, machine.height, WrapAround.both)
            chip_x %= chip_w
            chip_y %= chip_h

            # Determine the chip within the board
            board_chip = SpiNNakerTriadGeometry.get_spinn5_geometry()\
                .get_local_chip_coordinate(chip_x, chip_y)

            # Determine the logical board coordinates (and compensate for
            # wrap-around)
            x, y, z = chip_to_board(chip_x, chip_y, chip_w, chip_h)

            # Determine the board's physical location (fail if board does not
            # exist)
            cfb = machine.board_locations.get((x, y, z), None)
            if cfb is None:  # pragma: no cover
                return None
            cabinet, frame, board = cfb

            # Determine what job is running on that board
            job_id, job = self._job_for_location(machine, x, y, z)

            return {
                "machine": machine_name,
                "logical": (x, y, z),
                "physical": (cabinet, frame, board),
                "chip": (chip_x, chip_y),
                "board_chip": board_chip,
                "job_id": job_id,
                "job_chip": self._get_job_chip(job, x, y, z, board_chip)
            }

    def _where_is_by_chip_coordinate(self, machine_name, chip_x, chip_y):
        """ Helper for :py:meth:`where_is`
        """
        with self._lock:
            # Get the actual Machine
            machine = self._machines.get(machine_name, None)
            if machine is None:
                return None

            # Compensate chip coordinates for wrap-around
            chip_w, chip_h = triad_dimensions_to_chips(
                machine.width, machine.height, WrapAround.both)
            chip_x %= chip_w
            chip_y %= chip_h

            # Determine the chip within the board
            board_chip = SpiNNakerTriadGeometry.get_spinn5_geometry()\
                .get_local_chip_coordinate(chip_x, chip_y)

            # Determine the logical board coordinates (and compensate for
            # wrap-around)
            x, y, z = chip_to_board(chip_x, chip_y, chip_w, chip_h)

            # Determine the board's physical location (fail if board does not
            # exist)
            cfb = machine.board_locations.get((x, y, z), None)
            if cfb is None:
                return None
            cabinet, frame, board = cfb

            # Determine what job is running on that board
            job_id, job = self._job_for_location(machine, x, y, z)

            return {
                "machine": machine_name,
                "logical": (x, y, z),
                "physical": (cabinet, frame, board),
                "chip": (chip_x, chip_y),
                "board_chip": board_chip,
                "job_id": job_id,
                "job_chip": self._get_job_chip(job, x, y, z, board_chip)
            }

    def _where_is_by_job_chip_coordinate(self, job_id, chip_x, chip_y):
        """ Helper for :py:meth:`where_is`
        """
        with self._lock:
            # Covert from job-relative chip location
            job = self._jobs.get(job_id, None)
            if job is None or job.boards is None:
                return None
            machine_name = job.allocated_machine.name
            job_x, job_y, job_z = map(min, zip(*job.boards))
            dx, dy = board_to_chip(job_x, job_y, job_z)
            chip_x += dx
            chip_y += dy

            # Get the actual Machine
            machine = self._machines.get(machine_name, None)
            if machine is None:  # pragma: no cover
                return None

            # Compensate chip coordinates for wrap-around
            chip_w, chip_h = triad_dimensions_to_chips(
                machine.width, machine.height, WrapAround.both)
            chip_x %= chip_w
            chip_y %= chip_h

            # Determine the chip within the board
            board_chip = SpiNNakerTriadGeometry.get_spinn5_geometry()\
                .get_local_chip_coordinate(chip_x, chip_y)

            # Determine the logical board coordinates (and compensate for
            # wrap-around)
            x, y, z = chip_to_board(chip_x, chip_y, chip_w, chip_h)

            # Determine the board's physical location (fail if board does not
            # exist)
            cfb = machine.board_locations.get((x, y, z), None)
            if cfb is None:
                return None
            cabinet, frame, board = cfb

            # Determine what job is running on that board
            found_job_id, job = self._job_for_location(machine, x, y, z)

            # Make sure the board found is actually running that job (this
            # won't be the case, e.g. if a user specifies a board within their
            # machine which is actually dead or allocated to a neighbouring
            # job)
            if found_job_id != job_id:
                return None

            return {
                "machine": machine_name,
                "logical": (x, y, z),
                "physical": (cabinet, frame, board),
                "chip": (chip_x, chip_y),
                "board_chip": board_chip,
                "job_id": job_id,
                "job_chip": self._get_job_chip(job, x, y, z, board_chip)
            }

    def _get_job_chip(self, job, x, y, z, board_chip):
        # pylint: disable=too-many-arguments
        if job is None:
            return None
        board_chip_x, board_chip_y = board_chip

        # Determine the board coordinate within the job
        job_x, job_y, job_z = map(min, zip(*job.boards))
        job_x = x - job_x
        job_y = y - job_y
        job_z = z - job_z

        # Turn that into a chip coordinate and wrap-around according to the
        # boards actually available in the allocated machine
        job_chip_x, job_chip_y = board_to_chip(job_x, job_y, job_z)
        return ((job_chip_x + board_chip_x) % job.width,
                (job_chip_y + board_chip_y) % job.height)

    def where_is(self, **kwargs):
        """ Find out where a SpiNNaker board or chip is located, logically and
        physically.

        May be called in one of the following styles::

            >>> # Query by logical board coordinate within a machine.
            >>> where_is(machine=..., x=..., y=..., z=...)

            >>> # Query by physical board location within a machine.
            >>> where_is(machine=..., cabinet=..., frame=..., board=...)

            >>> # Query by chip coordinate (as if the machine were booted as
            >>> # one large machine).
            >>> where_is(machine=..., chip_x=..., chip_y=...)

            >>> # Query by chip coordinate, within the boards allocated to a
            >>> # job.
            >>> where_is(job_id=..., chip_x=..., chip_y=...)

        Returns
        -------
        {"machine": ..., "logical": ..., "physical": ..., "chip": ..., \
                "board_chip": ..., "job_chip": ..., "job_id": ...} or None
            If a board exists at the supplied location, a dictionary giving the
            location of the board/chip, supplied in a number of alternative
            forms. If the supplied coordinates do not specify a specific chip,
            the chip coordinates given are those of the Ethernet connected chip
            on that board.

            If no board exists at the supplied position, None is returned
            instead.

            ``machine`` gives the name of the machine containing the board.

            ``logical`` the logical board coordinate, (x, y, z) within the
            machine.

            ``physical`` the physical board location, (cabinet, frame, board),
            within the machine.

            ``chip`` the coordinates of the chip, (x, y), if the whole machine
            were booted as a single machine.

            ``board_chip`` the coordinates of the chip, (x, y), within its
            board.

            ``job_id`` is the job ID of the job currently allocated to the
            board identified or None if the board is not allocated to a job.

            ``job_chip`` the coordinates of the chip, (x, y), within its
            job, if a job is allocated to the board or None otherwise.
        """
        # Internally, we normalise the input coordinate into:
        #
        #     machine_name, chip_x, chip_y
        #
        # and then convert this back into all the output formats required.
        # At various points, if we encounter a board/job/chip which doesn't
        # exist we'll drop out.

        keywords = set(kwargs)
        if keywords == set("machine x y z".split()):
            return self._where_is_by_logical_triple(kwargs["machine"],
                                                    kwargs["x"], kwargs["y"],
                                                    kwargs["z"])
        elif keywords == set("machine cabinet frame board".split()):
            return self._where_is_by_physical_triple(kwargs["machine"],
                                                     kwargs["cabinet"],
                                                     kwargs["frame"],
                                                     kwargs["board"])
        elif keywords == set("machine chip_x chip_y".split()):
            return self._where_is_by_chip_coordinate(kwargs["machine"],
                                                     kwargs["chip_x"],
                                                     kwargs["chip_y"])
        elif keywords == set("job_id chip_x chip_y".split()):
            return self._where_is_by_job_chip_coordinate(kwargs["job_id"],
                                                         kwargs["chip_x"],
                                                         kwargs["chip_y"])
        else:
            raise TypeError(
                "Invalid arguments: {}".format(", ".join(keywords)))

    def destroy_timed_out_jobs(self):
        """ Destroy any jobs which have timed out.
        """
        with self._lock:
            now = timestamp()
            # NB: Copy the list of jobs because we will be modifying it
            for job in list(self._jobs.values()):
                if job.keepalive is not None and job.keepalive_until < now:
                    # Job timed out, destroy it
                    self.destroy_job(None, job.id, "Job timed out.")

    def check_free(self):
        """ Check for freed machines that are now available
        """
        with self._lock:
            self._job_queue.check_free()

    def _bmp_on_request_complete(self, job, success, reason=None):
        """ Callback function called by an AsyncBMPController when it completes
        a previously issued request.

        This function sets the specified Job's state to JobState.ready when
        this function has been called job.bmp_requests_until_ready times.

        This function should be passed partially-called with the job the
        callback is associated it.

        Parameters
        ----------
        job : :py:class:`._Job`
            The job whose state should be set. (To be defined by wrapping this
            method in a partial).
        success : bool
            Command success indicator provided by the AsyncBMPController.
        """
        with self._lock:
            # If a BMP command failed, cancel the job
            if not success:
                message = "Machine configuration failed."
                if reason is not None:
                    message += " Error: " + reason
                self.destroy_job(None, job.id, message)

            # Count down the number of outstanding requests before the job is
            # ready
            job.bmp_requests_until_ready -= 1
            assert job.bmp_requests_until_ready >= 0
            if job.bmp_requests_until_ready == 0:
                job.state = JobState.ready
                if job.id in self._retired_jobs:
                    self._job_queue.free(job.id)

                # Report state changes for jobs which are still running
                if job.id in self._jobs:
                    self._changed_jobs.add(job.id)
                    if self._on_background_state_change is not None:
                        self._on_background_state_change()

    def _set_job_power_and_links(self, job, power, link_enable=None):
        """ Power on/off and configure links for the boards associated with a
        specific job.

        Parameters
        ----------
        job : :py:class:`._Job`
            The job whose boards should be controlled.
        power : bool
            The power state to apply to the boards. True = on, False = off.
        link_enable : bool or None, optional
            Whether to enable (True) or disable (False) peripheral links or
            leave them unchanged (None).
        """
        with self._lock:
            machine = job.allocated_machine

            on_done = partial(self._bmp_on_request_complete, job)

            # Group commands by the frame they interact with to allow all
            # commands within a frame to be sent atomically
            frame_commands = defaultdict(partial(AtomicRequests, on_done))

            controllers = self._bmp_controllers[machine.name]

            # Power commands
            for xyz in job.boards:
                c, f, b = machine.board_locations[xyz]
                controller = controllers[(c, f)]
                job_log.info("power(%s, %s) on BMP %s for job %s",
                             b, power, controller.hostname, job.id)
                frame_commands[controller].power(b, bool(power))

            # Link state commands
            if link_enable is not None:
                for x, y, z, link in job.periphery:
                    c, f, b = machine.board_locations[(x, y, z)]
                    controller = controllers[(c, f)]
                    job_log.info(
                        "link(%s, %s, %s) on BMP %s for job %s",
                        b, link, link_enable, controller.hostname, job.id)
                    frame_commands[controller].link(b, link, bool(link_enable))

            # Send power/link commands atomically for each frame
            job.bmp_requests_until_ready += len(frame_commands)
            for controller, commands in frame_commands.items():
                with controller:
                    controller.add_requests(commands)

            # Update job state
            job.state = JobState.power
            job.power = power
            self._changed_jobs.add(job.id)

    def _job_queue_on_allocate(self, job_id, machine_name, boards,
                               periphery, torus):
        """ Called when a job is successfully allocated to a machine.
        """
        # pylint: disable=too-many-arguments
        with self._lock:
            # Update job metadata
            job = self._jobs[job_id]
            job.allocated_machine = self._machines[machine_name]
            job.boards = boards
            job.periphery = periphery
            job.torus = torus
            self._changed_jobs.add(job.id)
            self._changed_machines.add(machine_name)

            # Compute dimensions of machine the job will run on. Note that the
            # formulae used below for converting from board to chip coordinates
            # is only valid when either 'oz' is zero or only a single board is
            # allocated. Since we only allocate multi-board regions by the
            # triad this will be the case.
            ox, oy, oz = min(job.boards)  # Origin
            bx, by, _ = max(job.boards)  # Top-right bound

            # Get system bounds in chips
            if len(job.boards) > 1:
                job.width, job.height = triad_dimensions_to_chips((bx-ox) + 1,
                                                                  (by-oy) + 1,
                                                                  job.torus)
            else:
                # Special case: single board allocations are always 8x8
                job.width = job.height = 8

            # Get SpiNNaker chip Ethernet IPs (enumerated in terms of chip
            # coordinates)
            job.connections = {
                board_to_chip(x-ox, y-oy, z-oz):
                job.allocated_machine.spinnaker_ips[(x, y, z)]
                for (x, y, z) in job.boards
            }

            # Initialise the boards
            self.power_on_job_boards(job.lasthost, job_id)

    def _job_queue_on_free(self, job_id, reason):
        """ Called when a job is freed.
        """
        self._changed_machines.add(self._jobs[job_id].allocated_machine.name)
        self._teardown_job(job_id, reason)

    def _job_queue_on_cancel(self, job_id, reason):
        """ Called when a job is cancelled before having been allocated.
        """
        self._teardown_job(job_id, "Cancelled: {}".format(reason or ""))

    def _teardown_job(self, job_id, reason):
        """ Called once job has been removed from the JobQueue.

        Powers down any hardware in use and finally removes the job from _jobs.
        """
        with self._lock:
            job = self._jobs.pop(job_id)
            self._retired_jobs[job_id] = reason
            self._changed_jobs.add(job.id)

            # Keep the number of retired jobs limited to prevent
            # accumulating memory consumption forever.
            if len(self._retired_jobs) > self._max_retired_jobs:
                self._retired_jobs.pop(next(iter(self._retired_jobs)))

            # Power-down any boards that were in use
            if job.boards is not None:
                self._set_job_power_and_links(job, power=False)
            if job.lasthost is None:
                job_log.info("completed shutdown of job %s", job_id)
            else:
                job_log.info("completed shutdown of job %s (owner-host: %s)",
                             job_id, job.lasthost)

    def _create_machine_bmp_controllers(self, machine, on_thread_start=None):
        """ Create BMP controllers for a machine.
        """
        with self._lock:
            controllers = {}
            self._bmp_controllers[machine.name] = controllers
            for (c, f), hostname in machine.bmp_ips.items():
                controllers[(c, f)] = AsyncBMPController(
                    hostname, on_thread_start)

    def _init_dynamic_state(self):
        """ Initialise all dynamic (non-pickleable) state.

        Specifically:

        * Creates the global controller lock
        * Creates connections to BMPs.
        * Reset keepalive_until on all existing jobs (e.g. allowing remote
          devices a chance to reconnect before terminating their jobs).
        """
        # Recreate the lock
        assert self._lock is None
        self._lock = RLock()

        with self._lock:
            # Create connections to BMPs
            assert self._bmp_controllers is None
            self._bmp_controllers = {}
            try:
                for machine in self._machines.values():
                    self._create_machine_bmp_controllers(machine)

                # Reset keepalives to allow remote clients time to reconnect
                for job_id in self._jobs:
                    self.job_keepalive(None, job_id)
            except Exception:
                self.stop()
                raise

    @property
    def seconds_before_free(self):
        return self._job_queue.seconds_before_free

    @seconds_before_free.setter
    def seconds_before_free(self, seconds_before_free):
        self._job_queue.seconds_before_free = seconds_before_free


class JobState(IntEnum):
    """ All the possible states that a job may be in.
    """

    unknown = 0
    """ The job ID requested was not recognised.
    """

    queued = 1
    """ The job is waiting in a queue for a suitable machine.
    """

    power = 2
    """ The boards allocated to the job are currently being powered on or
    powered off.
    """

    ready = 3
    """ The job has been allocated boards and the boards are not currently
    powering on or powering off.
    """

    destroyed = 4
    """ The job has been destroyed.
    """


class JobStateTuple(namedtuple("JobStateTuple",
                               "state,power,keepalive,reason,start_time,"
                               "keepalivehost")):
    """ Tuple describing the state of a particular job, returned by
    :py:meth:`.Controller.get_job_state`.

    Parameters
    ----------
    state : :py:class:`.JobState`
        The current state of the queried job.
    power : bool or None
        If job is in the ready or power states, indicates whether the boards
        are power{ed,ing} on (True), or power{ed,ing} off (False). In other
        states, this value is None.
    keepalive : float or None
        The Job's keepalive value: the number of seconds between queries
        about the job before it is automatically destroyed. None if no
        timeout is active (or when the job has been destroyed).
    reason : str or None
        If the job has been destroyed, this may be a string describing the
        reason the job was terminated.
    start_time : float or None
        The Unix time (UTC) at which the job was created.
    keepalivehost : str or None
        The IP address of the last system to take an action that caused the
        job to be kept alive.
    """

    # Python 3.4 Workaround: https://bugs.python.org/issue24931
    __slots__ = tuple()


class JobMachineInfoTuple(namedtuple("JobMachineInfoTuple",
                                     "width,height,connections,"
                                     "machine_name,boards")):
    """ Tuple describing the machine alloated to a job, returned by
    :py:meth:`.Controller.get_job_machine_info`.

    Parameters
    ----------
    width, height : int or None
        The dimensions of the machine in *chips* or None if no machine
        allocated.
    connections : {(x, y): hostname, ...} or None
        A dictionary mapping from SpiNNaker Ethernet-connected chip coordinates
        in the machine to hostname or None if no machine allocated.
    machine_name : str or None
        The name of the machine the job is allocated on or None if no machine
        allocated.
    boards : set([(x, y, z), ...]) or None
        The boards allocated to the job.
    """

    # Python 3.4 Workaround: https://bugs.python.org/issue24931
    __slots__ = tuple()


class JobTuple(namedtuple("JobTuple",
                          "job_id,owner,start_time,keepalive,state,power,"
                          "args,kwargs,allocated_machine_name,boards,"
                          "keepalivehost")):
    """ Tuple describing a job in the list of jobs returned by
    :py:meth:`.Controller.list_jobs`.

    Parameters
    ----------
    job_id : int
        The ID of the job.
    owner : str
        The string giving the name of the Job's owner.
    start_time : float
        The time the job was created (Unix time, UTC)
    keepalive : float or None
        The maximum time allowed between queries for this job before it is
        automatically destroyed (or None if the job can remain allocated
        indefinitely).
    machine : str or None
        The name of the machine the job was specified to run on (or None if not
        specified).
    state : :py:class:`.JobState`
        The current state of the job.
    power : bool or None
        If job is in the ready or power states, indicates whether the boards
        are power{ed,ing} on (True), or power{ed,ing} off (False). In other
        states, this value is None.
    args, kwargs
        The arguments to the alloc function which specifies the type/size of
        allocation requested and the restrictions on dead boards, links and
        torus connectivity.
    allocated_machine_name : str or None
        The name of the machine the job has been allocated to run on (or None
        if not allocated yet).
    boards : set([(x, y, z), ...])
        The boards allocated to the job.
    keepalivehost : str
        The name of the host that is reckoned to be keeping this job alive.
        Will be the empty string if no known host is doing so (a possible
        state after a service restart).
    """

    # Python 3.4 Workaround: https://bugs.python.org/issue24931
    __slots__ = tuple()


class MachineTuple(namedtuple("MachineTuple",
                              "name,tags,width,height,"
                              "dead_boards,dead_links")):
    """ Tuple describing a machine in the list of machines returned by
    :py:meth:`.Controller.list_machines`.

    Parameters
    ----------
    name : str
        The name of the machine.
    tags : set(['tag', ...])
        The tags the machine has.
    width, height : int
        The dimensions of the machine in triads.
    dead_boards : set([(x, y, z), ...])
        The coordinates of known-dead boards.
    dead_links : set([(x, y, z, :py:class:`spalloc_server.links.Links`), ...])
        The locations of known-dead links from the perspective of the sender.
        Links to dead boards may or may not be included in this list.
    """

    # Python 3.4 Workaround: https://bugs.python.org/issue24931
    __slots__ = tuple()


class _Job(object):
    """ The metadata, used internally, associated with a non-destroyed job.

    Attributes
    ----------
    id : int
        The ID of the job.
    owner : str
        The job's owner.
    start_time : float
        The time the job was created (Unix time, UTC)
    keepalive : float or None
        The maximum time allowed between queries for this job before it is
        automatically destroyed (or None if the job can remain allocated
        indefinitely).
    keepalive_until : float or None
        The time at which this job will become timed out (or None if no
        timeout required).
    state : :py:class:`.JobState`
        The current state of the job.
    power : bool or None
        If job is in the ready or power states, indicates whether the boards
        are power{ed,ing} on (True), or power{ed,ing} off (False). In other
        states, this value is None.
    args, kwargs
        The arguments to the alloc function which specifies the type/size of
        allocation requested and the restrictions on dead boards, links and
        torus connectivity.
    allocated_machine : \
            :py:class:`spalloc_server.configuration.Machine` or None
        The machine the job has been allocated to run on (or None if not
        allocated yet).
    boards : set([(x, y, z), ...]) or None
        The boards allocated to the job or None if not allocated.
    periphery : set([(x, y, z,\
                     :py:class:`spalloc_server.links.Links`), ...]) or None
        The links around the periphery of the job or None if not allocated.
    torus : :py:class:`spalloc_server.coordinates.WrapAround` or None
        Does the allocated set of boards have wrap-around links? None if
        not allocated.
    width, height : int or None
        The dimensions of the SpiNNaker network in the allocated boards or None
        if not allocated any boards.
    connections : {(x, y): hostname, ...} or None
        If boards are allocated, gives the mapping from chip coordinate to
        Ethernet connection hostname.
    bmp_requests_until_ready : int
        A counter incremented whenever a BMP command is started and
        decremented when the command completes. When this counter reaches
        zero, the user sets the state of the job to
        :py:class:`.JobState.ready`.
    """

    def __init__(self, _id, owner,
                 start_time=None,
                 keepalive=60.0,
                 lasthost=None,
                 state=JobState.queued,
                 power=None,
                 args=tuple(), kwargs=None,
                 allocated_machine=None,
                 boards=None,
                 periphery=None,
                 torus=None,
                 width=None,
                 height=None,
                 connections=None,
                 bmp_requests_until_ready=0):
        # pylint: disable=too-many-arguments
        self.id = _id
        self.owner = owner

        if start_time is not None:  # pragma: no branch
            self.start_time = start_time  # pragma: no cover
        else:
            now = datetime.now(utc)
            epoch = datetime(1970, 1, 1, tzinfo=utc)
            self.start_time = (now - epoch).total_seconds()

        # If None, never kill this job due to inactivity. Otherwise, stop the
        # job if the time exceeds this value. It is the allocator's
        # responsibility to update this periodically.
        self.keepalive = keepalive
        if self.keepalive is not None:
            self.keepalive_until = timestamp() + self.keepalive
        else:
            self.keepalive_until = None
        self.lasthost = lasthost

        # The current life-cycle state of the job
        self.state = state

        # False
        self.power = power

        # Arguments for the allocator
        self.args = args
        self.kwargs = dict({} if kwargs is None else kwargs)

        # The hardware allocated to this job (if any)
        self.allocated_machine = allocated_machine
        self.boards = boards
        self.periphery = periphery
        self.torus = torus
        self.width = width
        self.height = height

        # IP address lookup for allocated boards
        self.connections = connections

        # The number of BMP requests which must complete before this job may
        # return to the ready state.
        self.bmp_requests_until_ready = bmp_requests_until_ready

    def update_keepalive(self, host):
        if host is not None:
            self.lasthost = host
        if self.keepalive is not None:
            self.keepalive_until = timestamp() + self.keepalive
