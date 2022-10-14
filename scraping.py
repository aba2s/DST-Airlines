import requests
import json
import airportsdata

'''
/!\ Please make sure to get a valid api key to retrieve data from airlabs
Complete documentation could be found --> https://airlabs.co/docs/flights

To use this scrip please set up a virutual environement and install
the requirements.txt file
'''

params = {
    "api_key": "you_api_key"
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
# airports = airportsdata.load('IATA')  # key is IATA code
# This part will be completed in next days

# ------------------------------------------------------------------------- #
#                 Extracting and loading airport's  data                    #
# --------------------------------------------------------------------------#

params_airport ={
    "api_key": "you_api_key",
    "dep_iata": "JFK"
}
departure_flights_request = requests.get(url + end_point[2], params_airport)
departure_flights_request = departure_flights_request.json()
departure_flights = departure_flights_request["response"]

with open("departure_flights.json", "w") as file:
    json.dump(departure_flights, file)
