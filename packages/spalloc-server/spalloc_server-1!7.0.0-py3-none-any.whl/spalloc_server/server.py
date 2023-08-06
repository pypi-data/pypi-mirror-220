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

""" A TCP server which exposes a public interface for allocating boards.

This module is essentially the 'top level' module for the functionality of the\
SpiNNaker Partitioning Server, containing the :py:func:`function <.main>`\
which is mapped to the ``spalloc-server`` command-line tool.
"""

from argparse import ArgumentParser
from collections import OrderedDict
from json import dumps as json, loads as dejson
import logging as log
from os import path
from pickle import dump as pickle, load as unpickle
from threading import Thread
from time import sleep
from spinn_utilities.overrides import overrides
from spalloc_server import __version__, coordinates, configuration
from spalloc_server.configuration import Configuration
from spalloc_server.controller import Controller
from spalloc_server.polling_server_core import PollingServerCore
from spalloc_server.configuration_reloader import ConfigurationReloader

BUFFER_SIZE = 1024

_COMMANDS = {}
""" A dictionary from command names to (unbound) methods of the\
    :py:class:`.Server` class.
"""


def spalloc_command(f):
    """ Decorator which marks a class function of :py:class:`.Server` as a\
        command which may be called by a client.
    """
    _COMMANDS[f.__name__] = f
    return f


class _CriticalStop(Exception):
    pass


