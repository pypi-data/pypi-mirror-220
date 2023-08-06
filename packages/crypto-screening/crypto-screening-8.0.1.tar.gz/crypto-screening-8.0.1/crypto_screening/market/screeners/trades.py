# trades.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Union, List, Callable
)

import pandas as pd

from cryptofeed.types import Trade
from cryptofeed.defines import TRADES

from crypto_screening.symbols import adjust_symbol
from crypto_screening.dataset import (
    TRADES_COLUMNS, create_dataset, AMOUNT, PRICE, SIDE
)
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.callbacks import Callback, callback_data
from crypto_screening.market.screeners.recorder import (
    MarketScreener, MarketRecorder, MarketHandler
)

__all__ = [
    "TradesMarketScreener",
    "TradesMarketRecorder",
    "TradesScreener",
    "trades_market_screener",
    "create_trades_market_dataset",
    "record_trades",
    "create_trades_screeners"
]

def create_trades_market_dataset() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_dataset(
        columns=TradesMarketRecorder.COLUMNS
    )
# end create_trades_market_dataset

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
        screeners: Iterable[TradesScreener],
        data: Trade,
        timestamp: float,
        callbacks: Optional[Iterable[Callback]] = None
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param screeners: The screeners.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    :param callbacks: The callbacks for the service.

    :return: The validation value.
    """

    exchange = data.exchange.lower()
    symbol = adjust_symbol(symbol=data.symbol)

    try:
        index = dt.datetime.fromtimestamp(timestamp)

        data = {
            AMOUNT: float(data.amount),
            PRICE: float(data.price),
            SIDE: data.side
        }

        valid = False

        for screener in screeners:
            if index in screener.market.index:
                continue
            # end if

            valid = True

            screener.market.loc[index] = data
        # end for

        if valid:
            for callback in callbacks or []:
                payload = callback_data(
                    data=[(timestamp, data)],
                    exchange=exchange, symbol=symbol
                )

                await callback.record(
                    payload, timestamp, key=TradesScreener.NAME
                )
            # end if
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

    - screeners:
        The screeners to record data into their market datasets.

    - callbacks:
        The callbacks to run when collecting new data.

    >>> from crypto_screening.market.screeners import TradesMarketRecorder
    >>>
    >>> recorder = TradesMarketRecorder(...)
    """

    COLUMNS = TradesScreener.COLUMNS

    @property
    def trades_screeners(self) -> List[TradesScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return self.find_screeners(base=TradesScreener)
    # end trades_screeners

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

    async def process(self, data: Trade, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.

        :return: The validation value.
        """

        exchange = data.exchange.lower()
        symbol = adjust_symbol(symbol=data.symbol)

        return await record_trades(
            screeners=self.find_screeners(
                base=TradesScreener, exchange=exchange, symbol=symbol
            ), data=data, timestamp=timestamp, callbacks=self.callbacks
        )
    # end process
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
    def trades_screeners(self) -> List[TradesScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return self.find_screeners(base=TradesScreener)
    # end trades_screeners
# end MarketOrderbookScreener

def create_trades_screeners(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
) -> List[TradesScreener]:
    """
    Defines the class attributes.

    :param data: The data for the screeners.
    :param location: The saving location for the data.
    :param cancel: The time to cancel the waiting.
    :param delay: The delay for the process.
    """

    screeners = []

    for exchange, symbols in data.items():
        for symbol in symbols:
            screeners.append(
                TradesScreener(
                    symbol=symbol, exchange=exchange, delay=delay,
                    location=location, cancel=cancel
                )
            )
        # end for
    # end for

    return screeners
# end create_trades_screeners

def trades_market_screener(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[MarketHandler] = None,
        amount: Optional[int] = None,
        callbacks: Optional[Iterable[Callback]] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[TradesMarketRecorder] = None
) -> TradesMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
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

    screeners = create_trades_screeners(
        data=data, location=location,
        cancel=cancel, delay=delay
    )

    return TradesMarketScreener(
        recorder=recorder or TradesMarketRecorder(
            screeners=screeners, callbacks=callbacks
        ), screeners=screeners,
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )
# end trades_market_screener