#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script retrieves the current temperature for a given address by leveraging
the Open-Meteo API for weather data and the OpenStreetMap Nominatim API for geocoding.

It first obtains the latitude and longitude coordinates for the address, then uses
these coordinates to fetch the weather data, and finally prints the current temperature.

Retrieved from PS6 - AppGPT
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-06-26"
__version__ = "1.4"
__email__ = "philippe.marziale@edu.hefr.ch"


import pytz
import requests
from datetime import datetime

# API URLs
API_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
API_GEOCODE_URL = "https://nominatim.openstreetmap.org/search"


def get_weather(latitude, longitude, current_time):
    """
    Get the current weather for the specified latitude and longitude.

    Args:
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.
        current_time (datetime): The current time.

    Returns:
        float: The current temperature in Celsius.
    """
    # Prepare the request parameters for the weather API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "windspeed_10m", "precipitation"],
        "timezone": "auto",
        "forecast_days": 1,
    }

    # Send the request to the weather API
    response = requests.get(API_WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        current_temp = None

        return data

        # Loop through the temperature data to find the current temperature
        for time, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]):
            time_utc = datetime.fromisoformat(time).replace(tzinfo=pytz.utc)
            if current_time < time_utc:
                current_temp = temp
                break

        # Return the current temperature or the last temperature value if not found
        return current_temp or data["hourly"]["temperature_2m"][-1]


def geocode(address):
    """
    Get the latitude and longitude coordinates of the given address.

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: A tuple containing the latitude and longitude coordinates.
    """
    # Prepare the request parameters for the geocoding API
    params = {"q": address, "format": "json"}

    # Send the request to the geocoding API
    response = requests.get(API_GEOCODE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            # Return the latitude and longitude coordinates
            return data[0]["lat"], data[0]["lon"]
        else:
            # print(f"No results fdgfd for the address: {address}")
            return f"No results found for the address: {address}"
    else:
        # print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"


def get_current_time():
    """
    Get the current time in the Europe/Paris timezone.

    Returns:
        datetime: The current time as a datetime object.
    """
    tz = pytz.timezone("Europe/Paris")
    return datetime.now(tz)


"""
if __name__ == "__main__":
    address = "HEIA-FR, Fribourg, CH"
    latitude, longitude = geocode(address)
    current_time = get_current_time()
    current_temp = get_weather(latitude, longitude, current_time)

    # Print the temperature information with a formatted time string
    print(
        f"Current temperature at {address}, at {current_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')} : {current_temp}°C"
    )
"""