class Server(PollingServerCore, ConfigurationReloader):
    """ A TCP server which manages, power, partitioning and scheduling of jobs\
        on SpiNNaker machines.

    Once constructed the server starts a background thread\
    (:py:attr:`._server_thread`, :py:meth:`._run`) which implements the main\
    server logic and handles communication with clients, monitoring of\
    asynchronous board control events (e.g. board power-on completion) and\
    watches for selected signals. All members of this object are assumed to be\
    accessed only from this thread while it is running. The thread is stopped,\
    and its completion awaited by calling\
    :py:meth:`.stop_and_join`, stopping the server.

    The server uses a :py:class:`~spalloc_server.Controller` object to\
    implement scheduling, allocation and machine management functionality.\
    This object is :py:mod:`pickled <pickle>` when the server shuts down in\
    order to preserve the state of all managed machines (e.g. allocated jobs\
    etc.).

    To allow the interruption of the server thread on asynchronous events from\
    the Controller a :py:func:`~socket.socketpair` (:py:attr:`._notify_send`\
    and :py:attr:`._notify_send`) is used which monitored along with client\
    connections and SIGHUP signals (used to trigger config file reloading).

    A number of callable commands are implemented by the server in the form of\
    a subset of the :py:class:`.Server`'s methods indicated by the\
    :py:func:`.spalloc_command` decorator. These may be called by a client by\
    sending a line ``{"command": "...", "args": [...], "kwargs": {...}}``. If\
    the function throws an exception, the client is disconnected. If the\
    function returns, it is packed as a JSON line ``{"return": ...}``, and if\
    the function raises an exception, it is packed as a JSON line\
    ``{"exception": "the message"}``.
    """

    def __init__(self, config_filename, cold_start=False, port=22244):
        """
        :param config_filename: \
            The filename of the config file for the server which describes the\
            machines to be controlled.
        :type config_filename: str
        :param cold_start: \
            If False (the default), the server will attempt to restore its\
            previous state, if True, the server will start from scratch.
        :type cold_start: bool
        :param port: Which port to listen on. Defaults to 22244.
        :type port: int
        """
        # ============ STATE THAT NEEDS TO BE ALWAYS DEFINED ============

        self._cold_start = cold_start
        self._port = port

        # Should the background thread terminate?
        self._stop = False

        # Flag for checking if the server is still alive
        self._running = False

        # Currently open sockets to clients. Once server started, should only
        # be accessed from the server thread.
        self._server_socket = None

        # The server core object that the object that is persisted
        self._controller = None

        # Buffered data received from each socket
        # {fd: buf, ...}
        self._client_buffers = {}

        # ============ SUPERCLASS INITIALISATION ============

        super().__init__()
        ConfigurationReloader.__init__(self, config_filename, self.wake)

        # ============ ACTIVE OBJECTS ============

        # The background thread in which the server will run
        self._server_thread = Thread(target=self._run, name="Server Thread")

        # The current server configuration options. Once server started, should
        # only be accessed from the server thread.
        self._configuration = Configuration()

        # Infer the saved-state location
        self._state_filename = self._get_state_filename(
            self.configuration_file)

        # Attempt to restore saved state if required
        if not self._cold_start and path.isfile(self._state_filename):
            try:
                with open(self._state_filename, "rb") as f:
                    self._controller = unpickle(f)
                log.info("Server warm-starting from %s.",
                         self._state_filename)
            except Exception:  # pylint: disable=broad-except
                # Some other error occurred during unpickling.
                log.exception(
                    "Server state could not be unpacked from %s.",
                    self._state_filename)
                self._controller = None

        # Perform cold-start if no saved state was loaded
        if self._controller is None:
            log.info("Server cold-starting.")
            self._controller = Controller()

        # Notify the background thread when something changes in the background
        # of the controller (e.g. power state changes).
        self._controller.on_background_state_change = self.wake

        # Read configuration file. This must succeed when the server is first
        # being started.
        if not self.read_config_file():
            self._controller.stop()
            raise _CriticalStop("Config file could not be loaded.")

        # Start the server
        self._server_thread.start()
        self._running = True

    def _send_change_notifications(self):
        raise NotImplementedError

    def _clear_watches(self, client):
        raise NotImplementedError

    def _get_state_filename(self, cfg):
        """ How to get the name of the state file from the name of another\
            file (expected to be the config file). Assumes that the config\
            file is in a directory that can be written to.

        :param cfg: The name of the file to use as a base.
        :type cfg: str
        :return: The full filename
        """
        # Factored out for ease of reading.
        dirname = path.dirname(cfg)
        basename = path.basename(cfg)
        filename = ".{}.state.{}".format(basename, __version__)
        return path.join(dirname, filename)

    @overrides(ConfigurationReloader._parse_config)
    def _parse_config(self, config_file_contents):
        g = {}
        g.update(configuration.__dict__)
        g.update(coordinates.__dict__)
        exec(config_file_contents, g)  # pylint: disable=exec-used
        return g

    @overrides(ConfigurationReloader._validate_config)
    def _validate_config(self, parsed_config):
        new = parsed_config.get("configuration", None)
        if new is None or not isinstance(new, Configuration):
            return None
        return new

    @overrides(ConfigurationReloader._load_valid_config)
    def _load_valid_config(self, validated_config):
        old = self._configuration
        self._configuration = validated_config

        # Restart the server if the port or IP has changed (or if the server
        # has not yet been started...)
        if validated_config.ip != old.ip or self._server_socket is None:
            # Close all open connections
            if self._close():  # pragma: no cover
                sleep(0.25)  # Ugly hack; fully release socket now

            # Create a validated_config server socket
            self._server_socket = self._open_server_socket(
                validated_config.ip, self._port)

        # Update the controller
        self._controller.max_retired_jobs = validated_config.max_retired_jobs
        self._controller.seconds_before_free = \
            validated_config.seconds_before_free
        self._controller.machines = OrderedDict(
            (m.name, m) for m in validated_config.machines)
        self.wake()

    def _close(self):
        """ Close all server sockets and disconnect all client connections.

        :return: Whether the server socket itself was closed.
        """
        result = False
        if self._server_socket is not None:
            self.unregister_channel(self._server_socket)
            log.info("closing server socket")
            self._server_socket.close()
            result = True
            self._server_socket = None
        for client_socket in list(self._client_buffers.keys()):
            self._disconnect_client(client_socket)
        return result

    def _disconnect_client(self, client):
        """ Disconnect a client.

        :param client: The client to disconnect
        :type client: :py:class:`socket.Socket`
        """
        try:
            log.info("Client %s disconnected.", client.getpeername())
        except Exception:  # pylint: disable=broad-except
            log.info("Client %s disconnected.", client)

        # Clear input buffer if created
        if client in self._client_buffers:
            del self._client_buffers[client]

        # Clear any watches
        self._clear_watches(client)

        # Stop watching the client's socket for data
        try:
            self.unregister_channel(client)
        except KeyError:
            # The odd case of the unregistered client -
            # this can be ignored as it wasn't registered anyway
            pass

        # Disconnect the client
        client.close()

    def _accept_client(self):
        """ Accept a new client.
        """
        try:
            client, addr = self._server_socket.accept()
        except IOError as e:  # pragma: no cover
            log.warning("problem when accepting connection", exc_info=e)
            return
        log.info("New client connected from %s", addr)

        # Watch the client's socket for data
        self.register_channel(client)

        # Create a buffer for data sent by the client
        self._client_buffers[client] = b""

    def _msg_client(self, client, message):
        """ Low-level way to send a message to a client.

        :param client: The client that we are sending a message to.
        :type client: :py:class:`socket.Socket`
        :param message: The object or array to send. Will be converted to JSON.
        """
        try:
            client.send(json(message).encode("utf-8") + b"\n")
        except Exception:
            self._disconnect_client(client)
            raise

    def _handle_command(self, client, line):
        """ Dispatch a single command.

        :param client: \
            The client that made the request, used to provide a session\
            context where relevant.
        :type client: :py:class:`socket.Socket`
        :param line: \
            The line parsed from the socket. Should be a complete JSON object\
            with at least a 'command' key.
        :type line: str
        :return: Dictionary describing the result of the operation.
        :rtype: dict
        :raises IOError: \
            If something really bad goes wrong with message decoding. The\
            expected response at this point would be simply closing the socket.
        """
        cmd_obj = dejson(line.decode("utf-8"))
        if "command" not in cmd_obj:
            raise IOError("no command name given")
        command_name = cmd_obj["command"]
        if not isinstance(command_name, str):
            raise IOError("parsed gibberish from user")
        if command_name not in _COMMANDS:
            log.info("lookup failure: %s", command_name)
            raise IOError("unrecognised command name")
        command = _COMMANDS[command_name]
        if command is None:  # pragma: no cover
            # Should be unreachable
            log.critical("unexpected lookup failure: %s", command_name)
            raise IOError("unrecognised command name")
        args = cmd_obj["args"] if "args" in cmd_obj else []
        if not isinstance(args, list):
            raise IOError("bad args; must be JSON array")
        kwargs = cmd_obj["kwargs"] if "kwargs" in cmd_obj else {}
        if not isinstance(kwargs, dict):
            raise IOError("bad kwargs: must be JSON dictionary")
        elif "client" in kwargs:
            del kwargs["client"]
        # Execute the specified command
        try:
            return {"return": command(self, client, *args, **kwargs)}
        except Exception as e:  # pylint: disable=broad-except
            return {"exception": str(e)}

    def _handle_commands(self, client):
        """ Handle incoming commands from a client.

        :param client: \
            The client that made the request, used to provide a session\
            context where relevant.
        :type client: :py:class:`socket.Socket`
        """
        try:
            data = client.recv(BUFFER_SIZE)
        except (OSError, IOError):
            data = b""

        # Did the client disconnect?
        if not data:
            self._disconnect_client(client)
            return

        peer = "UNKNOWN"
        line = ""
        try:
            peer = client.getpeername()
            self._client_buffers[client] += data

            # Process any complete commands (whole lines)
            while b"\n" in self._client_buffers[client]:
                line, _, self._client_buffers[client] = \
                    self._client_buffers[client].partition(b"\n")
                # Note that we skip blank lines
                if line:
                    self._msg_client(client,
                                     self._handle_command(client, line))
        except Exception:  # pylint: disable=broad-except
            # If any of the above fails for any reason (e.g. invalid JSON,
            # unrecognised command, command crashes, etc.), just disconnect
            # the client.
            log.exception("Client %s sent bad command %r, disconnecting",
                          peer, line)
            self._disconnect_client(client)

    def _send_notifications(self, label, changes, watches):
        """ How to actually send requested notifications."""
        if changes:
            for client, items in list(watches.items()):
                if items is None or not items.isdisjoint(changes):
                    try:
                        self._msg_client(client, {
                            label: list(changes) if items is None else
                            list(changes.intersection(items))})
                    except (OSError, IOError):
                        log.exception("Could not send notification.")

    def _run(self):
        """ The main server thread.

        This 'infinite' loop runs in a background thread and waits for and\
        processes events such as the :py:meth:`.PollingServerCore.wake` method\
        being called, the config file changing, clients sending commands or\
        new clients connecting. It also periodically calls\
        :py:meth:`.controller.Controller.destroy_timed_out_jobs` on the\
        controller.
        """
        log.info("Server running.")
        while not self._stop:
            # Wait for a connection to get opened/closed, a command to arrive,
            # the config file to change or the timeout to elapse.
            channels = self.ready_channels(
                self._configuration.timeout_check_interval)

            for channel in channels:
                if channel is None:  # pragma: no cover
                    continue
                if channel == self._server_socket:
                    # New client connected
                    self._accept_client()
                else:
                    # Incoming data from client
                    self._handle_commands(channel)

            # Cull any jobs which have timed out
            self._controller.destroy_timed_out_jobs()

            # Check if any new free spaces have appeared
            self._controller.check_free()

            # Send any job/machine change notifications out
            self._send_change_notifications()

            # Config file changed, re-read it
            if self.config_needs_reloading:
                if not self.read_config_file():  # pragma: no cover
                    log.warning("failed to reread configuration file")

    def is_alive(self):
        """ Is the server running?
        """
        return self._running

    def join(self):
        """ Wait for the server to completely shut down.
        """
        self._server_thread.join()
        self._controller.join()

    def stop_and_join(self):
        """ Stop the server and wait for it to shut down completely.
        """
        log.info("Server shutting down, please wait...")

        try:
            # Shut down server thread
            self._stop = True
            self.wake()
            self._server_thread.join()
        finally:
            # Close all connections; this is the critical part as it closes
            # the server socket itself.
            log.info("Closing connections...")
            self._close()

        # Shut down the controller and flush all BMP commands
        log.info("Waiting for all queued BMP commands...")
        self._controller.stop()
        self._controller.join()

        # Dump controller state to file
        with open(self._state_filename, "wb") as f:
            pickle(self._controller, f)

        log.info("Server shut down.")

        self._running = False

    @staticmethod
    def _name(client):
        """ Get the 'name' of the client. This is the string form of the IP\
            address, or None if the concept isn't well defined.

        :return: The client's name (for logging).
        """
        try:
            return None if client is None else str(client.getpeername()[0])
        except Exception:  # pylint: disable=broad-except
            # pragma: no cover
            return None


