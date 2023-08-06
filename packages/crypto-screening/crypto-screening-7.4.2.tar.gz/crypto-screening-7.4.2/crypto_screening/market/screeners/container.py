# container.py

from abc import ABCMeta, abstractmethod
from typing import Iterable, List, Type, TypeVar, Optional, Dict

from represent import represent, Modifiers

from crypto_screening.market.screeners.ohlcv import OHLCVScreener
from crypto_screening.market.screeners.orderbook import OrderbookScreener
from crypto_screening.market.screeners.trades import TradesScreener
from crypto_screening.market.screeners.orders import OrdersScreener
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.recorder import structure_screener_datasets

__all__ = [
    "DynamicScreenersContainer",
    "FixedScreenersContainer",
    "screeners_table",
    "ScreenersContainer"
]

_S = TypeVar(
    "_S",
    BaseScreener,
    OHLCVScreener,
    OrderbookScreener,
    TradesScreener,
    OrdersScreener
)

@represent
class ScreenersContainer(metaclass=ABCMeta):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    >>> from crypto_screening.market.screeners.container import ScreenersContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> container = ScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    __modifiers__ = Modifiers(hidden=["screeners"])

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        self.screeners = list(screeners)

        self.market = structure_screener_datasets(self.screeners)
    # end __init__

    @property
    def orderbook_screeners(self) -> List[OrderbookScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return self.find_screeners(base=OrderbookScreener)
    # end orderbook_screeners

    @property
    def orders_screeners(self) -> List[OrdersScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The orders screeners.
        """

        return self.find_screeners(base=OrdersScreener)
    # end orders_screeners

    @property
    def ohlcv_screeners(self) -> List[OHLCVScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The OHLCV screeners.
        """

        return self.find_screeners(base=OHLCVScreener)
    # end ohlcv_screeners

    @property
    def trades_screeners(self) -> List[TradesScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The trades screeners.
        """

        return self.find_screeners(base=TradesScreener)
    # end trades_screeners

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list(symbols.keys())
            for exchange, symbols in self.market.items()
        }
    # end structure

    @abstractmethod
    def find_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None
    ) -> List[_S]:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the search.

        :return: The data.
        """
    # end find_screeners

    def find_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None,
            index: Optional[int] = None
    ) -> _S:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the search.
        :param index: The index of the screener in the list.

        :return: The data.
        """

        try:
            return self.find_screeners(
                exchange=exchange, symbol=symbol,
                base=base, interval=interval
            )[index or 0]

        except IndexError:
            raise IndexError(
                f"Cannot find screeners  matching to "
                f"type - {base}, exchange - {exchange}, "
                f"symbol - {symbol}, interval - {interval}, "
                f"index - {index} inside {repr(self)}"
            )
        # end try
    # end find_orderbook_screener

    def screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval to search.

        :return: The data.
        """

        try:
            self.find_screener(
                exchange=exchange, symbol=symbol,
                base=base, interval=interval
            )

            return True

        except ValueError:
            return False
        # end try
    # end screener_in_market

    def orderbook_screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end orderbook_screener_in_market

    def orders_screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=OrdersScreener
        )
    # end orders_screener_in_market

    def find_orderbook_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            index: Optional[int] = None
    ) -> OrderbookScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param index: The index of the screener in the list.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol,
            base=OrderbookScreener, index=index
        )
    # end find_orderbook_screener

    def find_orders_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            index: Optional[int] = None
    ) -> OrdersScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param index: The index of the screener in the list.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol,
            base=OrdersScreener, index=index
        )
    # end find_orders_screener

    def find_orderbook_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
    ) -> List[OrderbookScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end find_orderbook_screener

    def find_orders_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
    ) -> List[OrdersScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OrdersScreener
        )
    # end find_orders_screeners

    def ohlcv_screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            interval: Optional[str] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the dataset.

        :return: The data.
        """

        try:
            self.find_ohlcv_screener(
                exchange=exchange, symbol=symbol, interval=interval
            )

            return True

        except ValueError:
            return False
    # end ohlcv_screener_in_market

    def trades_screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=TradesScreener
        )
    # end trades_screener_in_market

    def find_ohlcv_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            interval: Optional[str] = None,
            index: Optional[int] = None
    ) -> OHLCVScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the dataset.
        :param index: The index for the screener.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=OHLCVScreener,
            interval=interval, index=index
        )
    # end find_screeners

    def find_trades_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            index: Optional[int] = None
    ) -> TradesScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param index: The index for the screener.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=TradesScreener,
            index=index
        )
    # end find_trades_screener

    def find_ohlcv_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            interval: Optional[str] = None
    ) -> List[OHLCVScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the datasets.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OHLCVScreener,
            interval=interval
        )
    # end find_ohlcv_screeners

    def find_trades_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
    ) -> List[TradesScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=TradesScreener
        )
    # end find_trades_screeners
# end ScreenersContainer

@represent
class DynamicScreenersContainer(ScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    >>> from crypto_screening.market.screeners.container import DynamicScreenersContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> container = DynamicScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    def find_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None
    ) -> List[_S]:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the search.

        :return: The data.
        """

        screeners = []

        for screener in self.screeners:
            if (
                ((screener.exchange == exchange) or (exchange is None)) and
                ((screener.symbol == symbol) or (symbol is None)) and
                isinstance(screener, base or BaseScreener) and
                (
                    (screener.interval == interval) if (
                        isinstance(screener, OHLCVScreener) and
                        (interval is not None)
                    ) else True
                )
            ):
                screeners.append(screener)
            # end if
        # end for

        return screeners
    # end find_screeners
