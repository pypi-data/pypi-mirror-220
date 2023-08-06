# recorder.py

import warnings
import threading
import time
from abc import ABCMeta, abstractmethod
import datetime as dt
from typing import (
    Optional, Dict, Any, List,
    Iterable, Type, Union
)
from functools import partial
import asyncio

from represent import Modifiers, represent

from cryptofeed import FeedHandler
from cryptofeed.feed import Feed

from crypto_screening.process import find_string_value
from crypto_screening.exchanges import EXCHANGES, EXCHANGE_NAMES
from crypto_screening.symbols import adjust_symbol
from crypto_screening.market.screeners.base import (
    BaseMarketScreener, BaseScreener, BaseScreenersContainer
)
from crypto_screening.market.screeners.callbacks import Callback

__all__ = [
    "MarketHandler",
    "ExchangeFeed",
    "FEED_GROUP_SIZE",
    "add_feeds",
    "MarketScreener",
    "MarketRecorder"
]

class MarketHandler(FeedHandler):
    """A class to handle the market data feed."""

    def __init__(self) -> None:
        """Defines the class attributes."""

        super().__init__(
            config={'uvloop': False, 'log': {'disabled': True}}
        )
    # end __init__
# end MarketHandler

class ExchangeFeed(Feed):
    """A class to represent an exchange feed object."""

    handler: Optional[MarketHandler] = None

    running: bool = False

    def stop(self) -> None:
        """Stops the process."""

        self.running = False

        Feed.stop(self)
    # end stop

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        Create tasks for exchange interfaces and backends.

        :param loop: The event loop for the process.
        """

        self.running = True

        Feed.start(self, loop=loop)
    # end start
# end ExchangeFeed


FEED_GROUP_SIZE = 20

def add_feeds(
        handler: MarketHandler,
        data: Dict[str, Iterable[str]],
        fixed: Optional[bool] = False,
        amount: Optional[int] = FEED_GROUP_SIZE,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> None:
    """
    Adds the symbols to the handler for each exchange.

    :param handler: The handler object.
    :param data: The data of the exchanges and symbols to add.
    :param parameters: The parameters for the exchanges.
    :param fixed: The value for fixed parameters to all exchanges.
    :param amount: The maximum amount of symbols for each feed.
    """

    base_parameters = None

    if not fixed:
        parameters = parameters or {}

    else:
        base_parameters = parameters or {}
        parameters = {}
    # end if

    for exchange, symbols in data.items():
        exchange = find_string_value(value=exchange, values=EXCHANGE_NAMES)

        symbols = [adjust_symbol(symbol, separator='-') for symbol in symbols]

        if fixed:
            parameters.setdefault(exchange, base_parameters)
        # end if

        EXCHANGES[exchange]: Type[ExchangeFeed]

        groups = []

        for i in range(0, int(len(symbols) / amount) + len(symbols) % amount, amount):
            groups.append(symbols[i:])
        # end for

        for symbols_packet in groups:
            exchange_parameters = (
                parameters[exchange]
                if (
                    (exchange in parameters) and
                    isinstance(parameters[exchange], dict) and
                    all(isinstance(key, str) for key in parameters)
                ) else {}
            )

            feed = EXCHANGES[exchange](symbols=symbols_packet, **exchange_parameters)

            feed.start = partial(ExchangeFeed.start, feed)
            feed.stop = partial(ExchangeFeed.stop, feed)
            feed.handler = handler
            feed.running = False

            handler.add_feed(feed)
        # end for
    # end for
# end add_feeds

@represent
class MarketRecorder(BaseScreenersContainer, metaclass=ABCMeta):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.market.screeners.recorder import MarketRecorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = MarketRecorder(data=market)

    """

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            callbacks: Optional[Iterable[Callback]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param screeners: The screeners to record.
        :param callbacks: The callbacks for the service.
        """

        super().__init__(screeners=screeners)

        self.callbacks = callbacks or []

        self._disabled = False
    # end __init__

    @property
    def disabled(self) -> bool:
        """Returns the value for the recorder to run."""

        return self._disabled
    # end disabled

    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """
    # end parameters

    def disable(self) -> None:
        """Stops the recorder."""

        self._disabled = True
    # end disable

    def enable(self) -> None:
        """Starts the recorder."""

        self._disabled = False
    # end disable

    async def process(self, data: Any, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """
    # end process

    async def record(self, data: Any, timestamp: float):
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        if not self.disabled:
            await self.process(data=data, timestamp=timestamp)
        # end if
    # end record
# end MarketRecorder

class MarketScreener(BaseMarketScreener):
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

    - handler:
        The handler object to handle the data feed.

    - recorder:
        The recorder object to record the data of the market from the feed.

    - screeners:
        The screener object to control and fill with data.

    - refresh:
        The duration of time between each refresh. 0 means no refresh.

    - amount:
        The amount of symbols for each symbols group for an exchange.

    - limited:
        The value to limit the running screeners to active exchanges.
    """

    __modifiers__ = Modifiers()
    __modifiers__.excluded.append('handler')

    screeners: List[BaseScreener]
    recorder: MarketRecorder

    DELAY = 1
    AMOUNT = FEED_GROUP_SIZE

    REFRESH = dt.timedelta(minutes=10)

    def __init__(
            self,
            recorder: MarketRecorder,
            screeners: Optional[Iterable[BaseScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[MarketHandler] = None,
            amount: Optional[int] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        """

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, screeners=screeners
        )

        if refresh is True:
            refresh = self.REFRESH
        # end if

        self.recorder = recorder
        self.handler = handler or MarketHandler()
        self.limited = limited or False
        self.amount = amount or self.AMOUNT
        self.refresh = refresh

        self.loop: Optional[asyncio.AbstractEventLoop] = None

        self._feeds_parameters: Optional[Dict[str, Any]] = None
        self._run_parameters: Optional[Dict[str, Any]] = None
    # end __init__

    def update_screeners(self) -> None:
        """Updates the records of the object."""

        super().update_screeners()

        self.recorder.update_screeners()
    # end update_screeners

    def add_feeds(
            self,
            data: Optional[Dict[str, Iterable[str]]] = None,
            fixed: Optional[bool] = True,
            amount: Optional[int] = None,
            parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
    ) -> None:
        """
        Adds the symbols to the handler for each exchange.

        :param data: The data of the exchanges and symbols to add.
        :param parameters: The parameters for the exchanges.
        :param fixed: The value for fixed parameters to all exchanges.
        :param amount: The maximum amount of symbols for each feed.
        """

        if data is None:
            data = self.structure()
        # end if

        self._feeds_parameters = dict(
            data=data, fixed=fixed, parameters=parameters, amount=amount
        )

        feed_params = self.recorder.parameters()
        feed_params.update(parameters or {})

        add_feeds(
            self.handler, data=data, fixed=fixed,
            parameters=feed_params, amount=amount or self.amount
        )
    # end add_feeds

    def refresh_feeds(self) -> None:
        """Refreshes the feed objects."""

        if self._feeds_parameters is None:
            warnings.warn(
                "Cannot refresh feeds as there was "
                "no feeds initialization to repeat."
            )

            return
        # end if

        self.handler.feeds.clear()

        self.add_feeds(**self._feeds_parameters)
    # end refresh

    def rerun(self) -> None:
        """Refreshes the process."""

        if self._run_parameters is None:
            warnings.warn(
                "Cannot rerun as there was "
                "no initial process to repeat."
            )

            return
        # end if

        self.terminate()
        self.refresh_feeds()
        self.run(**self._run_parameters)
    # end rerun

    def screening_loop(
            self,
            start: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if loop is None:
            loop = asyncio.new_event_loop()
        # end if

        self.loop = loop

        asyncio.set_event_loop(loop)

        self._screening = True

        for screener in self.screeners:
            screener._screening = True
        # end for

        if self._feeds_parameters is None:
            self.add_feeds()
        # end if

        self.handler.run(
            start_loop=start and (not loop.is_running()),
            install_signal_handlers=False
        )
    # end screening_loop

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        for screener in self.screeners:
            screener._saving_process = threading.Thread(
                target=screener.saving_loop
            )
            screener._saving_process.start()
        # end for
    # end saving_loop

    def update_loop(self) -> None:
        """Updates the state of the screeners."""

        self._updating = True

        refresh = self.refresh

        if isinstance(refresh, dt.timedelta):
            refresh = refresh.total_seconds()
        # end if

        start = time.time()

        while self.updating:
            s = time.time()

            if self.screening:
                self.update()

                current = time.time()

                if refresh and ((current - start) >= refresh):
                    self.rerun()

                    start = current
                # end if
            # end if

            time.sleep(max([self.delay - (time.time() - s), 0]))
        # end while
    # end update_loop

    def update(self) -> None:
        """Updates the state of the screeners."""

        for screener in self.screeners:
            for feed in self.handler.feeds:
                feed: ExchangeFeed

                if (
                    self.limited and
                    (screener.exchange.lower() == feed.id.lower()) and
                    (not feed.running)
                ):
                    screener.stop()
                # end if
            # end for
        # end for
    # end update

    def stop_screening(self) -> None:
        """Stops the screening process."""

        super().stop_screening()

        self.loop: asyncio.AbstractEventLoop

        async def stop() -> None:
            """Stops the handler."""

            self.handler.stop(self.loop)
            self.handler.close(self.loop)
        # end stop

        self.loop.create_task(stop())

        for task in asyncio.all_tasks(self.loop):
            task.cancel()
        # end for

        self.loop = None

        self.handler.running = False
    # end stop_screening

    def start_screening(
            self,
            start: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Starts the screening process.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if self.screening:
            warnings.warn(f"Timeout screening of {self} is already running.")

            return
        # end if

        self._screening_process = threading.Thread(
            target=lambda: self.screening_loop(loop=loop, start=start)
        )

        self._screening_process.start()
    # end start_screening

    def run(
            self,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            update: Optional[bool] = True,
            screen: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            wait: Optional[Union[bool, float, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
    ) -> None:
        """
        Runs the program.

        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        :param update: The value to update the screeners.
        :param screen: The value to start the loop.
        :param loop: The event loop.

        :return: The start_timeout process.
        """

        self._run_parameters = dict(
            save=save, block=block, update=update, screen=screen,
            loop=loop, wait=wait, timeout=timeout,
        )

        if not block:
            self.start_screening(loop=loop, start=screen)
        # end if

        super().run(
            screen=False, block=False, wait=wait,
            timeout=timeout, update=update, save=save
        )

        if block:
            self.screening_loop(loop=loop, start=screen)
        # end if
    # end run
# end MarketScreener