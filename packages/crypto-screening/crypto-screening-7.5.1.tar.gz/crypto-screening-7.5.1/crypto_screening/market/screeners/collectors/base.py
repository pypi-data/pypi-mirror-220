# base.py

import warnings
import threading
import datetime as dt
from typing import List, Tuple, Optional, Iterable, Union, Dict

from crypto_screening.market.screeners.base import BaseScreener, BaseMarketScreener
from crypto_screening.market.screeners.container import ScreenersContainer
from crypto_screening.collect.market.state.base import index_to_datetime

__all__ = [
    "ScreenersDataCollector"
]

Data = List[Tuple[Union[str, float, dt.datetime], Dict[str, Optional[Union[str, float, bool]]]]]

class ScreenersDataCollector(ScreenersContainer, BaseMarketScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - screeners:
        The screener object to control and fill with data.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - screeners:
        The screener object to control and fill with data.
    """

    def __init__(
            self,
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

        BaseMarketScreener.__init__(
            self, screeners=screeners, location=location,
            cancel=cancel, delay=delay
        )

        ScreenersContainer.__init__(self, screeners=screeners)
    # end __init__

    def handle(
            self,
            name: str,
            exchange: str,
            symbol: str,
            interval: str,
            data: Data
    ) -> None:
        """
        Handles the data received from the connection.

        :param data: The data to handle.
        :param name: The name of the data.
        :param exchange: The exchange of the screener.
        :param symbol: The symbol of the screener.
        :param interval: The interval of the screener.
        """

        screeners = self.find_screeners(
            base=BaseScreener.SCREENER_NAME_TYPE_MATCHES[name],
            exchange=exchange, symbol=symbol,
            interval=interval
        )

        for screener in screeners:
            for index, row in data:
                index = index_to_datetime(index)

                if index not in screener.market.index:
                    screener.market.loc[index] = row
                # end if
            # end for
        # end for
    # end handle

    def screening_loop(self) -> None:
        """Runs the process of the price screening."""
    # end screening_loop

    def start_screening(self) -> None:
        """Starts the screening process."""

        if self.screening:
            warnings.warn(f"Timeout screening of {self} is already running.")

            return
        # end if

        self._screening_process = threading.Thread(
            target=lambda: self.screening_loop()
        )

        self._screening_process.start()
    # end start_screening
# end ScreenersDataCollector