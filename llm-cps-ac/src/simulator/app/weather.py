#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the Weather class used in the heating simulation.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-06-21"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import requests
from datetime import datetime
import pytz

from app.constants import TIME_STEP


class Weather:
    """
    Class to handle the interaction with the OpenMeteo API to get weather data.
    """

    # The API URLs
    API_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    API_GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(self, address):
        """
        Initialize a Weather with given parameters.

        Args:
            address (str): The address to get weather data for
        """
        self.address = address
        self.current_time = datetime.now(pytz.timezone("Europe/Paris"))
        self.latitude, self.longitude = self.geocode()
        self.weather_data = self.get_weather(self.current_time)
        self.index = 0
        self.counter = 0

    def geocode(self):
        """
        Get the latitude and longitude coordinates of the given address.
        """
        # Prepare the request parameters for the geocoding API
        params = {"q": self.address, "format": "json"}

        # Send the request to the geocoding API
        response = requests.get(self.API_GEOCODE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if data:
                # Return the latitude and longitude coordinates
                return float(data[0]["lat"]), float(data[0]["lon"])
            else:
                raise Exception(f"No results found for the address: {self.address}")
        else:
            raise Exception(f"Error: {response.status_code}")

    def get_weather(self, current_time):
        """
        Get the weather for the specified latitude and longitude,
        7 days from the day of the call and every hour.

        Args:
            current_time (datetime): The current time
        """
        # Make the current_time timezone-aware
        utc = pytz.UTC
        current_time = current_time.replace(tzinfo=utc)

        # Prepare the request parameters for the weather API
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": "temperature_2m",
            "timezone": "auto",
        }

        # Send the request to the weather API
        response = requests.get(self.API_WEATHER_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Return the temperature data
            return list(zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]))

    def update_building_outside_temperature(self, building, time_step):
        """
        Update the outside temperature of the building with the current temperature.

        Args:
            building (Building): The building to update.
            time_step (int): The time step in minutes
        """
        self.counter += time_step
        if self.counter >= TIME_STEP["hour"]:
            self.counter = 0
            self.index = (self.index + 1) % len(self.weather_data)

        time, temperature = self.weather_data[self.index]
        building.outside_temperature = temperature
        # print(f"Outside temperature: {building.outside_temperature}°C")
