import requests

# https://blog.teclado.com/how-to-interact-with-apis-using-python/

APP_ID = "e7b40bcecb8f45429f218a098dacb1cd"
ENDPOINT = "https://openexchangerates.org/api/latest.json"

# Make a get request for the latest currency exchange rates
response = requests.get(f"{ENDPOINT}?app_id={APP_ID}")
exchange_rates = response.json()

# Use exchage rate data to perform USD to GBP conversion
usd_amount = 1000
gbp_amount = usd_amount * exchange_rates['rates']['GBP']
print(f"USD{usd_amount} is GBP{gbp_amount}")
