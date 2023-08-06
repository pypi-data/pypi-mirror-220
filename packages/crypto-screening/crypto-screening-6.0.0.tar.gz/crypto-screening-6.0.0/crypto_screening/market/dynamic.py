# dynamic.py

from typing import Optional, Iterable, List, Union, Dict

from represent import Modifiers

import pandas as pd

from crypto_screening.collect.screeners import exchanges_symbols_screeners
from crypto_screening.market.screeners.ohlcv import OHLCVScreener
from crypto_screening.collect.market.orderbook import (
    assets_orderbook_market_state, symbols_orderbook_market_state,
    SymbolsOrderbookMarketState, AssetsOrderbookMarketState
)
from crypto_screening.collect.market.ohlcv import (
    assets_ohlcv_market_state, symbols_ohlcv_market_state,
    SymbolsOHLCVMarketState, AssetsOHLCVMarketState
)
from crypto_screening.collect.market.orders import (
    assets_orders_market_state, symbols_orders_market_state,
    SymbolsOrdersMarketState, AssetsOrdersMarketState
)
from crypto_screening.collect.market.trades import (
    assets_trades_market_state, symbols_trades_market_state,
    SymbolsTradesMarketState, AssetsTradesMarketState
)
from crypto_screening.market.screeners.container import ScreenersContainer

__all__ = [
    "DynamicScreenerContainer"
]

class DynamicScreenerContainer(ScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    >>> from crypto_screening.market.dynamic import DynamicScreenerContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> dynamic_screener = DynamicScreenerContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> dynamic_screener.find_screener(exchange="binance", symbol="BTC/USDT"))
    >>> dynamic_screener.data(exchange="binance", symbol="BTC/USDT", length=10))
    """

    __modifiers__ = Modifiers(**ScreenersContainer.__modifiers__)
    __modifiers__.excluded.append("exchanges")

    def find_ohlcv_dataset(
            self,
            exchange: str,
            symbol: str,
            interval: str,
            length: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the dataset.
        :param length: The length of the data.

        :return: The data.
        """

        screener = self.find_ohlcv_screener(
            exchange=exchange, symbol=symbol, interval=interval
        )

        length = min(length or 0, len(screener.market))

        return screener.market.iloc[-length:]
    # end find_ohlcv_dataset

    def find_orderbook_dataset(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        try:
            screener = self.find_orderbook_screener(
                exchange=exchange, symbol=symbol
            )

            market = screener.market

        except ValueError:
            screener = self.find_screeners(
                exchange=exchange, symbol=symbol
            )[0]

            if isinstance(screener, OHLCVScreener):
                market = screener.orderbook_market

            else:
                market = screener.market
            # end if
        # end try

        length = min(length or 0, len(market))

        return market.iloc[-length:]
    # end find_orderbook_dataset

    def find_orders_dataset(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screener = self.find_orders_screener(
            exchange=exchange, symbol=symbol
        )

        length = min(length or 0, len(screener.market))

        return screener.market.iloc[-length:]
    # end find_orders_dataset

    def find_trades_dataset(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screener = self.find_trades_screener(
            exchange=exchange, symbol=symbol
        )

        length = min(length or 0, len(screener.market))

        return screener.market.iloc[-length:]
    # end find_trades_dataset

    def find_datasets(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> List[pd.DataFrame]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screeners = self.find_screeners(exchange=exchange, symbol=symbol)

        return [
            screener.market.iloc[-min(length or 0, len(screener.market)):]
            for screener in screeners
        ]
    # end find_dataset

    def assets_orderbook_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsOrderbookMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = []
        screeners.extend(self.orderbook_screeners)
        screeners.extend(self.ohlcv_screeners)

        screeners = exchanges_symbols_screeners(
            screeners=screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_orderbook_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_orderbook_market_state

    def symbols_orderbook_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsOrderbookMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = []
        screeners.extend(self.orderbook_screeners)
        screeners.extend(self.ohlcv_screeners)

        screeners = exchanges_symbols_screeners(
            screeners=screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_orderbook_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_orderbook_market_state

    def assets_ohlcv_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsOHLCVMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.ohlcv_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_ohlcv_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_ohlcv_market_state

    def symbols_ohlcv_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsOHLCVMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.ohlcv_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_ohlcv_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_ohlcv_market_state

    def assets_trades_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsTradesMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.trades_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_trades_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_trades_market_state

    def symbols_trades_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsTradesMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.trades_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_trades_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_trades_market_state

    def assets_orders_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsOrdersMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.orders_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_orders_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_orders_market_state

    def symbols_orders_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsOrdersMarketState:
        """
        Fetches the values and relations between the assets.

        :param length: The length of the values.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The values of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.orders_screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_orders_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_orders_market_state
# end DynamicScreenerContainer