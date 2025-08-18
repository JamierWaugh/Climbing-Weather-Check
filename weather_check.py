import requests


def rainfall_by_postcode(postcode):
    #Get lang and long via postcode
    geo = requests.get(f"https://api.postcodes.io/postcodes/{postcode}").json()
    lang = geo["result"]["langitude"]
    long = geo["result"]["longitude"]
    #Use lang and long to find rainfall over past x amount of time