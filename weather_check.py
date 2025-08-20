import requests
from datetime import datetime, timedelta
from geopy.distance import geodesic


def rainfall_by_postcode(postcode):
    #Get lang and long via postcode
    geo = requests.get(f"https://api.postcodes.io/postcodes/{postcode}").json()
    lat = geo["result"]["latitude"]
    lon = geo["result"]["longitude"]

    print(lat, " ", lon)
    print(type(lat))
    #Use lang and long to find rainfall over past x amount of time

    end = datetime.time
    start, end = get_times()
    past_days = 7
    url = "https://environment.data.gov.uk/flood-monitoring/id/stations"
    params = {"parameter": "rainfall"}
    # Find nearest station
    
    response = requests.get(url, params=params).json()

    nearest_station = get_nearest_station(lat, lon, response["items"])

    print(nearest_station)
    station_id = nearest_station["@id"]
    print(station_id)
    # Get date 5 days ago in ISO8601 format
    since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Build readings URL
    readings_url = f"{station_id}/readings"
    params = {"parameter": "rainfall", "since": since_date}

    response = requests.get(readings_url, params=params)
    data = response.json()
    print(data["items"][0]["value"])
    total_rain = 0
    for hour in data["items"]:
        print(hour)
        rain_by_hour = hour["value"]
        total_rain += rain_by_hour
    print("Total rain", total_rain)
    #average_mm = total_mm / len(rain)

    print(average_mm)
    
    
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

#Get nearest station to lat and lon
def get_nearest_station(origin_lat, origin_lon, stations):
    closest_lat = 0
    closest_lon = 0
    closest_station = 0
    #Search each station and save the closest
    for station in stations:
        try:
            if (station["lat"]):
                if (origin_lat - station["lat"] < origin_lat - closest_lat) and (origin_lon - station["long"] < origin_lon - closest_lon):
                    closest_lat = station["lat"]
                    closest_lon = station["long"]
                    closest_station = station
        except:
            print(station["@id"], "has no lat")
            

    print(closest_station)
    return closest_station




by_hour = rainfall_by_postcode("LS29 7Sy")



print(by_hour)