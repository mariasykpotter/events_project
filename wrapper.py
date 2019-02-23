import eventful

api = eventful.API('FTcN9qrSkd47hmpr')

events = api.call('/events/search', q='', l='London')
for event in events['events']['event']:
    print (event["url"],event["city_name"],event["longitude"],event["country_name"],event["start_time"], event["description"], event["performers"],event["venue_address"], event["title"])
