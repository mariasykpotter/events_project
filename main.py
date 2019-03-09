import json
import requests
import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
import html
from folium.features import DivIcon

start_year, start_month, start_day = [int(x) for x in input().split()]
map_color = input()
geolocator = Nominatim(
    user_agent="Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
# today_date = datetime.today()
# print(today_date)
event_date = datetime.date(start_year, start_month, start_day)
date = str(event_date)
user_key = "FTcN9qrSkd47hmpr"
event_location = "London"
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
coordinates = geolocator.geocode(event_location)
print(coordinates.latitude, coordinates.longitude)
f1 = open("demofile1.json", "w+")
url = "http://api.eventful.com/json/events/search?"
url += "&app_key=" + user_key
url += "&location=" + event_location
url += "&date=" + date
print(url)
data1 = requests.get(url).json()
print(data1)
json.dump(data1, f1)
count = 0
m = folium.Map(location=(coordinates.latitude, coordinates.longitude))
name_layer = folium.FeatureGroup(name='names')
location_layer = folium.FeatureGroup(name='locations')
for el in data1["events"]["event"]:
    if el["start_time"].split()[0] == str(event_date):
        count += 1
        print(el["title"])
        print(el["latitude"], el["longitude"])
        location_layer.add_child(
            folium.Marker(location=[float(el["latitude"]), float(el["longitude"])], popup=el["title"],
                          icon=folium.Icon(icon="leaf", color=map_color)))
        name_layer.add_child(folium.Marker([float(el["latitude"]), float(el["longitude"])],

                                           icon=DivIcon(icon_size=(130, 120), icon_anchor=(0, 0),

                                                        html='<div style="font-size: 10pt"><B><a href = "' + el[
                                                            "url"] + '" >{}</a></B></div>'.format(

                                                            html.escape(el["title"]))), ))
m.add_child(name_layer)
m.add_child(location_layer)
folium.LayerControl().add_to(m)
m.save('Map.html')

