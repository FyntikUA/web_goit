import asyncio
import datetime
import aiohttp
import argparse
import json


'''Приклад виклику програми "python main.py 3 EUR USD GBP" - де "3" це кількість днів, не більше 10, 
                                                            "EUR USD GBP" вибір валют.
'''


async def fetch_exchange_rates(date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_currency_rates(days, currencies):
    tasks = []
    results = []

    # Отримуємо курси валют для кожного дня
    for day in range(days):
        date = (datetime.date.today() - datetime.timedelta(days=day)).strftime('%d.%m.%Y')
        tasks.append(fetch_exchange_rates(date))

    # Очікуємо завершення всіх асинхронних запитів
    responses = await asyncio.gather(*tasks)

    # Обробляємо результати запитів
    for idx, data in enumerate(responses):
        rates = {}
        for currency in currencies:
            currency_data = next((item for item in data['exchangeRate'] if item['currency'] == currency), None)
            if currency_data:
                rates[currency] = {
                    'sale': currency_data['saleRateNB'],
                    'purchase': currency_data['purchaseRateNB']
                }
        results.append({(datetime.date.today() - datetime.timedelta(days=idx)).strftime('%d.%m.%Y'): rates})

    return results

def parse_args():
    parser = argparse.ArgumentParser(description='Get exchange rates for selected currencies from PrivatBank API.')
    parser.add_argument('days', type=int, nargs='?', default=1, help='Number of days to retrieve exchange rates for (up to 10 days)')
    parser.add_argument('currencies', metavar='currency', nargs='*', type=str, help='List of currencies to retrieve rates for (e.g., EUR USD)')
    return parser.parse_args()

#def parse_args():
#    parser = argparse.ArgumentParser(description='Get exchange rates for selected currencies from PrivatBank API.')
#    parser.add_argument('days', type=int, help='Number of days to retrieve exchange rates for (up to 10 days)')
#    parser.add_argument('currencies', metavar='currency', nargs='+', type=str, help='List of currencies to retrieve rates for (e.g., EUR USD)')
#    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.days > 10:
        print('Error: Maximum number of days allowed is 10.')
        exit(1)

    rates = asyncio.run(get_currency_rates(args.days, args.currencies))
    print(json.dumps(rates, indent=2))
