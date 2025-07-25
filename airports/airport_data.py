import gzip
import json
import os
import math
from typing import List, Dict, Any, Optional, Union

# Load the gzipped JSON data from the data directory
data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'airports.gz')
with gzip.open(data_file_path, 'rt') as f:
    airports = json.load(f)

def _validate_regex(data: str, pattern: str, error_message: str) -> None:
    """
    Validates a string against a pattern and raises an error if it doesn't match.
    
    Args:
        data: The data to validate
        pattern: The pattern to test against (simplified regex patterns)
        error_message: The error message to raise if validation fails
    
    Raises:
        ValueError: If the data does not match the pattern
    """
    import re
    # Convert to uppercase for validation to make it case-insensitive
    if not re.match(pattern, data.upper()):
        raise ValueError(error_message)

def _get_airport_by_code(code: str) -> Optional[Dict[str, Any]]:
    """
    Helper function to get an airport by either IATA or ICAO code.
    
    Args:
        code: A 3-letter IATA or 4-character ICAO code
    
    Returns:
        The first matching airport object, or None
    """
    if not isinstance(code, str):
        return None
    
    code = code.upper()
    
    # Validate and filter based on IATA code format (3 uppercase letters)
    if len(code) == 3 and code.isalpha():
        results = [airport for airport in airports if airport.get("iata") == code]
        return results[0] if results else None
    
    # Validate and filter based on ICAO code format (4 uppercase letters/numbers)
    if len(code) == 4 and code.isalnum():
        results = [airport for airport in airports if airport.get("icao") == code]
        return results[0] if results else None
    
    return None

