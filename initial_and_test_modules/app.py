import requests
import json
import folium
from linked_list import Set
import html
from folium.features import DivIcon

user_key = 'SSqPdQ5xLbF6dwN2'
event_location = 'New York'
page_size = 250
sort_order = 'popularity'
sort_direction = 'descending'
start_date = 20190416
end_date = 20190430
url = "http://api.eventful.com/json/events/search?"
url += "&app_key={}".format(user_key)
url += "&location={}".format(event_location)
url += "&date={}00-{}00".format(start_date, end_date)
url += "&page_size={}".format(page_size)
url += "&sort_order={}".format(sort_order)
url += "&sort_direction={}".format(sort_direction)


def get_data(url):
    '''Gets data from API to json'''
    response = requests.get(url)
    data = response.content.decode()
    data = json.loads(data)
    with open('data/data.json', 'w') as file:
        json.dump(data, file)


get_data(url)


def events():
    '''
    Returns the list of dictionaries.
    :return: list
    '''
    with open('data/data.json', 'r') as file:
        temp = json.load(file)
    return temp['events']['event']


class Event:
    '''Class for Event representation'''

    def __repr__(self):
        '''
        String representation of Event
        :return:str
        '''
        return '<<<{}({}, {})>>>'.format(self.title, self.city_name, self.start_time)


def factory():
    """
    Adds attributes to Event object and creates list including them.
    :return: Set
    """
    x = Set()
    for event in events():
        obj = Event()
        for i in event:
            if i in ["id", "title", "start_time", "city_name", "latitude", "longitude", "url", "image"]:
                obj.__dict__[i] = event[i]
        x.add(obj)
    return x


# print(factory().get())


class Map:
    '''Class for Map representation'''

    def __init__(self, marker_color, zoom_start):
        '''
        Initialises a class Map
        :param marker_color: str
        :param zoom_start: int
        '''
        self.marker_color = marker_color
        self.zoom = zoom_start

    def draw(self, linked_list):
        '''
        Draw a map.
        :param linked_list:Set
        '''
        event = factory().head.data
        m = folium.Map(location=[float(event.latitude), float(event.longitude)], zoom_start=self.zoom)
        node = linked_list.head
        name_layer = folium.FeatureGroup(name='names')
        location_layer = folium.FeatureGroup(name='locations')
        while node is not None:
            location_layer.add_child(folium.Marker([float(node.getData().latitude), float(node.getData().longitude)],
                                                   icon=folium.Icon(color=self.marker_color),
                                                   popup=node.getData().title))
            name_layer.add_child(folium.Marker([float(node.getData().latitude), float(node.getData().longitude)],
                                               icon=DivIcon(icon_size=(130, 120), icon_anchor=(0, 0),
                                                            html='<div style="font-size: 10pt"><B><a href = "' + node.getData().url + '" >{}</a></B></div>'.format(
                                                                html.escape(node.getData().title[0]))), ))
            node = node.getNext()
        m.add_child(name_layer)
        m.add_child(location_layer)
        folium.LayerControl().add_to(m)
        m.save('templates/map.html')


fact = factory()
fact.get()
Map("red", 12).draw(fact)
fact.remove_all()
print(len(fact))
