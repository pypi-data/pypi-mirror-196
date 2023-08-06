from enum import IntEnum, unique

import zmq
from zmq import ssh


@unique
class SocketType(IntEnum):
    """Socket type enumeration to be used with :py:class:`SocketComm`."""

    PUSH = 0
    PULL = 1
    PAIR = 2
    PUB = 3
    SUB = 4


@unique
class ConnType(IntEnum):
    """Connection type enumeration to be used with :py:class:`SocketComm`."""

    BIND = 0
    CONNECT = 1


class SocketComm:
    def __init__(
        self,
        context: zmq.Context,
        addr: str,
        socket_type: int,
        connect_type: int,
        high_water_mark: int = 1,
        ssh_server: str = "",
        name: str = "",
    ) -> None:
        """Creates a `SocketComm` object that wraps a ZMQ Socket.

        Args:
            context (zmq.Context): ZMQ Context.
            addr (str): The socket address (including port).
            socket_type (int): Socket type :py:class:`SocketType`.
            connect_type (int): Connection type :py:class:`ConnType`.
            high_water_mark (int, optional): High water mark. Defaults to 1.
                If it is 1 and the socket type is PUB/SUB, then CONFLATE will be set to True.
            ssh_server (str, optional): SSH server address for tunnelling. Defaults to "".
            name (str, optional): A name for this object. Defaults to "".
        """

        self.addr = addr
        self.socket_type = socket_type
        self.connect_type = connect_type
        self.context = context
        self.ssh_server = ssh_server
        self.name = name
        self.high_water_mark = high_water_mark
        self.socket = self._get_socket()
        self._connect()

    def _get_socket(self) -> zmq.Socket:
        """Creates and returns a ZMQ Socket.

        Raises:
            ValueError: If `socket_type` is not one of:
              - `SocketType.PUSH`
              - `SocketType.PULL`
              - `SocketType.PAIR`
              - `SocketType.PUB`
              - `SocketType.SUB`

        Returns:
            socket (zmq.Socket): A ZMQ Socket.
        """
        if self.socket_type == SocketType.PUSH:
            socket = self.context.socket(zmq.PUSH)
            socket.setsockopt(zmq.SNDHWM, self.high_water_mark)

        elif self.socket_type == SocketType.PULL:
            socket = self.context.socket(zmq.PULL)
            socket.setsockopt(zmq.RCVHWM, self.high_water_mark)

        elif self.socket_type == SocketType.PAIR:
            socket = self.context.socket(zmq.PAIR)

        elif self.socket_type == SocketType.PUB:
            socket = self.context.socket(zmq.PUB)
            if self.high_water_mark == 1:
                socket.setsockopt(zmq.CONFLATE, 1)

        elif self.socket_type == SocketType.SUB:
            socket = self.context.socket(zmq.SUB)
            socket.setsockopt(zmq.SUBSCRIBE, b"")
            if self.high_water_mark == 1:
                socket.setsockopt(zmq.CONFLATE, 1)

        else:
            raise ValueError(f"Invalid `socket_type`: {self.socket_type}")
        return socket

    def _connect(self) -> None:
        """Setup the connection.

        https://pyzmq.readthedocs.io/en/latest/howto/ssh.html
        https://stackoverflow.com/a/22474105

        Raises:
            ValueError: If `connect_type` is not one of:
              - `ConnType.BIND`
              - `ConnType.CONNECT`
        """
        if self.ssh_server:
            ssh.tunnel_connection(self.socket, self.addr, self.ssh_server)
            return
        if self.connect_type == ConnType.BIND:
            self.socket.bind(self.addr)
        elif self.connect_type == ConnType.CONNECT:
            self.socket.connect(self.addr)
        else:
            raise ValueError(f"Invalid `connect_type`: {self.connect_type}")

    def __enter__(self):
        return self.socket

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Pending messages shall be discarded immediately when the socket is closed
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close(1)