def get_airport_by_iata(iata_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 3-letter IATA code.
    
    Args:
        iata_code: The IATA code of the airport to find (e.g., 'AAA')
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If the IATA code format is invalid or if no data is found
    """
    _validate_regex(iata_code, r'^[A-Z]{3}$', "Invalid IATA format. Please provide a 3-letter uppercase code, e.g., 'AAA'.")
    results = [airport for airport in airports if airport.get("iata") == iata_code.upper()]
    if not results:
        raise ValueError(f"No data found for IATA code: {iata_code}")
    return results

def get_airport_by_icao(icao_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 4-character ICAO code.
    
    Args:
        icao_code: The ICAO code of the airport to find (e.g., 'NTGA')
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If the ICAO code format is invalid or if no data is found
    """
    _validate_regex(icao_code, r'^[A-Z0-9]{4}$', "Invalid ICAO format. Please provide a 4-character uppercase code, e.g., 'NTGA'.")
    results = [airport for airport in airports if airport.get("icao") == icao_code.upper()]
    if not results:
        raise ValueError(f"No data found for ICAO code: {icao_code}")
    return results

def get_airport_by_city_code(city_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their city code.
    
    Args:
        city_code: The city code to search for
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If no airport found with the city code
    """
    results = [airport for airport in airports if airport.get("city_code") == city_code.upper()]
    if not results:
        raise ValueError(f"No airport found with city code: {city_code}")
    return results

def get_airport_by_country_code(country_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 2-letter country code.
    
    Args:
        country_code: The country code to search for (e.g., 'US')
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If the country code format is invalid or if no data is found
    """
    _validate_regex(country_code, r'^[A-Z]{2}$', "Invalid Country Code format. Please provide a 2-letter uppercase code, e.g., 'US'.")
    results = [airport for airport in airports if airport.get("country_code") == country_code.upper()]
    if not results:
        raise ValueError(f"No data found for Country Code: {country_code}")
    return results

def get_airport_by_continent(continent_code: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their 2-letter continent code.
    
    Args:
        continent_code: The continent code to search for (e.g., 'AS' for Asia)
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If the continent code format is invalid or if no data is found
    """
    _validate_regex(continent_code, r'^[A-Z]{2}$', "Invalid Continent Code format. Please provide a 2-letter uppercase code, e.g., 'AS'.")
    results = [airport for airport in airports if airport.get("continent") == continent_code.upper()]
    if not results:
        raise ValueError(f"No data found for Continent Code: {continent_code}")
    return results

def search_by_name(query: str) -> List[Dict[str, Any]]:
    """
    Searches for airports by their name. Case-insensitive.
    
    Args:
        query: The name or partial name to search for (e.g., "Heathrow")
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If search query is less than 2 characters
    """
    if not isinstance(query, str) or len(query) < 2:
        raise ValueError("Search query must be at least 2 characters long.")
    
    lower_case_query = query.lower()
    results = [
        airport for airport in airports 
        if airport.get("airport", "").lower().find(lower_case_query) != -1
    ]
    return results

def find_nearby_airports(lat: float, lon: float, radius_km: float = 100) -> List[Dict[str, Any]]:
    """
    Finds airports within a specified radius (in kilometers) of a given latitude and longitude.
    
    Args:
        lat: The latitude of the center point
        lon: The longitude of the center point
        radius_km: The search radius in kilometers (defaults to 100)
    
    Returns:
        A list of airports within the radius
    """
    R = 6371  # Radius of the Earth in kilometers
    
    def to_rad(value):
        return (value * math.pi) / 180
    
    results = []
    for airport in airports:
        # Use 'latitude' and 'longitude' and ensure they exist
        if not airport.get("latitude") or not airport.get("longitude"):
            continue
        
        try:
            # Convert string coordinates to numbers before calculating
            airport_lat = float(airport["latitude"])
            airport_lon = float(airport["longitude"])
            
            d_lat = to_rad(airport_lat - lat)
            d_lon = to_rad(airport_lon - lon)
            a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
                 math.cos(to_rad(lat)) * math.cos(to_rad(airport_lat)) *
                 math.sin(d_lon / 2) * math.sin(d_lon / 2))
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
            
            if distance <= radius_km:
                results.append(airport)
        except (ValueError, TypeError):
            continue
    
    return results

def get_airports_by_type(airport_type: str) -> List[Dict[str, Any]]:
    """
    Finds airports by their type (e.g., 'large_airport', 'medium_airport', 'small_airport', 'heliport', 'seaplane_base').
    
    Args:
        airport_type: The type of airport to filter by
    
    Returns:
        A list of matching airport objects
    
    Raises:
        ValueError: If the type is not a non-empty string
    """
    if not isinstance(airport_type, str) or len(airport_type) == 0:
        raise ValueError("Invalid type provided.")
    
    lower_case_type = airport_type.lower()
    results = []
    
    for airport in airports:
        if not airport.get("type"):
            continue
        
        airport_type_lower = airport["type"].lower()
        
        # Exact match first
        if airport_type_lower == lower_case_type:
            results.append(airport)
        # Allow partial matching for convenience (e.g., 'airport' matches 'large_airport')
        elif lower_case_type == 'airport' and 'airport' in airport_type_lower:
            results.append(airport)
    
    return results

def calculate_distance(code1: str, code2: str) -> Optional[float]:
    """
    Calculates the great-circle distance between two airports using their IATA or ICAO codes.
    
    Args:
        code1: The IATA or ICAO code of the first airport
        code2: The IATA or ICAO code of the second airport
    
    Returns:
        The distance in kilometers, or None if an airport is not found
    """
    airport1 = _get_airport_by_code(code1)
    airport2 = _get_airport_by_code(code2)
    
    if not airport1 or not airport2:
        return None
    
    try:
        R = 6371  # Radius of the Earth in kilometers
        
        def to_rad(value):
            return (value * math.pi) / 180
        
        lat1 = float(airport1["latitude"])
        lon1 = float(airport1["longitude"])
        lat2 = float(airport2["latitude"])
        lon2 = float(airport2["longitude"])
        
        d_lat = to_rad(lat2 - lat1)
        d_lon = to_rad(lon2 - lon1)
        
        a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
             math.cos(to_rad(lat1)) * math.cos(to_rad(lat2)) *
             math.sin(d_lon / 2) * math.sin(d_lon / 2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    except (ValueError, TypeError, KeyError):
        return None

def get_autocomplete_suggestions(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Provides a list of airports for autocomplete suggestions based on a query.
    It searches by airport name, city, and IATA code.
    
    Args:
        query: The partial query string from the user
        limit: Maximum number of results to return (defaults to 10)
    
    Returns:
        A list of matching airports (limited to specified number)
    """
    if not isinstance(query, str) or len(query) < 2:
        return []
    
    lower_case_query = query.lower()
    results = []
    
    for airport in airports:
        if (airport.get("airport", "").lower().find(lower_case_query) != -1 or
            airport.get("iata", "").lower().find(lower_case_query) != -1):
            results.append(airport)
    
    # Return a limited number of results for performance
    return results[:limit]

def find_airports(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Finds airports that match multiple criteria.
    
    Args:
        filters: A dictionary of filters to apply
    
    Returns:
        A list of matching airports
    """
    results = []
    
    for airport in airports:
        match = True
        for key, filter_value in filters.items():
            if key == 'has_scheduled_service':
                # Check if the airport's scheduled_service matches the filter
                scheduled_service = airport.get('scheduled_service')
                
                # Convert string "yes"/"no" to boolean if needed
                if isinstance(scheduled_service, str):
                    actual_value = scheduled_service.lower() == 'yes'
                else:
                    actual_value = bool(scheduled_service)
                
                if actual_value != filter_value:
                    match = False
                    break
            
            elif key == 'min_runway_ft':
                try:
                    runway_length = int(airport.get('runway_length', 0))
                    if runway_length < filter_value:
                        match = False
                        break
                except (ValueError, TypeError):
                    match = False
                    break
            
            else:
                # For other filters, do exact match
                if airport.get(key) != filter_value:
                    match = False
                    break
        
        if match:
            results.append(airport)
    
    return results

def get_airports_by_timezone(timezone: str) -> List[Dict[str, Any]]:
    """
    Finds all airports within a specific timezone.
    
    Args:
        timezone: The timezone identifier (e.g., 'Europe/London')
    
    Returns:
        A list of matching airports
    
    Raises:
        ValueError: If timezone is empty
    """
    if not timezone:
        raise ValueError("Timezone cannot be empty.")
    
    # The data key is 'time', you might want to alias it to 'timezone'
    return [airport for airport in airports if airport.get('time') == timezone]

def get_airport_links(code: str) -> Optional[Dict[str, Optional[str]]]:
    """
    Gets a map of external links for a given airport.
    
    Args:
        code: The IATA or ICAO code of the airport
    
    Returns:
        A dictionary of links, or None if airport not found
    """
    airport = _get_airport_by_code(code)
    if not airport:
        return None
    
    return {
        'website': airport.get('website'),
        'wikipedia': airport.get('wikipedia'),
        'flightradar24': airport.get('flightradar24_url'),
        'radarbox': airport.get('radarbox_url'),
        'flightaware': airport.get('flightaware_url'),
    }