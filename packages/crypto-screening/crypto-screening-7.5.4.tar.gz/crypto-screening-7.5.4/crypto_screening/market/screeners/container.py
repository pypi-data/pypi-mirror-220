# container.py

from typing import Iterable, List, Type, TypeVar, Optional, Dict

from represent import represent

from crypto_screening.market.screeners.ohlcv import OHLCVScreener
from crypto_screening.market.screeners.orderbook import OrderbookScreener
from crypto_screening.market.screeners.trades import TradesScreener
from crypto_screening.market.screeners.orders import OrdersScreener
from crypto_screening.market.screeners.base import BaseScreener

__all__ = [
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
        for interval in {
            (
                screener.interval
                if isinstance(screener, OHLCVScreener) else
                None
            ), None
        }:
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
    # end for

    return table
# end screeners_table

@represent
class ScreenersContainer:
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> from crypto_screening.market.screeners.container import ScreenersContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> container = ScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        self._screeners = list(screeners)

        self._table = screeners_table(self.screeners)
    # end __init__

    @property
    def screeners(self) -> List[BaseScreener]:
        """
        Returns a list of all the screeners.

        :return: The screeners.
        """

        return list(self._screeners)
    # end screeners

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

    def update(self) -> None:
        """Updates the records of the object."""
    # end update

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list([symbol for symbol in symbols if symbol is not None])
            for exchange, symbols in self._table[None].items()
            if exchange is not None
        }
    # end structure

    def add(
            self,
            screeners: Iterable[BaseScreener],
            adjust: Optional[bool] = True,
            update: Optional[bool] = True
    ) -> None:
        """
        Updates the data with the new screeners.

        :param screeners: The new screeners to add.
        :param adjust: The value to adjust for screeners.
        :param update: The value to update.
        """

        new_screeners = []

        for screener in screeners:
            if screener not in self._screeners:
                new_screeners.append(screener)

            elif not adjust:
                raise ValueError(
                    f"Cannot add screener {repr(screener)} to "
                    f"{repr(self)} because it is already present."
                )
            # end if
        # end for

        self._screeners.extend(new_screeners)

        screeners_table(new_screeners, table=self._table)

        if update:
            self.update()
        # end if
    # end update

    def remove(
            self,
            screeners: Iterable[BaseScreener],
            adjust: Optional[bool] = True,
            update: Optional[bool] = True
    ) -> None:
        """
        Updates the data with the new screeners.

        :param screeners: The new screeners to add.
        :param adjust: The value to adjust for screeners.
        :param update: The value to update.
        """

        for screener in screeners:
            if screener in self._screeners:
                self._screeners.remove(screener)

            elif not adjust:
                raise ValueError(
                    f"Cannot remove screener {repr(screener)} from "
                    f"{repr(self)} because it is not present."
                )
            # end if
        # end for

        self._table.clear()

        screeners_table(self._screeners, table=self._table)

        if update:
            self.update()
        # end if
    # end remove

    def find_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None,
            adjust: Optional[bool] = True
    ) -> List[_S]:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the search.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        try:
            return list(self._table[base][exchange][symbol][interval])

        except KeyError:
            if not adjust:
                raise ValueError(
                    f"Cannot find screeners  matching to "
                    f"type - {base}, exchange - {exchange}, "
                    f"symbol - {symbol}, interval - {interval} "
                    f"inside {repr(self)}"
                )
            # end if
        # end try
    # end find_screeners

    def find_screener(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            base: Optional[Type[_S]] = None,
            interval: Optional[str] = None,
            index: Optional[int] = None,
            adjust: Optional[bool] = True
    ) -> _S:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the search.
        :param index: The index of the screener in the list.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        try:
            return self.find_screeners(
                exchange=exchange, symbol=symbol,
                base=base, interval=interval, adjust=adjust
            )[index or 0]

        except IndexError:
            if not adjust:
                raise IndexError(
                    f"Cannot find screeners matching to "
                    f"type - {base}, exchange - {exchange}, "
                    f"symbol - {symbol}, interval - {interval}, "
                    f"index - {index} inside {repr(self)}"
                )
            # end if
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
        :param symbol: The symbol name.
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
        :param symbol: The symbol name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end orderbook_screener_in_market

    def orders_screener_in_market(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.

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
        :param symbol: The symbol name.
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
        :param symbol: The symbol name.
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
            adjust: Optional[bool] = True
    ) -> List[OrderbookScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol,
            base=OrderbookScreener, adjust=adjust
        )
    # end find_orderbook_screener

    def find_orders_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            adjust: Optional[bool] = True
    ) -> List[OrdersScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol,
            base=OrdersScreener, adjust=adjust
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
        :param symbol: The symbol name.
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
            symbol: Optional[str] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.

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
        :param symbol: The symbol name.
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
        :param symbol: The symbol name.
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
            interval: Optional[str] = None,
            adjust: Optional[bool] = True
    ) -> List[OHLCVScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the datasets.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OHLCVScreener,
            interval=interval, adjust=adjust
        )
    # end find_ohlcv_screeners

    def find_trades_screeners(
            self,
            exchange: Optional[str] = None,
            symbol: Optional[str] = None,
            adjust: Optional[bool] = True
    ) -> List[TradesScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=TradesScreener,
            adjust=adjust
        )
    # end find_trades_screeners
# end MappedScreenersContainer