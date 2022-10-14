import requests
import json
import airportsdata
import os


'''
Please make sure to get a valid api key to retrieve data from airlabs
Complete documentation could be found --> https://airlabs.co/docs/flights

To use this scrip please set up a virutual environement and install
the requirements.txt file
'''

# Build paths inside the project like this: BASE_DIR / 'subdir'.
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

url = "https://airlabs.co/api/v9/"
end_point = [
    "flights?",
    "airlines?",
    "schedules?"
]
# ------------------------------------------------------------------------- #
#                Extracting and loading flights's data                      #
#                Status: status: 'en-route', 'landed', 'scheduled'          #
# --------------------------------------------------------------------------#

flights_request = requests.get(url + end_point[0], params)
flights_request = flights_request.json()
flights = flights_request['response']

with open("flights.json", "w") as fp:
    json.dump(flights, fp)

# ------------------------------------------------------------------------- #
#                Extracting and loading airline's data                      #
# --------------------------------------------------------------------------#

airlines_request = requests.get(url + end_point[1], params)
airlines_request = airlines_request.json()
airlines = airlines_request["response"]

with open("airlines.json", "w") as file:
    json.dump(airlines, file)

# ------------------------------------------------------------------------- #
#                 Extracting and loading all airports IATA code             #
# --------------------------------------------------------------------------#
'''
We need iata code to retrieve departure/arrival data by airport.
'''
airports = airportsdata.load('IATA')  # key is IATA code
# iata = list(filter(
#   lambda x: airports[x]['subd'] == 'Ile-de-France', airports))
# iata = list(map(lambda x: airports[x]['iata'], airports))

# Let's take only 'CDG' and 'ORY' airports for departure data.
iata = ['CDG', 'ORY']
# ------------------------------------------------------------------------- #
#                 Extracting and loading airport's  data                    #
# --------------------------------------------------------------------------#
data = []
for code in iata:
    params_airport = {
        "api_key": settings["airlabs_api_key"]["api_key"],
        "dep_iata": code
    }
    departure_flights_request = requests.get(
        url + end_point[2], params_airport)
    departure_flights_request = departure_flights_request.json()
    departure_flights = departure_flights_request["response"]
    data.append(departure_flights)

    with open("departure_flights.json", "w") as file:
        json.dump(data, file)
