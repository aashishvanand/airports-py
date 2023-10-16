from setuptools import setup, find_packages

setup(
    name="airports-py",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Aashish Vivekanand",
    author_email="aashishvanand@gmail.com",
    description="A comprehensive library providing easy retrieval of airport data based on IATA, ICAO, city codes, country codes, and continents. Ideal for developers building applications related to aviation, travel, and geography.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://aashishvanand.me/airport-data-js/",
    project_urls={
        "Source Code": "https://github.com/aashishvanand/airports-py",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "airport", "iata", "icao", "data", "library", "aviation", 
        "travel", "geography", "lookup", "codes", "continent", 
        "city", "country", "flightradar24", "radarbox", "flightaware"
    ]
)