class SpallocServer(Server):
    def __init__(self, config_filename, cold_start=False, port=22244):
        # For each client, contains a set() of job IDs and machine names that
        # the client is watching for changes or None if all changes are to be
        # monitored.
        # {socket: set or None, ...}
        self._client_job_watches = {}
        self._client_machine_watches = {}

        super().__init__(config_filename, cold_start, port)

    def _send_change_notifications(self):
        """ Send any registered change notifications to clients.

        Sends notifications of the forms ``{"jobs_changed": [job_id, ...]}``\
        and ``{"machines_changed": [machine_name, ...]}`` to clients who have\
        subscribed to be notified of changes to jobs or machines.
        """
        # Notify clients about jobs which have changed
        self._send_notifications("jobs_changed",
                                 self._controller.changed_jobs,
                                 self._client_job_watches)
        # Notify clients about machines which have changed
        self._send_notifications("machines_changed",
                                 self._controller.changed_machines,
                                 self._client_machine_watches)

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _tb):
        if self._running:
            self.stop_and_join()
        return False

    @spalloc_command
    def version(self, _client):
        """
        :rtype: str
        :return: The server's version number.
        """
        return __version__

    @spalloc_command
    def create_job(self, client, *args, **kwargs):
        """ Create a new job (i.e. allocation of boards).

        This function should be called in one of the following styles::

            # Any single (SpiNN-5) board
            job_id = create_job(owner="me")
            job_id = create_job(1, owner="me")

            # Board x=3, y=2, z=1 on the machine named "m"
            job_id = create_job(3, 2, 1, machine="m", owner="me")

            # Any machine with at least 4 boards
            job_id = create_job(4, owner="me")

            # Any 7-or-more board machine with an aspect ratio at least as
            # square as 1:2
            job_id = create_job(7, min_ratio=0.5, owner="me")

            # Any 4x5 triad segment of a machine (may or may-not be a
            # torus/full machine)
            job_id = create_job(4, 5, owner="me")

            # Any torus-connected (full machine) 4x2 machine
            job_id = create_job(4, 2, require_torus=True, owner="me")

        The 'other parameters' enumerated below may be used to further\
        restrict what machines the job may be allocated onto.

        Jobs for which no suitable machines are available are immediately\
        destroyed (and the reason given).

        Once a job has been created, it must be 'kept alive' by a simple\
        watchdog_ mechanism. Jobs may be kept alive by periodically calling\
        the :py:meth:`.job_keepalive` command or by calling any other\
        job-specific command. Jobs are culled if no keep alive message is\
        received for ``keepalive`` seconds. If absolutely necessary, a job's\
        keepalive value may be set to None, disabling the keepalive mechanism.

        .. _watchdog: https://en.wikipedia.org/wiki/Watchdog_timer

        Once a job has been allocated some boards, these boards will be\
        automatically powered on and left unbooted ready for use.

        :param str owner:
            **Required.** The name of the owner of this job.
        :param keepalive:
            The maximum number of seconds which may elapse between a query on
            this job before it is automatically destroyed. If None, no timeout
            is used. (Default: 60.0)
        :type keepalive: float or None
        :param machine:
            Specify the name of a machine which this job must be executed on.
            If None, the first suitable machine available will be used,
            according to the tags selected below. Must be None when tags are
            given. (Default: None)
        :type machine: str or None
        :param tags:
            The set of tags which any machine running this job must have. If
            None is supplied, only machines with the "default" tag will be
            used. If machine is given, this argument must be None.
            (Default: None)
        :type tags: list(str) or None
        :param float min_ratio:
            The aspect ratio (h/w) which the allocated region must be 'at
            least as square as'. Set to 0.0 for any allowable shape, 1.0 to be
            exactly square. Ignored when allocating single boards or specific
            rectangles of triads.
        :param max_dead_boards:
            The maximum number of broken or unreachable boards to allow in the
            allocated region. If None, any number of dead boards is permitted,
            as long as the board on the bottom-left corner is alive (Default:
            None).
        :type max_dead_boards: int or None
        :param max_dead_links:
            The maximum number of broken links allow in the allocated region.
            When require_torus is True this includes wrap-around links,
            otherwise peripheral links are not counted.  If None, any number
            of broken links is allowed. (Default: None).
        :type max_dead_links: int or None
        :param bool require_torus:
            If True, only allocate blocks with torus connectivity. In general
            this will only succeed for requests to allocate an entire machine
            (when the machine is otherwise not in use!). Must be False when
            allocating boards. (Default: False)
        :return: The job ID given to the newly allocated job.
        :rtype: int
        """
        if kwargs.get("tags", None) is not None:
            kwargs["tags"] = set(kwargs["tags"])
        owner = kwargs.get("owner", None)
        if owner is None:
            raise TypeError("owner must be specified for all jobs")
        kwargs["owner"] = str(owner)
        keepalive = kwargs.get("keepalive", 60.0)
        kwargs["keepalive"] = (None if keepalive is None else float(keepalive))
        return self._controller.create_job(self._name(client), *args, **kwargs)

    @spalloc_command
    def job_keepalive(self, client, job_id):
        """ Reset the keepalive timer for the specified job.

        .. note::

            All other job-specific commands implicitly do this.

        :param job_id: A job ID to be kept alive.
        :type job_id: int
        """
        self._controller.job_keepalive(self._name(client), job_id)

    @spalloc_command
    def get_job_state(self, client, job_id):
        """ Poll the state of a running job.

        :param int job_id: A job ID to get the state of.
        :rtype: dict(str, ...)
        :return: A dictionary with the following keys:

            ``state`` : :py:class:`~spalloc_server.controller.JobState`
                The current state of the queried job.
            ``power`` : bool or None
                If job is in the ready or power states, indicates whether the
                boards are power{ed,ing} on (``True``), or power{ed,ing} off
                (``False``). In other states, this value is ``None``.
            ``keepalive`` : float or None
                The Job's keepalive value: the number of seconds between
                queries about the job before it is automatically destroyed.
                ``None`` if no timeout is active (or when the job has been
                destroyed).
            ``reason`` : str or None
                If the job has been destroyed, this may be a string describing
                the reason the job was terminated.
            ``start_time`` : float or None
                For queued and allocated jobs, gives the Unix time (UTC) at
                which the job was created (or None otherwise).
        """
        out = self._controller.get_job_state(
            self._name(client), job_id)._asdict()
        out["state"] = int(out["state"])
        return out

    @spalloc_command
    def get_job_machine_info(self, client, job_id):
        """ Get the list of Ethernet connections to the allocated machine.

        :param int job_id: A job ID to get the machine info for.
        :rtype: dict(str, ...)
        :return: A dictionary with the following keys:

            ``width``, ``height`` : int or None
                The dimensions of the machine in chips, e.g. for booting.
                ``None`` if no boards are allocated to the job.
            ``connections`` : [[[x, y], hostname], ...] or None
                A list giving Ethernet-connected chip coordinates in the
                machine to hostname.
                ``None`` if no boards are allocated to the job.
            ``machine_name`` : str or None
                The name of the machine the job is allocated on.
                ``None`` if no boards are allocated to the job.
            ``boards`` : [[x, y, z], ...] or None
                All the boards allocated to the job or ``None`` if no boards
                allocated.
        """
        width, height, connections, machine_name, boards = \
            self._controller.get_job_machine_info(self._name(client), job_id)

        if connections is not None:
            connections = list(connections.items())
        if boards is not None:
            boards = list(boards)

        return {"width": width, "height": height,
                "connections": connections,
                "machine_name": machine_name,
                "boards": boards}

    @spalloc_command
    def power_on_job_boards(self, client, job_id):
        """ Power on (or reset if already on) boards associated with a job.

        Once called, the job will enter the 'power' state until the power
        state change is complete, this may take some time.

        :param int job_id: A job ID to turn boards on for.
        """
        self._controller.power_on_job_boards(self._name(client), job_id)

    @spalloc_command
    def power_off_job_boards(self, client, job_id):
        """ Power off boards associated with a job.

        Once called, the job will enter the 'power' state until the power
        state change is complete, this may take some time.

        :param int job_id: A job ID to turn boards off for.
        """
        self._controller.power_off_job_boards(self._name(client), job_id)

    @spalloc_command
    def destroy_job(self, client, job_id, reason=None):
        """ Destroy a job.

        Call when the job is finished, or to terminate it early, this function
        releases any resources consumed by the job and removes it from any
        queues.

        :param int job_id: A job ID to destroy.
        :param str reason:
            An optional human-readable description of the reason for the job's
            destruction.
        """
        self._controller.destroy_job(self._name(client), job_id, reason)

    def _register_for_notifications(self, client, watchset, _id):
        """ Helper method that handles the protocol for registration for\
            notifications.
        """
        if _id is None:
            watchset[client] = None
        elif client not in watchset:
            watchset[client] = set([_id])
        elif watchset[client] is not None:
            watchset[client].add(_id)
        else:
            # Client is already notified about all changes, do nothing!
            pass

    def _unregister_for_notifications(self, client, watchset, _id):
        """ Helper method that handles the protocol for unregistration for\
            notifications.
        """
        if client not in watchset:
            return
        if _id is None:
            del watchset[client]
            return
        watches = watchset[client]
        if watches is not None:
            watches.discard(_id)
            if not watches:
                del watchset[client]

    def _clear_watches(self, client):
        self._client_job_watches.pop(client, None)
        self._client_machine_watches.pop(client, None)

    @spalloc_command
    def notify_job(self, client, job_id=None):
        """ Register to be notified about changes to a specific job ID.

        Once registered, a client will be asynchronously be sent notifications
        form ``{"jobs_changed": [job_id, ...]}\\n`` enumerating job IDs which
        have changed. Notifications are sent when a job changes state, for
        example when created, queued, powering on/off, powered on and
        destroyed. The specific nature of the change is not reflected in the
        notification.

        :param job_id:
            A job ID to be notified of or None if all job state changes should
            be reported. Defaults to None (i.e., all jobs).
        :type job_id: int or None

        See Also
        --------
        no_notify_job : Stop being notified about a job.
        notify_machine : Register to be notified about changes to machines.
        """
        self._register_for_notifications(
            client, self._client_job_watches, job_id)

    @spalloc_command
    def no_notify_job(self, client, job_id=None):
        """ Stop being notified about a specific job ID.

        Once this command returns, no further notifications for the specified
        ID will be received.

        :param job_id:
            A job ID to no longer be notified of or None to not be notified of
            any jobs. Note that if all job IDs were registered for
            notification, this command only has an effect if the specified
            job_id is None. Defaults to None (i.e., all jobs).
        :type job_id: int or None

        See Also
        --------
        notify_job : Register to be notified about changes to a specific job.
        """
        self._unregister_for_notifications(
            client, self._client_job_watches, job_id)

    @spalloc_command
    def notify_machine(self, client, machine_name=None):
        """ Register to be notified about a specific machine name.

        Once registered, a client will be asynchronously be sent notifications
        of the form ``{"machines_changed": [machine_name, ...]}\\n``
        enumerating machine names which have changed. Notifications are sent
        when a machine changes state, for example when created, change,
        removed, allocated a job or an allocated job is destroyed.

        :param machine_name:
            A machine name to be notified of or None if all machine state
            changes should be reported. Defaults to None (i.e., all machines).
        :type machine_name: str or None

        See Also
        --------
        no_notify_machine : Stop being notified about a machine.
        notify_job : Register to be notified about changes to jobs.
        """
        self._register_for_notifications(
            client, self._client_machine_watches, machine_name)

    @spalloc_command
    def no_notify_machine(self, client, machine_name=None):
        """ Unregister to be notified about a specific machine name.

        Once this command returns, no further notifications for the specified
        ID will be received.

        :param machine_name:
            A machine name to no longer be notified of or None to not be
            notified of any machines. Note that if all machines were
            registered for notification, this command only has an effect if
            the specified machine_name is None. Defaults to None (i.e., all
            machines).
        :type machine_name: str or None

        See Also
        --------
        notify_machine : Register to be notified about changes to a machine.
        """
        self._unregister_for_notifications(
            client, self._client_machine_watches, machine_name)

    @spalloc_command
    def list_jobs(self, _client):
        """ Enumerate all non-destroyed jobs.

        :rtype: list(dict(str, ...))
        :return:
            A list of allocated/queued jobs in order of creation from oldest
            (first) to newest (last). Each job is described by a dictionary
            with the following keys:

            ``job_id``
                the ID of the job.

            ``owner``
                the string giving the name of the Job's owner.

            ``start_time``
                the time the job was created (Unix time, UTC).

            ``keepalive``
                the maximum time allowed between queries for this job before
                it is automatically destroyed (or ``None`` if the job can
                remain allocated indefinitely).

            ``state``
                the current
                :py:class:`~spalloc_server.controller.JobState` of the job.

            ``power``
                indicates whether the boards are powered on or not. If job
                is in the ready or power states, indicates whether the boards
                are power{ed,ing} on (``True``), or power{ed,ing} off
                (``False``). In other states, this value is ``None``.

            ``args`` and ``kwargs``
                the arguments to the alloc function which specifies the
                type/size of allocation requested and the restrictions on
                dead boards, links and torus connectivity.

            ``allocated_machine_name``
                the name of the machine the job has been allocated to run on
                (or ``None`` if not allocated yet).

            ``boards``
                a list [(x, y, z), ...] of boards allocated to the job.

            ``keepalivehost``
                the IP address of the host reckoned to be keeping this job
                alive (i.e., the host that did a request most recently that
                updated the internal keep-alive timeout).
        """
        out = []
        for job in self._controller.list_jobs():
            job = job._asdict()
            job["state"] = int(job["state"])
            if job["boards"] is not None:
                job["boards"] = list(job["boards"])
            if job["kwargs"].get("tags", None) is not None:
                job["kwargs"]["tags"] = list(job["kwargs"]["tags"])
            out.append(job)
        return out

    @spalloc_command
    def list_machines(self, _client):
        """ Enumerates all machines known to the system.

        :rtype: list(dict(str, ...))
        :return:
            The list of machines known to the system in order of priority from
            highest (first) to lowest (last). Each machine is described by a
            dictionary with the following keys:

            ``name``
                the name of the machine.

            ``tags``
                the list ['tag', ...] of tags the machine has.

            ``width`` and ``height``
                the dimensions of the machine in triads.

            ``dead_boards``
                a list([(x, y, z), ...]) giving the coordinates
                of known-dead boards.

            ``dead_links``
                a list([(x, y, z, link), ...]) giving the locations of
                known-dead links from the perspective of the sender.
                Links to dead boards may or may not be included in this list.
        """
        out = []
        for machine in self._controller.list_machines():
            machine = machine._asdict()
            machine["tags"] = list(machine["tags"])
            machine["dead_boards"] = list(machine["dead_boards"])
            machine["dead_links"] = [(x, y, z, int(link))
                                     for x, y, z, link
                                     in machine["dead_links"]]
            out.append(machine)
        return out

    @spalloc_command
    def get_board_position(self, _client, machine_name, x, y, z):
        """ Get the physical location of a specified board.

        :param str machine_name: The name of the machine containing the board.
        :param int x: Logical address within machine: first coordinate.
        :param int y: Logical address within machine: second coordinate.
        :param int z: Logical address within machine: third coordinate.
        :return:
            The physical location of the board (cabinet, frame, board) at the
            specified location or None if the machine/board are not recognised.
        :rtype: list(int) or None
        """
        return self._controller.get_board_position(machine_name, x, y, z)

    @spalloc_command
    def get_board_at_position(self, _client, machine_name, x, y, z):
        """ Get the logical location of a board at the specified physical\
            location.

        :param str machine_name: The name of the machine containing the board.
        :param int x: Physical address within machine: cabinet ID.
        :param int y: Physical address within machine: frame ID.
        :param int z: Physical address within machine: board ID.
        :return:
            The logical location of the board (a triple) at the specified
            location or None if the machine/board are not recognised.
        :rtype: list(int) or None
        """
        return self._controller.get_board_at_position(machine_name, x, y, z)

    @spalloc_command
    def where_is(self, _client, **kwargs):
        """ Find out where a SpiNNaker board or chip is located, logically and\
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

        Only these patterns of use are supported; all keyword arguments\
        listed above are mandatory when used for a particular query.

        :rtype: dict(str, ...) or None
        :return:
            If a board exists at the supplied location, a dictionary giving
            the location of the board/chip, supplied in a number of
            alternative forms. If the supplied coordinates do not specify a
            specific chip, the chip coordinates given are those of the
            Ethernet connected chip on that board.

            If no board exists at the supplied position, ``None`` is returned
            instead.

            The dictionary will have the following keys:

            ``machine``
                the name of the machine containing the board.

            ``logical``
                the logical board coordinate, (x, y, z) within the machine.

            ``physical``
                the physical board location, (cabinet, frame, board),
                within the machine.

            ``chip``
                the coordinates of the chip, (x, y), if the whole machine
                were booted as a single machine.

            ``board_chip``
                the coordinates of the chip, (x, y), within its board.

            ``job_id``
                the job ID of the job currently allocated to the board
                identified or ``None`` if the board is not allocated to a job.

            ``job_chip``
                the coordinates of the chip, (x, y), within its job,
                if a job is allocated to the board, or ``None`` otherwise.
        """
        return self._controller.where_is(**kwargs)


