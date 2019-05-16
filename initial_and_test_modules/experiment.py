import requests
import json


def event_json():
    user_key = 'SSqPdQ5xLbF6dwN2'
    event_location = 'New Delhi'
    start_date = 20190516
    end_date = 20190530
    url = "http://api.eventful.com/json/events/search?"
    url += "&app_key={}".format(user_key)
    url += "&location={}".format(event_location)
    url += "&date={}00-{}00".format(start_date, end_date)
    url += '&page_size=10'
    url += '&page_number=1'
    response = requests.get(url)
    data = response.json()['events']['event']
    # data = json.loads(data)
    with open('data/data.json', 'w') as file:
        json.dump(data, file)
    return


print(event_json())

