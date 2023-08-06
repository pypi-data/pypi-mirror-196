import datetime
import requests


def rates() -> list:
    """ Returns:
        list: [date, usdnok, usdeur]
    """
    date = datetime.datetime.now().strftime("%d-%m-%y")
    exchange_prices = []
    currency_codes = ['USD','NOK','EUR']
    for currency in currency_codes:
        res = requests.get(f"https://prices.azure.com/api/retail/prices?currencyCode='{currency}'&$filter=skuid eq 'DZH318Z08M9X/0147'").json()
        for elem in res["Items"]:
            exchange_prices.append(elem["retailPrice"])
    
    usdnok = exchange_prices[1]/exchange_prices[0]
    usdeur = exchange_prices[2]/exchange_prices[0]
    return [date,usdnok,usdeur]