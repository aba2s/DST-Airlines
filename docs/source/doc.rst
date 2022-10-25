Bienvenue à la documentation DST Airlines !
===========================================

Context
-------
De nos jours, on est capable d’avoir des informations sur les vols dans le monde entier et de traquer en temps réel un avion. Nous pouvons observer `ce site <https://www.flightradar24.com/>`_
en guise d’exemple. La technologie de contrôle du trafic aérien profite non seulement à la sécurité du trafic, mais également aux particuliers qui souhaitent consulter des données en temps
réel sur un vol. Grâce au suivi des vols, les citoyens peuvent mieux s'orienter 'ils doivent respecter des rendez-vous professionnels, ou privés et  ainsi leur emploi du temps.
Avec la généralisation des transpondeurs  type ADS-B, il est désormais possible d'effectuer le traitement des données par satellite. On peut donc interroger toutes les données de vol importantes en
temps réel et les afficher sur un terminal, qu'il s'agisse d'un téléphone ou de tout autre type d'écran. Fort de ce constat, Nous pensons qu'une application permettant de suivre les vols d'avions
en temps réel constitue une offre pertinente pour le grand public.  L'objectif de ce projet est donc de développer une application (API) de suivi de vols d'avions commerciaux en temps réel.
Nous travaillerons avec l'API AirLabs pour récupérer les données de vols dont nous avons besoin.

AirLabs API
-----------
AirLabs recueille des données à partir de milliers de sources, les nettoie, les agrége et les organise en collections complètes qui permettent aux développeurs de créer
des produits innovants et d'offrir une expérience utilisateur parfaite. L'API AirLabs Data est conçue pour fournir un moyen simple d'obtenir des données de positionnement
de vol mondial en temps réel, des horaires de vol et un ensemble impressionnant de compagnies aériennes, d'itinéraires, d'aéroports et d'autres informations pertinentes
liées à l'aviation. Les requêtes à l'API REST sont effectuées à l'aide de requêtes HTTP et les réponses sont fournies dans un format JSON, XML ou CSV léger. La documentation
de l'API peut être utilisée pour n'importe quel langage de programmation majeur et fournit des directives générales pour l'intération et des explications sur les points de
terminaison de l'API, les paramètres de requête et les objets de réponse. Pour une prise de main vous pouvez consulter sur le site, `ici <https://airlabs.co/docs//>`_

.. admonition:: Important

    La dernière version de l'API est la v9. C'est celle que nous utilisons ici. Veuillez toujours utiliser la dernière version avec chaque appel d'API.


Jeu de données utilisé
-----------------------
Les données utilisées sont stockées dans des fichiers au format JSON répartis dans quatre collections ci-dessous.

* **Flights**

.. list-table:: Real-Time Flights Data
   :header-rows: 1
   :stub-columns: 0

   * - Parameter
     - Description
   * - hex
     - ICAO24 Hex address.
   * - reg_number
     - Aircraft Registration Number
   * - flag
     - ISO 2 country code from Countries DB. Available in the Free plan.
   * - lat
     - Aircraft Geo-Latitude for now. Available in the Free plan.
   * - lng
     - Aircraft Geo-Longitude for now. Available in the Free plan.
   * - alt
     - Aircraft elevation for now (meters).
   * - dir
     - Aircraft head direction for now. Available in the Free plan.
   * - speed
     - Aircraft horizontal speed (km) for now.
   * - v_speed
     - Aircraft vertical speed (km) for now.
   * - squawk
     - Aircraft squawk signal code.
   * - airline_icao
     - Airline ICAO code.
   * - airline_iata
     - Airline IATA code.
   * - icao
     - Aircraft ICAO type. Available in the Free plan.
   * - flight_icao
     - Flight ICAO code-number.
   * - flight_iata
     - Flight IATA code-number.
   * - flight_number
     - Flight number only.
   * - dep_icao
     - Departure Airport ICAO code.
   * - dep_iata
     - Departure Airport IATA code. Available in the Free plan.
   * - arr_icao
     - Arrival Airport ICAO code.
   * - arr_iata
     - Arrival Airport IATA code.
   * - updated
     - UNIX timestamp of last aircraft signal.
   * - status
     - Current flight status - scheduled, en-route, landed.


* **Airlines**

.. list-table:: Arlines Data
   :header-rows: 1
   :stub-columns: 0

   * - Parameter
     - Description
   * - name
     - Airline name.
   * - icao_code
     - Airline ICAO code.
   * - iata_code
     - Airline IATA code.

* **Departures**

.. list-table:: Flights Departures Data
   :header-rows: 1
   :stub-columns: 0

   * - Parameter
     - Description
   * - airline_iata
     - Airline IATA code. Available in the Free plan.
   * - airline_icao
     - Airline ICAO code.
   * - flight_iata
     - Flight IATA code-number. Available in the Free plan..
   * - flight_icao
     - Flight ICAO code-number.
   * - flight_number
     - Flight number only. Available in the Free plan.
   * - cs_airline_iata
     - Codeshared airline IATA code.
   * - cs_flight_iata
     - Codeshared flight IATA code-number.
   * - cs_flight_number
     - Codeshared flight number.
   * - dep_iata
     - Departure airport IATA code. Available in the Free plan.
   * - dep_icao
     - Departure airport ICAO code.
   * - dep_terminal
     - Estimated departure terminal.
   * - dep_gate
     - Estimated departure gate.
   * - dep_time
     - Departure time in the airport time zone. Available in the Free plan.
   * - dep_time_ts
     - Departure UNIX timestamp.
   * - dep_time_utc
     - Departure time in UTC time zone.

* **Arrivals**

.. list-table:: Flights Arrivals Data
   :header-rows: 1
   :stub-columns: 0

   * - Parameter
     - Description
   * - airline_iata
     - Airline IATA code. Available in the Free plan.
   * - airline_icao
     - Airline ICAO code.
   * - flight_iata
     - Flight IATA code-number. Available in the Free plan..
   * - flight_icao
     - Flight ICAO code-number.
   * - flight_number
     - Flight number only. Available in the Free plan.
   * - cs_airline_iata
     - Codeshared airline IATA code.
   * - cs_flight_iata
     - Codeshared flight IATA code-number.
   * - cs_flight_number
     - Codeshared flight number.
   * - dep_iata
     - Departure airport IATA code. Available in the Free plan.
   * - dep_icao
     - Departure airport ICAO code.
   * - dep_terminal
     - Estimated departure terminal.
   * - dep_gate
     - Estimated departure gate.
   * - dep_time
     - Departure time in the airport time zone. Available in the Free plan.
   * - dep_time_ts
     - Departure UNIX timestamp.
   * - dep_time_utc
     - Departure time in UTC time zone.
