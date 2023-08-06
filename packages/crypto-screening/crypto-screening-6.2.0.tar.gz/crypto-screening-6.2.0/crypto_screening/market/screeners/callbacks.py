# callbacks.py

import warnings
import json
from typing import Optional, Any, Union
import asyncio
from textwrap import wrap

from cryptofeed.backends.socket import UDPProtocol

__all__ = [
    "Callback",
    "SocketCallback"
]

class Callback:
    """A class to represent a callback."""

    DATA_KEY: str = None
    CONNECTABLE: bool = False
    ADJUSTABLE: bool = True

    def __init__(self, key: Optional[Any] = None) -> None:
        """
        Defines the class attributes.

        :param key: The key od the data.
        """

        self.key = key if key else self.DATA_KEY
    # end __init__

    def record(self, data: Any, timestamp: float, key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """
    # end record

    @property
    def connectable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.CONNECTABLE
    # end connectable

    @property
    def adjustable(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.ADJUSTABLE
    # end adjustable

    async def connect(self) -> None:
        """Connects to the socket service."""
    # end connect
# end Callback

Connection = Union[asyncio.StreamWriter, asyncio.DatagramTransport]

class SocketCallback(Callback):
    """A class to represent a socket callback."""

    BUFFER = 1024
    MAX_BUFFER = BUFFER * 64
    MIN_BUFFER = 128

    TCP_PROTOCOL = 'tcp'
    UDP_PROTOCOL = 'udp'
    UDS_PROTOCOL = 'uds'

    PROTOCOLS = (TCP_PROTOCOL, UDP_PROTOCOL, UDS_PROTOCOL)

    REGULAR_FORMAT = 'regular'
    CHUNKED_FORMAT = 'chunked'

    FORMATS = (REGULAR_FORMAT, CHUNKED_FORMAT)

    FORMAT = 'format'
    DATA = 'data'
    TIMESTAMP = 'timestamp'
    NAME = 'name'
    KEY = 'key'
    PROTOCOL = 'protocol'
    CHUNKS = 'chunks'
    PART = 'part'

    CONNECTABLE = True

    def __init__(
            self,
            address: str,
            port: int,
            protocol: Optional[str] = None,
            key: Optional[Any] = None,
            buffer: Optional[int] = None
    ) -> None:
        """
        Defines the class attributes.

        :param address: The address of the socket.
        :param protocol: The server protocol.
        :param port: The port of the socket.
        :param key: The key od the data.
        :param buffer: The buffer size.
        """

        super().__init__(key=key)

        buffer = buffer or self.BUFFER
        protocol = protocol or self.TCP_PROTOCOL

        self.protocol = self.validate_protocol(protocol)
        self.address = address
        self.port = port
        self.buffer = buffer

        self.running = False
        self.connection: Optional[Connection] = None
        self._protocol: Optional[asyncio.DatagramProtocol] = None
    # end __init__

    @property
    def connected(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self.connection is not None
    # end connected

    def validate_protocol(self, protocol: str) -> str:
        """
        Validates the protocol.

        :param protocol: The protocol to validate.
        """

        if protocol not in self.PROTOCOLS:
            raise ValueError(
                f"Invalid protocol: {protocol}. "
                f"Protocol must be one of: {', '.join(self.PROTOCOLS)}"
            )
        # end if

        if protocol == self.UDS_PROTOCOL:
            try:
                dir(asyncio.open_unix_connection)

            except AttributeError:
                raise ValueError(f"Cannot use protocol: {protocol}.")
            # end try
        # end if

        return protocol
    # end validate_protocol

    # noinspection PyTypeChecker
    async def connect(self) -> None:
        """Connects to the socket service."""

        if self.connection is not None:
            warnings.warn(f"{repr(self)} callback is already connected.")

            return
        # end if

        self.validate_protocol(self.protocol)

        try:
            if self.protocol == self.UDP_PROTOCOL:
                loop = asyncio.get_event_loop()

                self.connection, self._protocol = (
                    await loop.create_datagram_endpoint(
                        lambda: UDPProtocol(loop),
                        remote_addr=(self.address, self.port)
                    )
                )

            elif self.protocol == self.TCP_PROTOCOL:
                _, self.connection = await asyncio.open_connection(
                    host=self.address, port=self.port
                )

            elif self.protocol == self.UDS_PROTOCOL:
                _, self.connection = await asyncio.open_unix_connection(
                    path=self.address
                )
            # end if

            self.running = True

        except Exception as e:
            if self.adjustable:
                warnings.warn(f"{type(e)}: {str(e)}")

            else:
                raise e
            # end if
        # end try
    # end connect

    def record(self, data: Any, timestamp: float, key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        if not (self.running and self.connected):
            return False
        # end if

        timestamp = float(timestamp)

        data = json.dumps(
            {
                self.PROTOCOL: self.protocol,
                self.KEY: self.key or key,
                self.TIMESTAMP: timestamp,
                self.DATA: data,
                self.FORMAT: self.REGULAR_FORMAT
            }
        )

        if self.protocol == self.UDP_PROTOCOL:
            if len(data) > self.buffer:
                size = max((self.MIN_BUFFER, self.buffer - self.MIN_BUFFER))

                chunks = wrap(data, size)

                for i, chunk in enumerate(chunks, start=1):
                    message = json.dumps(
                        {
                            self.PROTOCOL: self.protocol,
                            self.KEY: self.key or key,
                            self.CHUNKS: len(chunks),
                            self.TIMESTAMP: timestamp,
                            self.FORMAT: self.CHUNKED_FORMAT,
                            self.DATA: chunk,
                            self.PART: i
                        }
                    )

                    self.connection.sendto(message.encode())
                # end for

            else:
                self.connection.sendto(data.encode())
            # end if

        else:
            # noinspection PyUnresolvedReferences
            writer = (
                self.connection.write
                if hasattr(self.connection, 'write') else
                self.connection.swrite
            )

            # noinspection PyArgumentList
            writer(data.encode())
        # end if

        return True
    # end writer
# end SocketCallback