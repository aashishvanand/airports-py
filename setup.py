from setuptools import setup, find_packages

setup(
    name="airports-py",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Aashish Vivekanand",
    author_email="aashishvanand@gmail.com",
    description="A comprehensive library providing easy retrieval of airport data based on IATA, ICAO, city codes, country codes, and continents. Ideal for developers building applications related to aviation, travel, and geography.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aashishvanand/airports-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Creative Commons Attribution License",
        "Operating System :: OS Independent",
    ],
)