def main(args=None):
    """ Command-line launcher for the server.

    The server may be cleanly terminated using a keyboard interrupt (e.g.,\
    :kbd:`Ctrl+c`), and may be told to reload its configuration via `SIGHUP`.

    :param args: The command-line arguments passed to the program.
    """
    parser = ArgumentParser(
        description="Start a SpiNNaker machine partitioning server.")
    parser.add_argument("--version", "-V", action="version",
                        version="%(prog)s {}".format(__version__))
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="hide non-error output")
    parser.add_argument("config", type=str,
                        help="configuration filename to use for the server.")
    parser.add_argument("--cold-start", action="store_true",
                        default=False,
                        help="force a cold start, erasing any existing "
                             "saved state")
    parser.add_argument("--port", "-p", type=int, default=22244,
                        help="port to run the service on")
    args = parser.parse_args(args)

    if not args.quiet:
        log.basicConfig(
            level=log.INFO,
            format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")

    try:
        server = SpallocServer(config_filename=args.config,
                               cold_start=args.cold_start, port=args.port)
        # NB: Originally this loop was replaced with a call to server.join
        # however in Python 2, such blocking calls are not interruptible so we
        # use this rather ugly workaround instead.
        while server.is_alive():  # pragma: no cover
            try:
                sleep(0.1)
            except IOError:
                pass
    except _CriticalStop as e:
        # NB: No stack trace from a critical stop! The code that threw should
        # have logged the issue if a trace was relevant.
        log.error(str(e))
        return 1
    except KeyboardInterrupt:
        server.stop_and_join()
    except Exception:  # pylint: disable=broad-except
        log.exception("unexpected failure")
        return 2

    return 0


if __name__ == "__main__":  # pragma: no cover
    import sys
    sys.exit(main())
