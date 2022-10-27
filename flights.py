import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import Search


df = pd.read_json("flights.json")
df = df[(df["dep_iata"] == 'CDG') | (df["dep_iata"] == 'ORY')
        | (df["arr_iata"] == 'CDG') | (df["arr_iata"] == 'ORY')]

geometry = gpd.points_from_xy(df.lng, df.lat)  # Longitude, latitude
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Initialize the map
# lat = gdf["geometry"][0].y
# lng = gdf["geometry"][0].x
lat = 48.8499198
lng = 2.6370411

# icon = folium.Icon(color="green", icon="fa-plane", prefix='fa')
m = folium.Map(location=[lat, lng], zoom_start=6, prefer_canvas=True,
               tiles='OpenStreetMap')

# Create a GeoJson onject and display planes position
icon = folium.Icon(icon_color='yellow', icon='fa-plane', prefix='fa')
layer = folium.GeoJson(
    gdf,
    marker=folium.Marker(icon=icon),
    tooltip=folium.GeoJsonTooltip(
        fields=[
            'flight_number', 'flight_iata', 'dep_iata', 'arr_iata',
            'airline_icao', 'aircraft_icao', 'status'
        ], localize=True),
            ).add_to(m)

# Adding a seach navigation bar
Search(
    layer=layer,
    geom_type="Point",
    placeholder="Search for a street",
    search_label="status",
    search_zoom=16,
    collapsed=True,
    position='topright').add_to(m)
m.save('index.html')
