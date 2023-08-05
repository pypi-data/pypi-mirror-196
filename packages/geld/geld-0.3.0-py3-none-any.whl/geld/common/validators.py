from datetime import datetime
from decimal import Decimal
from geld.common.constants import CURRENCY_DATA
from geld.common.exceptions import (
    InvalidAmount,
    InvalidCurrencyCode,
    InvalidDate,
)


def currency_code_validator(currency_code: str) -> str:
    """
    Validates a given currency code.

    Args:
        currency_code (str): The currency code to validate.

    Returns:
        str: The validated currency code.

    Raises:
        InvalidCurrencyCode: If the given currency code is not valid.
    """
    try:
        _ = CURRENCY_DATA[currency_code]
    except KeyError:
        raise InvalidCurrencyCode
    return currency_code


def date_validator(date: str) -> str:
    """
    Validates a given date.

    Args:
        date str or datetime.datetime): The date to validate.

    Returns:
        str: The validated date in the format "YYYY-MM-DD".

    Raises:
        InvalidDate: If the given date is not valid.
    """
    if not date or date == "latest":
        return "latest"
    try:
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
        date, _ = date.isoformat().split("T")
    except (AttributeError, ValueError):
        raise InvalidDate
    return date


def amount_validator(amount: Decimal) -> Decimal:
    """
    Validates a given amount.

    Args:
        amount (Decimal or float or int or str): The amount to validate.

    Returns:
        Decimal: The validated amount as a Decimal object.

    Raises:
        InvalidAmount: If the given amount is not valid (not a Decimal object, negative).
    """
    try:
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
    except Exception:
        raise InvalidAmount
    if amount < 0:
        raise InvalidAmount
    return amount
