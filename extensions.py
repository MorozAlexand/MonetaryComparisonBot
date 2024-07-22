import requests
import json
from config import keys

class ApiException(Exception):
    pass

class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ApiException(f'Не возможно конвертировать одинаковые валюты {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiException(
                f'Не удалось обработать валюту {quote}.\n Cписок доступных валют для конвертирования: /values.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiException(
                f'Не удалось обработать валюту {base}.\n Cписок доступных валют для конвертирования: /values.')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}.\n Введите число.')
        r = requests.get(f'https://v6.exchangerate-api.com/v6/e7bafc77ba508e11b4f9c7e7/pair/{quote_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(r.content)['conversion_result']
        return total_base
