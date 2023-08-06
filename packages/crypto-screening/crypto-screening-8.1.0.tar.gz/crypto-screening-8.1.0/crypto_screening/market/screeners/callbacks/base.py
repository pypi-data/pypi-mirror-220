# base.py

import warnings
from typing import Optional, Any, Union, Dict, List, Tuple

__all__ = [
    "BaseCallback",
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
        BaseCallback.DATA: data,
        BaseCallback.EXCHANGE: exchange,
        BaseCallback.SYMBOL: symbol,
        BaseCallback.INTERVAL: interval
    }
# end callback_data

class BaseCallback:
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
# end BaseCallback