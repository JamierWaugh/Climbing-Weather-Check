import requests
from datetime import datetime, timedelta


def rainfall_by_postcode(postcode):
    #Get lang and long via postcode
    geo = requests.get(f"https://api.postcodes.io/postcodes/{postcode}").json()
    lat = geo["result"]["latitude"]
    lon = geo["result"]["longitude"]
    print(lat, " ", lon)
    #Use lang and long to find rainfall over past x amount of time

    end = datetime.time
    start, end = get_times()
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&past_days=3&hourly=precipitation&timezone=Europe/London"
    weather = requests.get(url).json()
    print(weather)
    
def get_times():
    #Get end of range (today)
    now = datetime.now() - timedelta(days=1)
    now_iso = now.strftime("%Y-%m-%d")
    print(now_iso)
    #Get start of range (three days ago)
    days_ago = now - timedelta(days=5)
    days_ago_iso = days_ago.strftime("%Y-%m-%d")
    print(days_ago_iso)
    return days_ago_iso, now_iso


by_hour = rainfall_by_postcode("LS29 7Sy")



print(by_hour)