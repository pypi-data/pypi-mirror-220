# sockets.py

import json
import asyncio
import warnings
import threading
import datetime as dt
from typing import Dict, Any, Optional, Union, Iterable, List, Tuple

from crypto_screening.market.screeners.callbacks import SocketCallback
from crypto_screening.market.screeners.base import BaseMarketScreener, BaseScreener
from crypto_screening.collect.screeners import find_screeners
from crypto_screening.market.screeners.ohlcv import OHLCVScreener

__all__ = [
    "SocketMarketScreener"
]

class SocketMarketScreener(BaseMarketScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - screeners:
        The screener object to control and fill with data.

    - address:
        The host for the socket connection.

    - port:
        The port for the socket connection.
    """

    def __init__(
            self,
            address: str,
            port: int,
            screeners: Optional[Iterable[BaseScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(
            screeners=screeners, location=location,
            cancel=cancel, delay=delay
        )

        self.address = address
        self.port = port

        self.loop: Optional[asyncio.AbstractEventLoop] = None

        self.chunks: Dict[float, List[Dict[str, Any]]] = {}

        self.fail_record: Dict[str, List[Tuple[bytes, Exception]]] = {}
    # end __init__

    async def receive(
            self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """
        Receives the data from the senders.

        :param reader: The data reader.
        :param writer: The data writer.
        """

        payload = await reader.read(SocketCallback.MAX_BUFFER)

        try:
            data = json.loads(
                f'[{payload.decode().replace("}{", "},{")}]'
            )

            for payload in data:
                if (
                    (payload[SocketCallback.PROTOCOL] == SocketCallback.UDP_PROTOCOL) and
                    (payload[SocketCallback.FORMAT] == SocketCallback.CHUNKED_FORMAT)
                ):
                    key = payload[SocketCallback.TIMESTAMP]

                    chunks = self.chunks.setdefault(key, [])

                    chunks.append(payload[SocketCallback.DATA])

                    if len(chunks) == payload[SocketCallback.CHUNKS]:
                        payload = json.loads(''.join(chunks[key]))

                        chunks.pop(key)

                        self.handle(
                            payload[SocketCallback.DATA],
                            name=payload[SocketCallback.KEY]
                        )
                    # end if

                else:
                    self.handle(
                        payload[SocketCallback.DATA],
                        name=payload[SocketCallback.KEY]
                    )
                # end for
            # end for

        except Exception as e:
            self.fail_record.setdefault(
                writer.get_extra_info('peername'), []
            ).append((payload, e))
        # end try
    # end receive

    async def receiving_loop(
            self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """
        Receives the data from the senders.

        :param reader: The data reader.
        :param writer: The data writer.
        """

        while self.screening:
            await self.receive(reader=reader, writer=writer)
        # end while
    # end receiving_loop

    def handle(self, data: Dict[str, Any], name: str) -> None:
        """
        Handles the data received from the connection.

        :param data: The data to handle.
        :param name: The name of the data.
        """

        screeners = find_screeners(
            self.screeners,
            exchange=data[SocketCallback.EXCHANGE],
            symbol=data[SocketCallback.SYMBOL]
        )

        screeners = [
            screener for screener in screeners
            if screener.NAME == name
        ]

        if (
            (SocketCallback.INTERVAL in data) and
            isinstance(data[SocketCallback.INTERVAL], str)
        ):
            screeners = [
                screener for screener in screeners
                if (
                    isinstance(screener, OHLCVScreener) and
                    (screener.interval == data[SocketCallback.INTERVAL])
                )
            ]
        # end if

        for screener in screeners:
            for index, row in data[SocketCallback.DATA]:
                screener.market.loc[dt.datetime.fromtimestamp(index)] = row
            # end for
        # end for
    # end handle

    def screening_loop(
            self,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param loop: The event loop.
        """

        if loop is None:
            loop = asyncio.new_event_loop()
        # end if

        self.loop = loop

        asyncio.set_event_loop(loop)

        async def run() -> None:
            """Runs the program to receive data."""

            server = await asyncio.start_server(
                self.receiving_loop, self.address, self.port
            )

            await server.serve_forever()
        # end run

        self._screening = True

        asyncio.run(run())
    # end screening_loop

    def start_screening(
            self, loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Starts the screening process.

        :param loop: The event loop.
        """

        if self.screening:
            warnings.warn(f"Timeout screening of {self} is already running.")

            return
        # end if

        self._screening_process = threading.Thread(
            target=lambda: self.screening_loop(loop=loop)
        )

        self._screening_process.start()
    # end start_screening
# end SocketMarketScreener