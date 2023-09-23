import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=1785a1e9298e9e0051fa3c9bced620e9&base=EUR&symbols=EUR,USD,RUB')
        in_base = json.loads(r.content)['rates']

        if base_ticker == 'EUR':
            total_base = in_base[quote_ticker]*amount
            return total_base
        elif base_ticker == 'RUB' and quote_ticker == 'EUR':
            total_base = amount/in_base[base_ticker]
            return total_base
        elif base_ticker == 'RUB' and quote_ticker == 'USD':
            total_base = (amount / in_base[base_ticker]) * in_base[quote_ticker]
            return total_base
        elif base_ticker == 'USD' and quote_ticker == 'EUR':
            total_base = amount / in_base[base_ticker]
            return total_base
        elif base_ticker == 'USD' and quote_ticker == 'RUB':
            total_base = (amount / in_base[base_ticker]) * in_base[quote_ticker]
            return total_base
