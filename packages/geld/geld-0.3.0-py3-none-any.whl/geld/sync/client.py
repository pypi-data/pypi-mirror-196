from geld.common.constants import BASE_URL
from geld.common.decorators import validate_currency_conversion_data
from geld.sync.base import SyncClientBase

from decimal import Decimal


class SyncClient(SyncClientBase):
    """
    A synchronous client for accessing the Currency Converter API and converting currency amounts.

    Attributes:
        _base_url (str): The base URL of the Currency Converter API.

    Methods:
        convert_currency: Converts a specified amount of currency from one currency code to another for a given date.
    """

    _base_url = BASE_URL

    @validate_currency_conversion_data
    def convert_currency(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal = 1,
        date: str = "latest",
    ) -> Decimal:
        """
        Converts a specified amount of currency from one currency code to another for a given date using the Currency Converter API.

        Args:
            from_currency (str): The currency code for the currency to convert from.
            to_currency (str): The currency code for the currency to convert to.
            amount (Decimal, optional): The amount of currency to convert. Defaults to 1.
            date (str, optional): The date to use for the conversion rate. Should be in the format "YYYY-MM-DD" or "latest". Defaults to "latest".

        Returns:
            Decimal: The converted amount of currency as a Decimal object.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the request to the API.
            InvalidCurrencyCode: If the from_currency or to_currency arguments are not valid currency codes.
            InvalidAmount: If the amount argument is not a valid Decimal object or is negative.
            InvalidDate: If the date argument is not in a valid format.
            KeyError: If the API response does not contain the expected keys.
            ValueError: If the API response contains invalid data.
        """
        return super(SyncClient, self).convert_currency(
            from_currency, to_currency, amount, date
        )
