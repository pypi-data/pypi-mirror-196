from abc import ABC
from typing import Any, Dict

import zmq

from akkits.schema.health_status.message import decode as decode_health_status
from akkits.schema.point_cloud.message import decode as decode_point_cloud
from akkits.schema.tracklet_packet.message import decode as decode_tracklet
from akkits.utils.zmq import ConnType, SocketComm, SocketType


class _Receiver(ABC):
    """
    The :py:class:`_Receiver` class is a base class for receivers.

    Every receiver must subclass :py:class:`_Receiver`, and implement :py:meth:`recv`.

    :py:meth:`recv` receives and decodes the flatbuffer message.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, socketcomm: SocketComm) -> None:
        """Creates the receiver.

        Args:
            socketcomm (SocketComm): A `SocketComm` object.
        """
        self._sock = socketcomm
        self.context = self._sock.context
        self.socket = self._sock.socket

    def recv(self) -> Dict[str, Any]:
        """Receives and decodes the flatbuffer message.

        Note that this is a blocking call that waits until a message arrives.

        Returns:
            data (Dict[str, Any]): A data dictionary.
        """
        raise NotImplementedError


class TrackletReceiver(_Receiver):
    """Tracklet packet (output data) receiver.

    Messages are decoded using :py:meth:`decode_tracklet`.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, context: zmq.Context, sock_addr: str) -> None:
        """Creates the receiver.

        Args:
            context (zmq.Context): ZMQ Context.
            sock_addr (str): Socket address.
        """
        super().__init__(SocketComm(context, sock_addr, SocketType.SUB, ConnType.CONNECT))

    def recv(self) -> Dict[str, Any]:
        """Receives and decodes the flatbuffer message.

        Note that this is a blocking call that waits until a message arrives.

        Returns:
            data (Dict[str, Any]): A data dictionary.
        """
        return decode_tracklet(self.socket.recv())


class PointCloudReceiver(_Receiver):
    """Point cloud data receiver.

    Messages are decoded using :py:meth:`decode_point_cloud`.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, context: zmq.Context, sock_addr: str) -> None:
        """Creates the receiver.

        Args:
            context (zmq.Context): ZMQ Context.
            sock_addr (str): Socket address.
        """
        super().__init__(SocketComm(context, sock_addr, SocketType.PULL, ConnType.CONNECT))

    def recv(self) -> Dict[str, Any]:
        """Receives and decodes the flatbuffer message.

        Note that this is a blocking call that waits until a message arrives.

        Returns:
            data (Dict[str, Any]): A data dictionary.
        """
        return decode_point_cloud(self.socket.recv())


class HealthStatusReceiver(_Receiver):
    """Health status receiver.

    Messages are decoded using :py:meth:`decode_health_status`.

    Attributes:
        context (zmq.Context): ZMQ Context.
        socket (zmq.Socket): ZMQ Socket.
    """

    def __init__(self, context: zmq.Context, sock_addr: str) -> None:
        """Creates the receiver.

        Args:
            context (zmq.Context): ZMQ Context.
            sock_addr (str): Socket address.
        """
        super().__init__(SocketComm(context, sock_addr, SocketType.SUB, ConnType.CONNECT))

    def recv(self) -> Dict[str, Any]:
        """Receives and decodes the flatbuffer message.

        Note that this is a blocking call that waits until a message arrives.

        Returns:
            data (Dict[str, Any]): A data dictionary.
        """
        return decode_health_status(self.socket.recv())
