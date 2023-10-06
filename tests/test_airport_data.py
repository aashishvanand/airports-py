import unittest
from airports import airport_data

class TestAirportData(unittest.TestCase):

    def test_get_airport_by_iata(self):
        result = airport_data.get_airport_by_iata("AAA")
        self.assertTrue(result)
        self.assertEqual(result[0]['iata'], "AAA")

    def test_get_airport_by_icao(self):
        result = airport_data.get_airport_by_icao("NTGA")
        self.assertTrue(result)
        self.assertEqual(result[0]['icao'], "NTGA")

    def test_get_airport_by_city_code(self):
        result = airport_data.get_airport_by_city_code("NYC")
        self.assertTrue(result)
        self.assertEqual(result[0]['city_code'], "NYC")

    def test_get_airport_by_country_code(self):
        result = airport_data.get_airport_by_country_code("US")
        self.assertTrue(result)
        self.assertEqual(result[0]['country_code'], "US")

    def test_get_airport_by_continent(self):
        result = airport_data.get_airport_by_continent("AS")
        self.assertTrue(result)
        self.assertEqual(result[0]['continent'], "AS")

    # Add more tests as needed...

if __name__ == '__main__':
    unittest.main(verbosity=2)
