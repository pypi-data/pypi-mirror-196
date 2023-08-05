import datetime
import requests

def main() -> None:
    exchange_prices = []
    currency_code = ['USD','NOK','EUR']
    for currency in currency_code:
        res = requests.get(f"https://prices.azure.com/api/retail/prices?currencyCode='{currency}'&$filter=skuid eq 'DZH318Z08M9X/0147'").json()
        for elem in res["Items"]:
            exchange_prices.append(elem["retailPrice"])
    
    date = datetime.datetime.now().strftime("%d-%m-%y")
    usdnok = exchange_prices[1]/exchange_prices[0]
    usdeur = exchange_prices[2]/exchange_prices[0]
    
    todays_prices = [date,usdnok,usdeur]
    print(todays_prices)
    
if __name__ == "__main__":
    main()