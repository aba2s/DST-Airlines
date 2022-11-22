from django.shortcuts import render
from .models import Flights
import requests
import json
import os
import time
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import Search


# Read api_key from settings.json file.
settings_filename = os.path.join(
    os.path.abspath(''), 'settings.json')
if os.path.isfile(settings_filename):
    with open(settings_filename) as settings_file:
        settings = json.load(settings_file)
else:
    settings = dict()

params = {
    "api_key": settings["airlabs_api_key"]["api_key"]
}

url = "https://airlabs.co/api/v9/"
end_point = [
    "flights?",
    "airlines?",
    "schedules?"  # Departures or arrivals flights
]

# ------------------------------------------------------------------------- #
#                Extracting and loading flights's data                      #
#                Status: status: 'en-route', 'landed', 'scheduled'          #


def flights_or_airlines(endpoint):
    """
    Cette fonction retourne un fichier json des données de vols en temps réel
    ou des données sur les compagnies aériennes, selon l'argument.

    Parameters
    ----------
    endpoint       : chaine de caractère complétant la racine de l'url.

    Returns
    -------
    a json file containing real time flights data or airlines data.
    """
    request = requests.get(url + endpoint, params)
    response = request.json()
    flights = response['response']   # a list of dictionary object

    # with open("flights.json", "r") as f:
    #    flights = json.load(f)

    list_flights = []
    for flight in flights:
        flight_instance = Flights(
            hex=flight.get('hex', None),
            reg_number=flight.get('reg_number', None),
            flag=flight.get('flag', None),
            lat=flight.get('lat', None),
            lng=flight.get('lng', None),
            alt=flight.get('alt', None),
            dir=flight.get('dir', None),
            speed=flight.get('speed', None),
            v_speed=flight.get('v_speed', None),
            squaw=flight.get('squawk', None),
            flight_number=flight.get('flight_number', None),
            flight_icao=flight.get('flight_icao', None),
            flight_iata=flight.get('flight_iata', None),
            dep_icao=flight.get('dep_icao', None),
            dep_iata=flight.get('dep_iata', None),
            arr_icao=flight.get('arr_icao', None),
            arr_iata=flight.get('arr_iata', None),
            airline_icao=flight.get('airline_icao', None),
            airline_iata=flight.get('airline_iata', None),
            aircraft_icao=flight.get('aircraft_icao', None),
            updated=flight.get('updated', None),
            status=flight.get('status', None),

        )
        list_flights.append(flight_instance)

    # Bulk save data in the database
    Flights.objects.bulk_create(list_flights)


# Call the function for saving data
print("Process starting with flights data ...")
start = time.time()
flights_or_airlines(end_point[0])
end = time.time()
print("Deltatime: ", end-start)
print("Process finished with fligths data!\n")


def index(request):
    # Retrieve flights from the database
    flights = Flights.objects.all().values()
    flights_df = pd.DataFrame(flights)
    flights_df = flights_df[
        (flights_df["dep_iata"] == 'CDG')
        | (flights_df["dep_iata"] == 'ORY')
        | (flights_df["dep_iata"] == 'BVA')
        | (flights_df["arr_iata"] == 'CDG')
        | (flights_df["arr_iata"] == 'ORY')
        | (flights_df["arr_iata"] == 'BVA')
    ]

    geometry = gpd.points_from_xy(flights_df.lng, flights_df.lat)
    flights_gdf = gpd.GeoDataFrame(
        flights_df, geometry=geometry, crs="EPSG:4326")

    # Initialize the map
    lat = 48.8499198
    lng = 2.6370411

    # icon = folium.Icon(color="green", icon="fa-plane", prefix='fa')
    m = folium.Map(location=[lat, lng], zoom_start=6,
                   prefer_canvas=True, tiles='OpenStreetMap')

    # Create a GeoJson onject and display planes position
    icon = folium.Icon(icon_color='yellow', icon='fa-plane', prefix='fa')
    layer = folium.GeoJson(
        flights_gdf,
        marker=folium.Marker(icon=icon),
        tooltip=folium.GeoJsonTooltip(
            fields=[
                'flight_number', 'flight_iata', 'dep_iata', 'arr_iata',
                'airline_icao', 'aircraft_icao', 'status'
            ], localize=True),
                ).add_to(m)

    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)

    # Adding a seach navigation bar
    Search(
        layer=layer,
        geom_type="Point",
        placeholder="Search for a street",
        search_label="status",
        search_zoom=16,
        collapsed=True,
        position='topright').add_to(m)

    m.save(os.path.join(
        os.path.abspath(''), 'templates', 'index.html'))
    return render(request, 'index.html')