# end ScreenersContainer

ScreenersTable = Dict[
    Optional[Type[BaseScreener]],
    Dict[
        Optional[str],
        Dict[Optional[str], Dict[Optional[str], List[BaseScreener]]]
    ]
]

def screeners_table(
        screeners: Iterable[BaseScreener],
        table: Optional[ScreenersTable] = None
) -> ScreenersTable:
    """
    Inserts all the screeners into the table.

    :param screeners: The screeners to insert into the table.
    :param table: The table to use for the data.

    :return: The screeners table.
    """

    if table is None:
        table = {}
    # end if

    for screener in screeners:
        interval = (
            screener.interval
            if isinstance(screener, OHLCVScreener) else
            None
        )

        lists = [
            (
                table.
                setdefault(type(screener), {}).
                setdefault(screener.exchange, {}).
                setdefault(screener.symbol, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(type(screener), {}).
                setdefault(screener.exchange, {}).
                setdefault(None, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(type(screener), {}).
                setdefault(None, {}).
                setdefault(screener.symbol, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(type(screener), {}).
                setdefault(None, {}).
                setdefault(None, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(type(screener), {}).
                setdefault(None, {}).
                setdefault(None, {}).
                setdefault(None, [])
            ),
            (
                table.
                setdefault(None, {}).
                setdefault(screener.exchange, {}).
                setdefault(screener.symbol, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(None, {}).
                setdefault(screener.exchange, {}).
                setdefault(None, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(None, {}).
                setdefault(None, {}).
                setdefault(screener.symbol, {}).
                setdefault(interval, [])
            ),
            (
                table.
                setdefault(None, {}).
                setdefault(None, {}).
                setdefault(None, {}).
                setdefault(interval, [])
            )
        ]

        for screeners_list in lists:
            if screener not in screeners_list:
                screeners_list.append(screener)
            # end if
        # end for
    # end for

    return table
# end screeners_table

class FixedScreenersContainer(ScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    >>> from crypto_screening.market.screeners.container import FixedScreenersContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> container = FixedScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        super().__init__(screeners=screeners)

        self._table = screeners_table(self.screeners)
    # end __init__

    def update(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Updates the data with the new screeners.

        :param screeners: The new screeners to add.
        """

        screeners = [
            screener for screener in screeners
            if screener not in self._screeners
        ]

        self.screeners.extend(screeners)

        screeners_table(screeners, table=self._table)
    # end update

    def find_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None
    ) -> List[_S]:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the search.

        :return: The data.
        """

        try:
            return list(self._table[base][exchange][symbol][interval])

        except KeyError:
            raise ValueError(
                f"Cannot find screeners  matching to "
                f"type - {base}, exchange - {exchange}, "
                f"symbol - {symbol}, interval - {interval} "
                f"inside {repr(self)}"
            )
        # end try
    # end find_screeners
# end FixedScreenersContainer