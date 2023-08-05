import json
import requests
from datetime import date
from decimal import Decimal
from geld.common.exceptions import APICallError, BaseUrlNotDefined


class SyncClientBase:
    _base_url = None

    def __init__(self):
        if not self._base_url:
            raise BaseUrlNotDefined

    def convert_currency(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal,
        date: str = None,
    ) -> Decimal:
        if from_currency == to_currency:
            return amount

        url = self._get_url(date)
        params = self._get_params(from_currency, to_currency)
        response = self._execute_request(url, params)

        if not response.status_code == 200:
            raise APICallError

        rate = self._get_rate_from_response(response, to_currency)
        converted_amount = self._convert_amount(amount, rate)

        return converted_amount

    def _get_url(self, date: str):
        return f"{self._base_url}/{date}/"

    def _get_params(self, from_currency: str, to_currency: str):
        return {
            "base": from_currency,
            "symbols": to_currency,
        }

    def _execute_request(self, url: str, params: dict):
        return requests.get(url, params=params)

    def _get_rate_from_response(self, response, to_currency: str):
        data = json.loads(response.text)
        rate = Decimal(data["rates"][to_currency])
        return rate

    def _convert_amount(self, amount: Decimal, rate: Decimal):
        return amount * rate
