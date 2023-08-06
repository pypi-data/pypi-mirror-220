# callbacks.py

import warnings
import json
import datetime as dt
from typing import Optional, Any, Union, Dict, Callable, List, Tuple
import asyncio
from textwrap import wrap

from cryptofeed.backends.socket import UDPProtocol

from sqlalchemy import Engine, text, inspect
from sqlalchemy.orm import sessionmaker

from crypto_screening.dataset import DATE_TIME
from crypto_screening.market.screeners.database import (
    create_engine, parts_to_database_table_name
)

__all__ = [
    "Callback",
    "SocketCallback",
    "DatabaseCallback",
    "callback_data"
]

CallbackData = List[Tuple[float, Dict[str, Optional[Union[str, bool, float]]]]]

def callback_data(
        data: CallbackData,
        exchange: str,
        symbol: str,
        interval: Optional[str] = None
) -> Dict[str, Union[str, CallbackData]]:
    """
    Wraps the data for the callback.

    :param data: The data to wrap.
    :param exchange: The source exchange of the data.
    :param symbol: The symbol of the data.
    :param interval: The interval of the data.

    :return: The wrapped data.
    """

    return {
        Callback.DATA: data,
        Callback.EXCHANGE: exchange,
        Callback.SYMBOL: symbol,
        Callback.INTERVAL: interval
    }
# end callback_data

class Callback:
    """A class to represent a callback."""

    DATA_KEY: str = None
    CONNECTABLE: bool = False
    ADJUSTABLE: bool = True

    DATA = 'data'
    EXCHANGE = 'exchange'
    SYMBOL = 'symbol'
    INTERVAL = 'interval'

    def __init__(self, key: Optional[Any] = None) -> None:
        """
        Defines the class attributes.

        :param key: The key od the data.
        """

        self.key = key if key else self.DATA_KEY

        self._connected = False
    # end __init__

    @property
    def connected(self) -> bool:
        """
        Checks if the connection was created.

        :return: The existence of a connection.
        """

        return self._connected
    # end connected

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

    async def start(self) -> None:
        """Connects to the socket service."""
    # end start

    async def connect(self) -> None:
        """Connects to the socket service."""

        if self.connected:
            warnings.warn(f"{repr(self)} callback is already connected.")

            return
        # end if

        try:
            await self.start()

            self._connected = True

        except Exception as e:
            if self.adjustable:
                warnings.warn(f"{type(e)}: {str(e)}")

            else:
                raise e
            # end if
        # end try
    # end connect

    async def process(self, data: Any, timestamp: float, key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """
    # end process

    async def record(self, data: Any, timestamp: float, key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        if self.connectable and (not self.connected):
            await self.connect()
        # end if

        if self.connectable and not self.connected:
            return False
        # end if

        try:
            return await self.process(data=data, timestamp=timestamp, key=key)

        except Exception as e:
            if self.adjustable:
                warnings.warn(f"{type(e)}: {str(e)}")

            else:
                raise e
            # end if
        # end try

        return False
    # end record
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

        self.connection: Optional[Connection] = None
        self._protocol: Optional[asyncio.DatagramProtocol] = None
        self._writer: Optional[Callable[[bytes], None]] = None
    # end __init__

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
    async def start(self) -> None:
        """Connects to the socket service."""

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

        self._writer = (
            self.connection.write
            if hasattr(self.connection, 'write') else
            self.connection.swrite
        )
    # end start

    async def process(
            self,
            data: Dict[str, Any],
            timestamp: float,
            key: Optional[Any] = None
    ) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        timestamp = float(timestamp)

        data = json.dumps(
            {
                self.PROTOCOL: self.protocol,
                self.KEY: key or self.key,
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
            self._writer(data.encode())
        # end if

        return True
    # end process
# end SocketCallback

class DatabaseCallback(Callback):
    """A class to represent a callback."""

    CONNECTABLE: bool = True

    DATATYPES = {
        str: "TEXT",
        bool: "BOOL",
        int: "INTEGER",
        float: "FLOAT",
        dt.datetime: "DATETIME"
    }

    def __init__(
            self,
            database: str,
            engine: Optional[Engine] = None,
            key: Optional[Any] = None
    ) -> None:
        """
        Defines the class attributes.

        :param database: The path to the database.
        :param engine: The engine for the database.
        :param key: The key od the data.
        """

        super().__init__(key=key)

        self.database = database

        self.engine = engine

        if isinstance(self.engine, Engine):
            self._connected = True
        # end if

        self._session: Optional = None

        self.tables: Dict[Tuple[str, str, str, Optional[str]], str] = {}
        self.table_names: Optional[List[str]] = None
    # end __init__

    async def process(
            self,
            data: Dict[str, Any],
            timestamp: float,
            key: Optional[Any] = None) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        :param key: The key for the data type.

        :return: The validation value.
        """

        if self._session is None:
            self._session = sessionmaker(bind=self.engine)()
        # end if

        if self.table_names is None:
            self.table_names = inspect(self.engine).get_table_names()
        # end if

        for index, row in data[self.DATA]:
            key, exchange, symbol, interval = (
                key or self.key, data[self.EXCHANGE],
                data[self.SYMBOL], data.get(self.INTERVAL, None)
            )

            if (key, exchange, symbol, interval) not in self.tables:
                table = parts_to_database_table_name(
                    name=key, exchange=exchange,
                    symbol=symbol, interval=interval
                )

                self.tables[(key, exchange, symbol, interval)] = table

                if table not in self.table_names:
                    creation = ', '.join(
                        f"{column} {self.DATATYPES[type(value)]}"
                        for column, value in row.items()
                    )

                    self._session.execute(
                        text(
                            "CREATE TABLE " + table +
                            f" ({DATE_TIME} TEXT, {creation}, "
                            f"PRIMARY KEY ({DATE_TIME}));"
                        )
                    )
                # end if

            else:
                table = self.tables.setdefault(
                    (key, exchange, symbol, interval),
                    parts_to_database_table_name(
                        name=key, exchange=exchange,
                        symbol=symbol, interval=interval
                    )
                )
            # end if

            index = dt.datetime.fromtimestamp(index)

            attributes = (repr(str(value)) for value in row.values())

            self._session.execute(
                text(
                    "INSERT INTO " + table +
                    f" VALUES ('{index}', {', '.join(attributes)});"
                )
            )

            self._session.commit()
        # end for

        if data[self.DATA]:
            return True

        else:
            return False
        # end if
    # end process

    async def start(self) -> None:
        """Connects to the socket service."""

        self.engine = self.engine or create_engine(self.database)
    # end start
# end DatabaseCallback