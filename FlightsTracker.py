#!/Users/Francis/Desktop/Python3.9/Training/venv/bin/python3
# -*- encoding: utf8 -*-
# Importation of Python libraries
import pandas as pd
from IPython.display import display
import requests
import urllib.request
import json
import ssl
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.layouts import column, row
from bokeh.client import push_session
from bokeh.models import HoverTool, WMTSTileSource, LinearColorMapper, LabelSet, Label
from bokeh.tile_providers import STAMEN_TERRAIN_RETINA, get_provider
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.server.server import Server
from bokeh.io import curdoc
import numpy as np
import folium
import os


# Header
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

# Provide your API key in the query string!!!

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read api_key from settings.json file.
settings_filename = os.path.join(BASE_DIR, 'settings.json')
if os.path.isfile(settings_filename):
    with open(settings_filename) as settings_file:
        settings = json.load(settings_file)
else:
    settings = dict()


params = {
    "api_key": settings["airlabs_api_key"]["api_key"]
}

end_point = [
    "flights?",
    "airlines?",
    "schedules?"
]

# Real time flight tracking:
api_base = 'http://airlabs.co/api/v9/'

# Load the JSON data into a JSON file:
api_result = requests.get(api_base+end_point[0], params)
api_response = api_result.json()
api_flights = api_response["response"]

with open("flights.json", "w") as fp:
    json.dump(api_flights, fp, indent=4, sort_keys=True)

# Load as JSON into a dataframe:
df = pd.read_json("flights.json")
# print with pandas
#display(df)

# Convert to Pandas Dataframe
flights_df = pd.DataFrame(df, columns = ['lat', 'lng', 'alt', 'flight_icao', 'dep_iata', 'arr_iata', 'airline_iata'])
display(flights_df)

# Convert France GPS coordinates to Web Mercator
x_range, y_range = ((-6.403614, 12.229198), (40.587984, 53.007425)) # FRANCE GPS coordinates location

# Convert All GPS coordinates to Web Mercator
def mercator(df, lat="lat", lon="lng"):
    radius = 6378137 # radius of the earth in meters
    df["x"] = df[lon] * (radius * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * radius
    return df

# Flights tracking main function
def flights_tracker(geo):
    # Bokeh column data source
    mercator_df = mercator(flights_df)
    flights_source = ColumnDataSource(mercator_df)
    display(flights_source)

    def streaming():
        # Map coordinates:
        # Objet MAP: https://docs.bokeh.org/en/latest/docs/reference/tile_providers.html
        map = figure(tools = 'pan, zoom_in, zoom_out, wheel_zoom, reset, save',
        x_range = x_range, y_range = y_range, x_axis_type = 'mercator',
          y_axis_type = 'mercator', sizing_mode = 'scale_width', plot_height = 300)

        # Add planes geolocalisation and informative labels object:
        infos = HoverTool()
        infos.tooltips = [('Flight', '@flight_icao'), ('Altitude', '@alt'),
         ('Departure', '@dep_iata'), ('Arrival', '@arr_iata'), ('Airline', '@airline_iata')]
        labels = LabelSet(x = 'x', y = 'y', text = 'flight_icao', level = 'glyph', x_offset = 5,
         y_offset = 5, source = flights_source, render_mode = 'canvas',
         background_fill_color = 'skyblue', text_color = 'black', text_font_size = '8pt')

        # Add the WMTS tile source to the map object:
        map_provider = (get_provider(STAMEN_TERRAIN_RETINA))
        map.add_tile(map_provider) # bokeh.tile_providers.StamenTerrainRetina
        map.add_tools(infos)
        map.circle('x', 'y', source = flights_source, fill_color = "blue", size = 10, fill_alpha = 0.8, line_width = 0.5)
        map.add_layout(labels)

        curdoc().title = "Flights Tracker"
        curdoc().add_root(map())
        session = push_session(curdoc())
        session.show()

#Display the Map in the browser:
#show(map)

# Server initialization for Bokeh Application (Flights Tracker) on port 48010:
# To run through bash terminal: bokeh serve --show FlightsTracker.py
apps = {'/': Application(FunctionHandler(flights_tracker))}
server = Server(apps, port=48010) # Any unassigned port will do
server.io_loop.start()
