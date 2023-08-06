# ohlcv.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any,
    Union, List, Callable, Tuple
)

import pandas as pd

from cryptofeed.types import OrderBook
from cryptofeed.defines import L2_BOOK

from crypto_screening.interval import interval_to_total_time
from crypto_screening.dataset import (
    OHLCV_COLUMNS, bid_ask_to_ohlcv,
    load_dataset, save_dataset, create_dataset
)
from crypto_screening.validate import validate_interval
from crypto_screening.symbols import adjust_symbol
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.callbacks import Callback, callback_data
from crypto_screening.market.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler
)
from crypto_screening.market.screeners.orderbook import (
    OrderbookScreener, record_orderbook, create_orderbook_screeners
)

__all__ = [
    "OHLCVMarketScreener",
    "OHLCVMarketRecorder",
    "OHLCVScreener",
    "ohlcv_market_screener",
    "create_ohlcv_market_dataset",
    "create_ohlcv_screeners"
]

Indexes = Dict[str, Dict[str, Dict[str, int]]]

def create_ohlcv_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(
        columns=OHLCVMarketRecorder.COLUMNS
    )
# end create_ohlcv_market_dataset

class OHLCVScreener(BaseScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The key of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - interval:
        The interval for the data structure of OHLCV.

    - market:
        The dataset of the market data as OHLCV.

    - base_market:
        The dataset of the market data as BID/ASK spread.
    """

    INTERVAL = "1m"
    NAME = "OHLCV"

    COLUMNS = OHLCV_COLUMNS

    def __init__(
            self,
            symbol: str,
            exchange: str,
            interval: Optional[str] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
            orderbook_market: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param interval: The interval for the data.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param market: The data for the market.
        :param orderbook_market: The base market dataset.
        """

        super().__init__(
            symbol=symbol, exchange=exchange, location=location,
            cancel=cancel, delay=delay, market=market
        )

        self.interval = self.validate_interval(interval or self.INTERVAL)

        self.orderbook_market = orderbook_market
    # end __init__

    @staticmethod
    def validate_interval(interval: str) -> str:
        """
        Validates the symbol value.

        :param interval: The interval for the data.

        :return: The validates symbol.
        """

        return validate_interval(interval=interval)
    # end validate_symbol

    @property
    def ohlcv_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end ohlcv_market

    def orderbook_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return (
            self.dataset_path(location=location).
            replace(self.NAME, OrderbookScreener.NAME)
        )
    # end orderbook_dataset_path

    def save_orderbook_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.orderbook_market) > 0:
            save_dataset(
                dataset=self.orderbook_market,
                path=self.orderbook_dataset_path(location=location)
            )
        # end if
    # end save_orderbook_dataset

    def ohlcv_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return self.dataset_path(location=location)
    # end ohlcv_dataset_path

    def save_ohlcv_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.ohlcv_market) > 0:
            save_dataset(
                dataset=self.ohlcv_market,
                path=self.ohlcv_dataset_path(location=location)
            )
        # end if
    # end save_ohlcv_dataset

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.save_ohlcv_dataset(location=location)
        self.save_orderbook_dataset(location=location)
    # end save_datasets

    def load_ohlcv_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.ohlcv_dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.ohlcv_market.loc[index] = data
        # end for
    # end load_ohlcv_dataset

    def load_orderbook_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.orderbook_dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.orderbook_market.loc[index] = data
        # end for
    # end load_orderbook_dataset

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.load_ohlcv_dataset(location=location)
        self.load_orderbook_dataset(location=location)
    # end load_datasets

    def orderbook_screener(self) -> OrderbookScreener:
        """
        Creates the orderbook screener object.

        :return: The orderbook screener.
        """

        return OrderbookScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay, market=self.orderbook_market
        )
    # end orderbook_screener
# end OHLCVScreener

