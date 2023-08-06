# trades.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any, Union, List, Callable
)

import pandas as pd

from sqlalchemy import Engine

from cryptofeed import FeedHandler
from cryptofeed.types import Trade
from cryptofeed.defines import TRADES

from crypto_screening.symbols import adjust_symbol
from crypto_screening.process import find_string_value
from crypto_screening.dataset import (
    TRADES_COLUMNS, create_dataset, AMOUNT, PRICE, SIDE
)
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.callbacks import Callback, callback_data
from crypto_screening.market.screeners.recorder import MarketScreener, MarketRecorder

__all__ = [
    "TradesMarketScreener",
    "TradesMarketRecorder",
    "TradesScreener",
    "create_trades_market",
    "trades_market_screener",
    "trades_market_recorder",
    "create_trades_market_dataset",
    "record_trades"
]

Market = Dict[str, Dict[str, pd.DataFrame]]

def create_trades_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(
        columns=TradesMarketRecorder.COLUMNS
    )
# end create_trades_market_dataset

def create_trades_market(data: Dict[str, Iterable[str]]) -> Market:
    """
    Creates the dataframes of the market data.

    :param data: The market data.

    :return: The dataframes of the market data.
    """

    return {
        exchange.lower(): {
            symbol.upper(): create_trades_market_dataset()
            for symbol in data[exchange]
        } for exchange in data
    }
# end create_trades_market

class TradesScreener(BaseScreener):
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

    - market:
        The dataset of the market data as trades.
    """

    NAME = "TRADES"

    COLUMNS = TRADES_COLUMNS

    @property
    def trades_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end trades_market
# end TradesScreener

async def record_trades(
        market: Market,
        data: Trade,
        timestamp: float,
        callbacks: Optional[Iterable[Callback]] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param market: The market structure.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    exchange = find_string_value(
        value=data.exchange, values=market.keys()
    )
    symbol = find_string_value(
        value=adjust_symbol(symbol=data.symbol),
        values=exchange
    )

    dataset = (
        market.
        setdefault(exchange, {}).
        setdefault(symbol, create_trades_market_dataset())
    )

    try:
        index = dt.datetime.fromtimestamp(timestamp)

        if index in dataset.index:
            return False
        # end if

        data = {
            AMOUNT: float(data.amount),
            PRICE: float(data.price),
            SIDE: data.side
        }

        dataset.loc[index] = data

        for callback in callbacks or []:
            payload = callback_data(
                data=[(timestamp, data)], exchange=exchange, symbol=symbol
            )

            await callback.record(payload, timestamp, key=TradesScreener.NAME)
        # end if

        return True

    except IndexError:
        return False
    # end try
# end record_trades

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

class TradesMarketRecorder(MarketRecorder):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - market:
        The market structure of the data to store the fetched data in.
        This structure is a dictionary with exchange names as keys
        and dictionaries as values, where their keys are symbols,
        and their values are the dataframes to record the data.

    - databases:
        The databases and their engines for storing data in databases.

    >>> from crypto_screening.market.screeners import orderbook_market_recorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = orderbook_market_recorder(data=market)
    """

    COLUMNS = TradesScreener.COLUMNS

    @property
    def trades_market(self) -> Market:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end trades_market

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[TRADES],
            callbacks={TRADES: self.record},
            max_depth=1
        )
    # end parameters

    def trades(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source key of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.data(exchange=exchange, symbol=symbol)
    # end trades

    def trades_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source key of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        try:
            self.trades(exchange=exchange, symbol=symbol)

            return True

        except ValueError:
            return False
        # end try
    # end trades_in_market

    async def record(self, data: Trade, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.

        :return: The validation value.
        """

        return await record_trades(
            market=self.market, data=data, timestamp=timestamp,
            callbacks=self.callbacks
        )
    # end record
# end TradesRecorder

class TradesMarketScreener(MarketScreener):
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

    >>> from crypto_screening.market.screeners import trades_market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = trades_market_screener(data=structure)
    >>> screener.run()
    """

    screeners: List[TradesScreener]
    recorder: TradesMarketRecorder

    COLUMNS = TradesMarketRecorder.COLUMNS

    def __init__(
            self,
            recorder: TradesMarketRecorder,
            screeners: Optional[Iterable[TradesScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
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

        self.screeners[:] = screeners or self.create_trades_screeners()
    # end __init__

    @property
    def trades_market(self) -> Market:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.recorder.trades_market
    # end trades_market

    @property
    def trades_screeners(self) -> List[TradesScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, TradesScreener)
        ]
    # end trades_screeners

    def connect_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        for screener in self.screeners:
            if isinstance(screener, TradesScreener):
                screener.market = self.trades(
                    exchange=screener.exchange, symbol=screener.symbol
                )
            # end if
        # end for
    # end connect_screeners

    def trades(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source key of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.trades(exchange=exchange, symbol=symbol)
    # end trades

    def trades_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source key of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.trades_in_market(exchange=exchange, symbol=symbol)
    # end trades_in_market

    def create_trades_screener(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, TradesScreener]]] = None
    ) -> TradesScreener:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screener.
        """

        if container is None:
            container = {}
        # end if

        if cancel is None:
            cancel = self.cancel
        # end if

        if delay is None:
            delay = self.delay
        # end if

        screener = TradesScreener(
            symbol=symbol, exchange=exchange, delay=delay,
            location=location, cancel=cancel, market=(
                self.trades(exchange=exchange, symbol=symbol)
                if self.trades_in_market(symbol=symbol, exchange=exchange)
                else None
            )
        )

        container.setdefault(exchange, {})[symbol] = screener

        return screener
    # end create_trades_screener

    def create_trades_screeners(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, TradesScreener]]] = None
    ) -> List[TradesScreener]:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screeners.
        """

        screeners = []

        for exchange, symbols in self.structure().items():
            for symbol in symbols:
                screeners.append(
                    self.create_trades_screener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel, container=container
                    )
                )
            # end for
        # end for

        return screeners
    # end create_trades_screeners
# end MarketOrderbookScreener

Databases = Union[Iterable[str], Dict[str, Engine]]

def trades_market_recorder(data: Dict[str, Iterable[str]]) -> TradesMarketRecorder:
    """
    Creates the market recorder object for the data.

    :param data: The market data.

    :return: The market recorder object.
    """

    return TradesMarketRecorder(
        market=create_trades_market(data=data)
    )
# end trades_market_recorder

def trades_market_screener(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[FeedHandler] = None,
        market: Optional[Market] = None,
        amount: Optional[int] = None,
        callbacks: Optional[Iterable[Callback]] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[TradesMarketRecorder] = None,
        fixed: Optional[bool] = True,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> TradesMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param parameters: The parameters for the exchanges.
    :param market: The object to fill with the crypto feed record.
    :param fixed: The value for fixed parameters to all exchanges.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param callbacks: The callbacks for the service.

    :return: The market screener object.
    """

    screener = TradesMarketScreener(
        recorder=recorder or TradesMarketRecorder(
            market=market or create_trades_market(data=data),
            callbacks=callbacks
        ),
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )

    screener.add_feeds(
        data=screener.recorder.structure(),
        fixed=fixed, parameters=parameters
    )

    return screener
# end trades_market_screener