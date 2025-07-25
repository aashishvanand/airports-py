import unittest
from airports import airport_data

class TestAirportData(unittest.TestCase):

    def test_get_airport_by_iata(self):
        """Test retrieving airport data for a valid IATA code"""
        result = airport_data.get_airport_by_iata("AAA")
        self.assertTrue(result)
        self.assertEqual(result[0]['iata'], "AAA")
        
        # Test error handling for invalid format
        with self.assertRaises(ValueError):
            airport_data.get_airport_by_iata("AA")  # Too short
        
        # Test error handling for non-existent code
        with self.assertRaises(ValueError):
            airport_data.get_airport_by_iata("ZZZ")

    def test_get_airport_by_icao(self):
        """Test retrieving airport data for a valid ICAO code"""
        result = airport_data.get_airport_by_icao("NTGA")
        self.assertTrue(result)
        self.assertEqual(result[0]['icao'], "NTGA")
        
        # Test error handling for invalid format
        with self.assertRaises(ValueError):
            airport_data.get_airport_by_icao("NTG")  # Too short

    def test_get_airport_by_city_code(self):
        """Test retrieving airport data for a valid city code"""
        # First, let's find a city code that actually exists
        available_city_codes = set()
        for airport in airport_data.airports:
            if airport.get('city_code'):
                available_city_codes.add(airport['city_code'])
        
        # Use the first available city code, or fall back to a common one
        if available_city_codes:
            test_city_code = list(available_city_codes)[0]
            result = airport_data.get_airport_by_city_code(test_city_code)
            self.assertTrue(result)
            self.assertEqual(result[0]['city_code'], test_city_code)
        else:
            # If no city codes exist, test error handling
            with self.assertRaises(ValueError):
                airport_data.get_airport_by_city_code("XYZ")

    def test_get_airport_by_country_code(self):
        """Test retrieving all airports for a given country code"""
        result = airport_data.get_airport_by_country_code("US")
        self.assertTrue(result)
        self.assertGreater(len(result), 100)  # US should have many airports
        self.assertEqual(result[0]['country_code'], "US")
        
        # Test error handling for invalid format
        with self.assertRaises(ValueError):
            airport_data.get_airport_by_country_code("USA")  # Too long

    def test_get_airport_by_continent(self):
        """Test retrieving all airports for a given continent code"""
        result = airport_data.get_airport_by_continent("AS")
        self.assertTrue(result)
        self.assertGreater(len(result), 100)  # Asia should have many airports
        self.assertEqual(result[0]['continent'], "AS")

    def test_search_by_name(self):
        """Test searching for airports by name"""
        result = airport_data.search_by_name("London")
        self.assertTrue(result)
        self.assertTrue(any('London' in airport.get('airport', '') for airport in result))
        
        # Test error handling for short query
        with self.assertRaises(ValueError):
            airport_data.search_by_name("L")  # Too short

    def test_find_nearby_airports(self):
        """Test finding airports within a given radius"""
        # Test around London coordinates
        lat, lon = 51.5074, -0.1278
        result = airport_data.find_nearby_airports(lat, lon, 50)  # 50km radius
        self.assertTrue(result)
        # Should include LHR (Heathrow)
        self.assertTrue(any(airport.get('iata') == 'LHR' for airport in result))

    def test_get_airports_by_type(self):
        """Test retrieving airports by type"""
        # Test large airports
        large_airports = airport_data.get_airports_by_type('large_airport')
        self.assertGreater(len(large_airports), 10)
        self.assertTrue(all(airport.get('type') == 'large_airport' for airport in large_airports))
        
        # Test convenience search for all airports
        all_airports = airport_data.get_airports_by_type('airport')
        self.assertGreater(len(all_airports), 50)
        self.assertTrue(all('airport' in airport.get('type', '').lower() for airport in all_airports))
        
        # Test error handling
        with self.assertRaises(ValueError):
            airport_data.get_airports_by_type("")  # Empty string

    def test_calculate_distance(self):
        """Test calculating distance between two airports"""
        # Distance between LHR and JFK should be approximately 5540 km
        distance = airport_data.calculate_distance('LHR', 'JFK')
        self.assertIsNotNone(distance)
        self.assertAlmostEqual(distance, 5540, delta=100)  # Allow 100km tolerance
        
        # Test with non-existent airport
        distance = airport_data.calculate_distance('XYZ', 'JFK')
        self.assertIsNone(distance)

    def test_get_autocomplete_suggestions(self):
        """Test autocomplete suggestions functionality"""
        suggestions = airport_data.get_autocomplete_suggestions('London')
        self.assertGreater(len(suggestions), 0)
        self.assertLessEqual(len(suggestions), 10)  # Should limit to 10
        self.assertTrue(any(airport.get('iata') == 'LHR' for airport in suggestions))
        
        # Test with short query
        suggestions = airport_data.get_autocomplete_suggestions('L')
        self.assertEqual(len(suggestions), 0)

    def test_find_airports_advanced_filtering(self):
        """Test advanced filtering functionality"""
        # Test filtering by multiple criteria
        airports = airport_data.find_airports({
            'country_code': 'GB',
            'type': 'large_airport'
        })
        self.assertTrue(all(
            airport.get('country_code') == 'GB' and 
            airport.get('type') == 'large_airport' 
            for airport in airports
        ))
        
        # Test filtering by scheduled service
        airports_with_service = airport_data.find_airports({'has_scheduled_service': True})
        airports_without_service = airport_data.find_airports({'has_scheduled_service': False})
        
        # At least one of these should have results
        self.assertGreater(len(airports_with_service) + len(airports_without_service), 0)

    def test_get_airports_by_timezone(self):
        """Test finding airports by timezone"""
        airports = airport_data.get_airports_by_timezone('Europe/London')
        self.assertGreater(len(airports), 10)
        self.assertTrue(all(airport.get('time') == 'Europe/London' for airport in airports))
        
        # Test error handling
        with self.assertRaises(ValueError):
            airport_data.get_airports_by_timezone('')  # Empty timezone

    def test_get_airport_links(self):
        """Test retrieving external links for airports"""
        # Test with LHR
        links = airport_data.get_airport_links('LHR')
        self.assertIsNotNone(links)
        self.assertIn('website', links)
        self.assertIn('wikipedia', links)
        self.assertIn('flightradar24', links)
        self.assertIn('radarbox', links)
        self.assertIn('flightaware', links)
        
        # Test with non-existent airport
        links = airport_data.get_airport_links('XYZ')
        self.assertIsNone(links)

    def test_private_helper_functions(self):
        """Test private helper functions"""
        # Test _get_airport_by_code
        airport = airport_data._get_airport_by_code('LHR')
        self.assertIsNotNone(airport)
        self.assertEqual(airport.get('iata'), 'LHR')
        
        airport = airport_data._get_airport_by_code('EGLL')
        self.assertIsNotNone(airport)
        self.assertEqual(airport.get('icao'), 'EGLL')
        
        # Test with invalid input
        airport = airport_data._get_airport_by_code('invalid')
        self.assertIsNone(airport)

    def test_case_insensitive_operations(self):
        """Test that operations are case insensitive where appropriate"""
        # IATA codes should work with lowercase (now fixed!)
        result1 = airport_data.get_airport_by_iata("AAA")
        result2 = airport_data.get_airport_by_iata("aaa")
        self.assertEqual(result1, result2)
        
        # Country codes should work with lowercase
        result1 = airport_data.get_airport_by_country_code("US")
        result2 = airport_data.get_airport_by_country_code("us")
        self.assertEqual(result1, result2)
        
        # Airport type search should be case insensitive
        result1 = airport_data.get_airports_by_type("large_airport")
        result2 = airport_data.get_airports_by_type("LARGE_AIRPORT")
        self.assertEqual(len(result1), len(result2))

if __name__ == '__main__':
    unittest.main(verbosity=2)