async def record_ohlcv(
        screeners: Iterable[Union[OrderbookScreener, OHLCVScreener]],
        indexes: Indexes,
        data: OrderBook,
        timestamp: float,
        callbacks: Optional[Iterable[Callback]] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param screeners: The screeners.
    :param indexes: The indexes of the OHLCV market.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    orderbook_screeners: List[OrderbookScreener] = [
        screener for screener in screeners
        if isinstance(screener, OrderbookScreener)
    ]

    if not orderbook_screeners:
        return False
    # end if

    if not await record_orderbook(
        screeners=orderbook_screeners, callbacks=callbacks,
        data=data, timestamp=timestamp
    ):
        return False
    # end if

    exchange = data.exchange.lower()
    symbol = adjust_symbol(symbol=data.symbol)

    ohlcv_screeners: Dict[str, List[OHLCVScreener]] = {}
    ohlcv_datasets: Dict[str, pd.DataFrame] = {}

    for screener in screeners:
        if isinstance(screener, OHLCVScreener):
            (
                ohlcv_screeners.
                setdefault(screener.interval, []).
                append(screener)
            )
        # end if
    # end for

    if not ohlcv_screeners:
        return False
    # end if

    spread = orderbook_screeners[0].market

    for interval, screeners in ohlcv_screeners.items():
        dataset_index = (
            indexes.
            setdefault(exchange, {}).
            setdefault(symbol, {}).
            setdefault(interval, 0)
        )

        span: dt.timedelta = spread.index[-1] - spread.index[dataset_index]

        interval_total_time = interval_to_total_time(interval)

        if (span >= interval_total_time) or (dataset_index == 0):
            ohlcv = bid_ask_to_ohlcv(
                dataset=spread.iloc[dataset_index:], interval=interval
            )

            ohlcv_datasets[interval] = ohlcv
        # end for
    # end for

    for interval, ohlcv in ohlcv_datasets.items():
        data: Dict[dt.datetime, Tuple[float, Dict[str, Any]]] = {}

        for screener in ohlcv_screeners[interval]:
            for index, row in ohlcv.iterrows():
                index: dt.datetime

                if index not in screener.ohlcv_market.index:
                    screener.ohlcv_market.loc[index] = row
                # end if

                data.setdefault(index, (index.timestamp(), row.to_dict()))
            # end for
        # end for

        indexes[exchange][symbol][interval] = len(spread)

        for callback in callbacks or []:
            payload = callback_data(
                data=list(data.values()), exchange=exchange,
                symbol=symbol, interval=interval
            )

            await callback.record(payload, timestamp, key=OHLCVScreener.NAME)
        # end if

    return True
# end record_ohlcv

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

class OHLCVMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.market.screeners import OHLCVMarketRecorder
    >>>
    >>> recorder = OHLCVMarketRecorder(...)
    """

    COLUMNS = OHLCVScreener.COLUMNS

    def __init__(
            self,
            screeners: Iterable[BaseScreener],
            callbacks: Optional[Iterable[Callback]] = None,
    ) -> None:
        """
        Defines the class attributes.

        :param screeners: The screener objects.
        :param callbacks: The callbacks for the service.
        """

        super().__init__(screeners=screeners, callbacks=callbacks)

        self._indexes: Indexes = {}
    # end __init__

    @property
    def ohlcv_screeners(self) -> List[OHLCVScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return self.find_screeners(base=OHLCVScreener)
    # end ohlcv_screeners

    @property
    def orderbook_screeners(self) -> List[OrderbookScreener]:
        """
        Returns a list of all the ohlcv screeners.

        :return: The ohlcv screeners.
        """

        return self.find_screeners(base=OrderbookScreener)
    # end orderbook_screeners

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[L2_BOOK],
            callbacks={L2_BOOK: self.record},
            max_depth=1
        )
    # end parameters

    async def process(self, data: OrderBook, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        exchange = data.exchange.lower()
        symbol = adjust_symbol(symbol=data.symbol)

        screeners = []

        screeners.extend(
            self.find_screeners(
                base=OrderbookScreener, exchange=exchange, symbol=symbol
            )
        )
        screeners.extend(
            self.find_screeners(
                base=OHLCVScreener, exchange=exchange, symbol=symbol
            )
        )

        return await record_ohlcv(
            screeners=screeners, data=data, indexes=self._indexes,
            callbacks=self.callbacks, timestamp=timestamp
        )
    # end process
# end MarketOHLCVRecorder

class OHLCVMarketScreener(MarketScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - screeners:
        The screeners to connect to the market screener.

    - intervals:
        The structure to set a specific interval to the dataset
        of each symbol in each exchange, matching the market data.

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

    >>> from crypto_screening.market.screeners import ohlcv_market_screener
    >>>
    >>> structure = {'1m': {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}}
    >>>
    >>> screener = ohlcv_market_screener(data=structure)
    >>> screener.run()
    """

    screeners: List[Union[OHLCVScreener, OrderbookScreener]]
    recorder: OHLCVMarketRecorder

    COLUMNS = OHLCVMarketRecorder.COLUMNS

    def __init__(
            self,
            recorder: OHLCVMarketRecorder,
            screeners: Optional[Iterable[Union[OHLCVScreener, OrderbookScreener]]] = None,
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
            delay=delay, recorder=recorder,
            screeners=screeners, handler=handler, limited=limited,
            amount=amount, refresh=refresh
        )
    # end __init__

    @property
    def ohlcv_screeners(self) -> List[OHLCVScreener]:
        """
        Returns a list of all the ohlcv screeners.

        :return: The ohlcv screeners.
        """

        return self.find_screeners(base=OHLCVScreener)
    # end ohlcv_screeners

    @property
    def orderbook_screeners(self) -> List[OrderbookScreener]:
        """
        Returns a list of all the ohlcv screeners.

        :return: The ohlcv screeners.
        """

        return self.find_screeners(base=OrderbookScreener)
    # end orderbook_screeners

    def merge_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        for ohlcv_screener in self.ohlcv_screeners:
            for orderbook_screener in self.orderbook_screeners:
                if (
                    (ohlcv_screener.exchange == orderbook_screener.exchange) and
                    (ohlcv_screener.symbol == orderbook_screener.symbol)
                ):
                    ohlcv_screener.orderbook_market = orderbook_screener.market
                # end if
            # end for
        # end for
    # end merge_screeners
# end MarketOHLCVRecorder

def create_ohlcv_screeners(
        data: Dict[str, Union[Iterable[str], Dict[str, Iterable[str]]]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
) -> List[OHLCVScreener]:
    """
    Defines the class attributes.

    :param data: The data for the screeners.
    :param location: The saving location for the data.
    :param cancel: The time to cancel the waiting.
    :param delay: The delay for the process.
    """

    screeners = []

    for exchange, symbols in data.items():
        if isinstance(symbols, dict):
            for symbol, intervals in symbols.items():
                for interval in intervals:
                    screeners.append(
                        OHLCVScreener(
                            symbol=symbol, exchange=exchange, delay=delay,
                            location=location, cancel=cancel, interval=interval
                        )
                    )
            # end for

        else:
            for symbol in symbols:
                screeners.append(
                    OHLCVScreener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel,
                    )
                )
        # end if
    # end for

    return screeners
# end create_ohlcv_screeners

def ohlcv_market_screener(
        data: Dict[str, Union[Iterable[str], Dict[str, Iterable[str]]]],
        screeners: Optional[Iterable[OrderbookScreener]] = None,
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[MarketHandler] = None,
        amount: Optional[int] = None,
        callbacks: Optional[Iterable[Callback]] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[OHLCVMarketRecorder] = None
) -> OHLCVMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param screeners: The base screeners.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param callbacks: The callbacks for the service.

    :return: The market screener object.
    """

    orderbook_screeners = (screeners or []) or create_orderbook_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay
    )

    ohlcv_screeners = create_ohlcv_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay
    )

    screeners = []
    screeners.extend(orderbook_screeners)
    screeners.extend(ohlcv_screeners)

    market = OHLCVMarketScreener(
        recorder=recorder or OHLCVMarketRecorder(
            screeners=screeners, callbacks=callbacks
        ), screeners=screeners,
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )

    market.merge_screeners()

    return market
# end orderbook_market_recorder