import requests
from datetime import datetime, timedelta
from geopy.distance import geodesic

rock_dict = {"sandstone": [3, 2], "limestone": [1, 5], "granite": [0, 5], "gritstone": [3, 2], "slate": [1, 4], "chalk": [2, 2]}


def rainfallByLatLon(lat,lon, rock_type):
    #Use lat and lon to find rainfall over past x amount of time

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&forecast_days=16&hourly=precipitation&timezone=Europe/London"
    weather = requests.get(url).json()
    #weather["hourly"]["precipitation"][:24 + past_days*24] gets only data from current day and last (past_days)
    rain = weather["hourly"]["precipitation"]
    total_mm = 0
    hour_count = 0
    rain_list = [] #List of total rain per day
    for mm in rain:
        hour_count += 1
        total_mm += mm
        if hour_count > 24: #Get total rain for each day
            rain_list.append(total_mm)
            total_mm = 0
            hour_count = 0
    #Add rain count to rainlist
    rain_list.append(total_mm)
    climbDays(rock_type, rain_list)
    

def getLatLon(postcode):
    #Get lang and long via postcode
    geo = requests.get(f"https://api.postcodes.io/postcodes/{postcode}").json()
    if geo["status"] == 200: #If valid postcode, return the lat and lon code
        lat = geo["result"]["latitude"]
        lon = geo["result"]["longitude"]
        return lat, lon
    else:
        return None, None

#Climb logic
def climbDays(rock_type, rain_list):
    #Convert to lower case for formatting
    rock_type = rock_type.lower()
    results_list = []
    if rock_type in rock_dict:
        days_needed = rock_dict[rock_type][0] #Days needed to know whether a rock is climable
        rainfall_max = rock_dict[rock_type][1] #Maximum amount of rain that can occur before not climable
        #For every day of rainfall after the minimum number of days to check
        for r in range(days_needed, len(rain_list)):
            #For every previous days required to check
            climb = True #Flag
            for pr in range(r-days_needed, r):
                if rain_list[pr] > rainfall_max: #If rainfall in any of the last (days_needed) days exceeds max rainfall, flag false
                    climb = False
            if climb == True:
                date = datetime.now() + timedelta(days=r) #Get date when you can climb
                date = date.strftime("%d-%m-%Y") #Reformat date
                results_list.append(date) #Append climable date
    print("You can climb on any of these upcoming dates:\n", *results_list)

def getInput():
    valid_postcode = False
    valid_rock_type = False 
    #Rock Flags
    #Gather lat and lon from postcode
    while valid_postcode == False:
        postcode = input("Enter postcode: ")
        lat, lon = getLatLon(postcode)
        if lat != None and lon != None:
            valid_postcode = True
        else: 
            print("Invalid postcode, please try again")
    #Get rock type
    while valid_rock_type == False:
        rock_type = input("Enter rock type, or enter list for a list of all rock types in the system: ")
        if rock_type == "list": #Provide list of rock types for user
            print(rock_dict.keys())
        elif rock_type in rock_dict: #If rock type is valid
            rainfallByLatLon(lat, lon, rock_type)
            valid_rock_type = True # Ensure no more looping after service
        else:
            print("Invalid rock type")

getInput()
