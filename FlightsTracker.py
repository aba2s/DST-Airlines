#IMPORT LIBRARY
from pprint import pprint
import pandas as pd
from IPython.display import display
import requests
import urllib.request
import json
import ssl
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.tile_providers import STAMEN_TONER
import numpy as np

# Header
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

# Provide your API key in the query string:
params = {
  'api_key': '9d2955c1-020a-4343-a6d7-c2f04450735b'
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

#Load as JSON into a dataframe:
df = pd.read_json("flights.json")
# print with pandas
#display(df)

#Convert to Pandas Dataframe
flight_df = pd.DataFrame(df, columns = ['lat', 'lng', 'alt', 'dep_iata', 'arr_iata', 'airline_iata'])
display(flight_df)
"""# Define country coordinate range with Mercator method (EPSG:3857)
x_range,y_range=([-15187814,-6458032], [2505715,6567666])

#Function to convert coordinate to web Mercator
def wgs84_to_web_mercator(df, lon="Long", lat="Lat"):
    k = 6378137
    df["x"] = df[lon] * (k * np.pi/180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
    return df
wgs84_to_web_mercator(flight_df)

#Bokeh column data source
flight_source=ColumnDataSource(flight_df)

#Setup figure
p=figure(x_range=x_range,y_range=y_range,x_axis_type='mercator',y_axis_type='mercator',
  sizing_mode='scale_width',plot_height=300)
p.add_tile(STAMEN_TONER)
p.circle('x','y',source=flight_source,fill_color="blue",size=10,fill_alpha=0.8,line_width=0.5)

#Display figure
show(p)"""