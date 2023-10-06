# airports-py

A comprehensive Python library providing easy retrieval of airport data based on IATA, ICAO, city codes, country codes, and continents. Ideal for developers building applications related to aviation, travel, and geography in Python.

## Features

- Retrieve airport data using IATA code.
- Retrieve airport data using ICAO code.
- Fetch data using city codes.
- Fetch data using country codes.
- Retrieve data based on continents.
- Built-in error handling for invalid input formats.
- Efficiently packaged with gzipped data.
- **Comprehensive Data Access**: Retrieve airport data using IATA code, ICAO code, city codes, country codes, and continents.
- **Unique Link Integration**: The first library to provide direct links to [FlightRadar24](https://www.flightradar24.com/), [Radarbox](https://www.radarbox.com/), and [FlightAware](https://www.flightaware.com/) for each airport, giving users immediate access to live flight tracking and airport data.

## Installation

You can install `airports-py` using pip:

```bash
pip install airports-py
```

## Usage

Here's how you can use the library:

```python
from airports import airport_data

# Retrieve airport data using IATA code
airport_by_iata = airport_data.get_airport_by_iata("AAA")
print(airport_by_iata)

# Retrieve airport data using ICAO code
airport_by_icao = airport_data.get_airport_by_icao("NTGA")
print(airport_by_icao)

# Fetch data using city codes
airport_by_city = airport_data.get_airport_by_city_code("NYC")
print(airport_by_city)

# Fetch data using country codes
airport_by_country = airport_data.get_airport_by_country_code("US")
print(airport_by_country)

# Retrieve data based on continents
airport_by_continent = airport_data.get_airport_by_continent("AS")
print(airport_by_continent)
```

### Using Command-Line Interface (CLI):

You can also directly execute Python code from the CLI without entering the interactive shell. Navigate to the root of your project and run:

```bash
python3 -c "from airports import airport_data; result = airport_data.get_airport_by_iata('MAA'); print(result)"
```

Replace `'MAA'` with other codes as needed.

## Testing

To test the library locally:

1. Navigate to the root of the project:

```bash
cd path_to_airports-py
```

2. Run the tests using:

```bash
python3 -m unittest discover tests -v
```

This command will discover and run all test files inside the `tests` directory and provide a detailed output.

## Example Data Fields

For Chennai International Airport:

| Field Name           | Data                                                     |
|----------------------|----------------------------------------------------------|
| IATA                 | MAA                                                      |
| ICAO                 | VOMM                                                     |
| Time Zone            | Asia/Kolkata                                             |
| City Code            | MAA                                                      |
| Country Code         | IN                                                       |
| Name                 | Chennai International Airport                            |
| Latitude             | 12.99                                                    |
| Longitude            | 80.1693                                                  |
| Altitude (in feet)   | 52                                                       |
| State                | Tamil Nadu                                               |
| City                 | Pallavaram                                               |
| County               | Kancheepuram                                             |
| State Code           | Tamil Nadu                                               |
| Airport Type         | large_airport                                            |
| Continent            | AS                                                       |
| State Abbreviation   | IN-TN                                                    |
| International        | TRUE                                                     |
| Wikipedia Link       | [Wikipedia](https://en.wikipedia.org/wiki/Chennai_International_Airport)|
| Official Website     | [Chennai Airport](http://chennaiairport.com)            |
| Location ID          | 12513629                                                 |
| Phone Number         | 044-2340551                                              |
| Runway Length (in meters) | 10050                                               |
| Flightradar24        | [Flightradar24](https://www.flightradar24.com/airport/MAA)|
| Radarbox             | [Radarbox](https://www.radarbox.com/airport/VOMM)       |
| Flightaware Link     | [Flightaware](https://www.flightaware.com/live/airport/VOMM)|

### Singapore Changi Airport:

| Field Name           | Data                                                     |
|----------------------|----------------------------------------------------------|
| IATA                 | SIN                                                      |
| ICAO                 | WSSS                                                     |
| Time Zone            | Asia/Singapore                                           |
| City Code            | SIN                                                      |
| Country Code         | SG                                                       |
| Name                 | Singapore Changi Airport                                 |
| Latitude             | 1.35019                                                  |
| Longitude            | 103.994                                                  |
| Altitude (in feet)   | 22                                                       |
| State                | Singapore                                                |
| City                 | Singapore                                                |
| County               | Singapore                                                |
| State Code           | South East                                               |
| Airport Type         | large_airport                                            |
| Continent            | AS                                                       |
| State Abbreviation   | SG-04                                                    |
| International        | TRUE                                                     |
| Wikipedia Link       | [Wikipedia](https://en.wikipedia.org/wiki/Singapore_Changi_Airport)|
| Official Website     | [Changi Airport](http://www.changiairport.com/)         |
| Location ID          | 12517525                                                 |
| Phone Number         | (65) 6542 1122                                           |
| Runway Length (in meters) | 13200                                               |
| Flightradar24         | [Flightradar24](https://www.flightradar24.com/airport/SIN)|
| Radarbox              | [Radarbox](https://www.radarbox.com/airport/WSSS)       |
| Flightaware           | [Flightaware](https://www.flightaware.com/live/airport/WSSS)|


## Running the Project Locally

1. Clone the repository:

```bash
git clone https://github.com/aashishvanand/airports-py.git
```

2. Change into the cloned directory:

```bash
cd airports-py
```

3. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

4. To run tests:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/aashishvanand/airports-py/issues).