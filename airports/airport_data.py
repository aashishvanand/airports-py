import gzip
import json
import os

# Load the gzipped data
data_path = os.path.join(os.path.dirname(__file__), 'data', 'airports.gz')
with gzip.open(data_path, 'rt') as f:
    AIRPORTS_DATA = json.load(f)

def get_airport_by_iata(iata_code):
    """Retrieve airport data by IATA code."""
    return [airport for airport in AIRPORTS_DATA if airport['iata'] == iata_code]

def get_airport_by_icao(icao_code):
    """Retrieve airport data by ICAO code."""
    return [airport for airport in AIRPORTS_DATA if airport['icao'] == icao_code]

def get_airport_by_city_code(city_code):
    """Retrieve airport data by city code."""
    return [airport for airport in AIRPORTS_DATA if airport['city_code'] == city_code]

def get_airport_by_country_code(country_code):
    """Retrieve airport data by country code."""
    return [airport for airport in AIRPORTS_DATA if airport['country_code'] == country_code]

def get_airport_by_continent(continent_code):
    """Retrieve airport data by continent."""
    return [airport for airport in AIRPORTS_DATA if airport['continent'] == continent_code]
