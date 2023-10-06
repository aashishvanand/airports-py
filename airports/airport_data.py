import gzip
import json
import os

# Load the gzipped JSON data
with gzip.open(os.path.join(os.path.dirname(__file__), 'airports.gz'), 'rt') as f:
    airports = json.load(f)

def get_airport_by_iata(iata_code):
    if len(iata_code) != 3:
        raise ValueError("Invalid IATA format. Please provide a 3-letter uppercase code, e.g., 'AAA'.")
    return [airport for airport in airports if airport["iata"] == iata_code.upper()]

def get_airport_by_icao(icao_code):
    if len(icao_code) != 4:
        raise ValueError("Invalid ICAO format. Please provide a 4-letter uppercase code, e.g., 'VOMM'.")
    return [airport for airport in airports if airport["icao"] == icao_code.upper()]

def get_airport_by_city_code(city_code):
    results = [airport for airport in airports if airport["city_code"] == city_code.upper()]
    if not results:
        raise ValueError(f"No airport found with city code: {city_code}")
    return results

def get_airport_by_country_code(country_code):
    results = [airport for airport in airports if airport["country_code"] == country_code.upper()]
    if not results:
        raise ValueError(f"No airport found with country code: {country_code}")
    return results

def get_airport_by_continent(continent):
    results = [airport for airport in airports if airport["continent"] == continent.upper()]
    if not results:
        raise ValueError(f"No airport found in continent: {continent}")
    return results
