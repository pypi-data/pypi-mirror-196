from abc import ABC

import zmq

from akkits.schema.health_status.message import build as build_health_status
from akkits.schema.point_cloud.message import build as build_point_cloud
from akkits.schema.tracklet_packet.message import build as build_tracklet
from akkits.utils.zmq import ConnType, SocketComm, SocketType


class _Sender(ABC):
    """
    The :py:class:`_Sender` class is a base class for senders.

    Every sender must subclass :py:class:`_Sender`, and implement :py:meth:`send`.

    :py:meth:`send` encodes and sends the flatbuffer message.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, socketcomm: SocketComm) -> None:
        """Creates the sender.

        Args:
            socketcomm (SocketComm): A `SocketComm` object.
        """
        self._sock = socketcomm
        self.context = self._sock.context
        self.socket = self._sock.socket

    def send(self, *args, **kwargs) -> None:
        """Encodes and sends the flatbuffer message."""
        raise NotImplementedError


class TrackletSender(_Sender):
    """Tracklet packet (output data) sender.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, context: zmq.Context, sock_addr: str) -> None:
        """Creates the sender.

        Args:
            context (zmq.Context): ZMQ Context.
            sock_addr (str): Socket address.
        """
        super().__init__(SocketComm(context, sock_addr, SocketType.PUB, ConnType.BIND))

    def send(self, *args, **kwargs) -> None:
        """Encodes and sends the flatbuffer message.

        See :py:meth:`build_tracklet` for the input arguments.
        """
        return self.socket.send(build_tracklet(*args, **kwargs))


class PointCloudSender(_Sender):
    """Point cloud data sender.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, context: zmq.Context, sock_addr: str) -> None:
        """Creates the sender.

        Args:
            context (zmq.Context): ZMQ Context.
            sock_addr (str): Socket address.
        """
        super().__init__(SocketComm(context, sock_addr, SocketType.PUSH, ConnType.BIND))

    def send(self, *args, **kwargs) -> None:
        """Encodes and sends the flatbuffer message.

        See :py:meth:`build_point_cloud` for the input arguments.
        """
        try:
            self.socket.send(build_point_cloud(*args, **kwargs), zmq.NOBLOCK)
        except zmq.Again:
            pass


class HealthStatusSender(_Sender):
    """Health status sender.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, context: zmq.Context, sock_addr: str) -> None:
        """Creates the sender.

        Args:
            context (zmq.Context): ZMQ Context.
            sock_addr (str): Socket address.
        """
        super().__init__(SocketComm(context, sock_addr, SocketType.PUB, ConnType.BIND))

    def send(self, *args, **kwargs) -> None:
        """Encodes and sends the flatbuffer message.

        See :py:meth:`build_health_status` for the input arguments.
        """
        return self.socket.send(build_health_status(*args, **kwargs))
