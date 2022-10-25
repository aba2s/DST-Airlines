"""
Assurez-vous svp d'avoir une clé de l'API afin de pouvoir faire des requêtes.
Une documentation pour prendre en main l'outil est
`ici <https://airlabs.co/docs/>`_

Ces scripts sont disponible sur le dépôt `github
<https://github.com/aba2s/DST-Airlines/>`_
"""

import requests
import json
# import airportsdata
import os

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
    flights = response['response']

    with open("flights.json", "w") as fp:
        json.dump(flights, fp, indent=4)


# real_time_flights = flights_or_airlines(end_point[0])
# airlines = flights_or_airlines(end_point[1])


# ------------------------------------------------------------------------- #
#                 Extracting and loading all airports IATA code             #
# --------------------------------------------------------------------------#


'''
We need iata code to retrieve departure/arrival data by airport.
'''
# airports = airportsdata.load('IATA')  # key is IATA code
# iata = list(filter(
#   lambda x: airports[x]['subd'] == 'Ile-de-France', airports))
# iata = list(map(lambda x: airports[x]['iata'], airports))

# Let's take only 'CDG' and 'ORY' airports for departure data.
iata = ['CDG', 'ORY']

# ------------------------------------------------------------------------- #
#                 Extracting and loading airport's  data                    #
# --------------------------------------------------------------------------#


def depatures_or_arrivals_flights(endpoint, key):
    """
    Cette fonction permet de filter les vols au départ où à l'arrivée d'un
    aéroport. Il est essentiel de ne pas oublier le code de l'aérroport
    d'arrivée ou de départ.

    Parameters
    ----------
    endpoint       : chaine de caractère complétant la racine de l'url.
    key            : doit être, soit l'aéroport de départ «dep_iata», \
                     soit l'aéroport d'arrivée «arr_iata».

    Returns
    -------
    a json file containing real time flights data or airlines data.
    """

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
        json.dump(data, file, indent=4)
