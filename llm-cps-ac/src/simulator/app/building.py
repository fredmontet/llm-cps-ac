#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the Building class used in the heating simulation.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "2.4"
__email__ = "philippe.marziale@edu.hefr.ch"


from app.constants import TIME_STEP


class Building:
    """
    Represents a building in the heating simulation.
    """

    EXPOSED_FACES = 5  # Number of faces exposed to the outside
    MAX_DELTA_TEMP = 50  # Maximum allowed temperature change

    def __init__(
        self,
        building_temperature,
        set_temperature,
        outside_temperature,
        building_edge,
        heat_transfer_coefficient,
        volume_heat_capacity,
        boiler,
        weather,
    ):
        """
        Initialize a building with given parameters.

        Args:
            building_temperature (float): Current temperature of the building
            set_temperature (float): Set temperature of the building
            outside_temperature (float): Outside temperature
            building_edge (float): Edge length of the cubical building
            heat_transfer_coefficient (float): Heat transfer coefficient
            volume_heat_capacity (int): Volume heat capacity type
            boiler (Boiler): Boiler used to heat the building
            weather (Weather): Weather object used to get the outside temperature
        """
        if (
            heat_transfer_coefficient <= 0
            or building_edge <= 0
            or volume_heat_capacity <= 0
        ):
            raise ValueError(
                "Heat transfer coefficient, building edge and volume heat capacity must be positive!"
            )

        # Initialize the building parameters
        self.building_temperature = building_temperature  # °C
        self.set_temperature = set_temperature  # °C
        self.outside_temperature = outside_temperature  # °C
        self.building_edge = building_edge  # m
        self.heat_transfer_coefficient = heat_transfer_coefficient  # W/m²/K
        self.volume_heat_capacity = volume_heat_capacity  # J/m³/°C
        self.boiler = boiler
        self.weather = weather

        # Initialize the use_real_weather variable
        self.use_real_weather = False

        # Initialize class functions
        self._calculate_building_surface()
        self._calculate_building_volume()
        self._calculate_heat_loss()

    def _calculate_building_surface(self):
        """
        Calculate the building's surface area.
        """
        self.building_surface = self.building_edge**2 * self.EXPOSED_FACES
        return self.building_surface

    def _calculate_building_volume(self):
        """
        Calculate the building's volume.
        """
        self.building_volume = self.building_edge**3
        return self.building_volume

    def _calculate_heat_loss(self):
        """
        Calculate the heat transfer coefficient.
        """
        self.heat_loss = (
            self.heat_transfer_coefficient
            * self.building_surface
            * (self.building_temperature - self.outside_temperature)
        )
        return self.heat_loss

    def toggle_use_real_weather(self):
        """
        Use real weather data or not.
        """
        self.use_real_weather = not self.use_real_weather

    def calculate_energy_consumption_kWh(self):
        """
        Calculate the energy consumption in kWh in the building.
        """
        energy = self.boiler.current_power / 1000 * 60  # W to kW to kWh
        return energy

    def calculate_temperature_reached(self):
        """
        Calculate the temperature to be reached in the building based on current boiler usage.
        """
        # Calculate the loss of the building
        loss = self.heat_transfer_coefficient * self.building_surface  # W/K

        # Calculate the gain of temperature in the building
        gain_temp = self.boiler.current_power / loss

        # Calculate the temperature to be reached
        reached_temp = self.outside_temperature + gain_temp
        return reached_temp

    def update_temperature(self, time_step):
        """
        Update the temperature of the building, considering the heat from boiler and heat loss to the outside.

        Args:
            time_step (float): Time step of the simulation in seconds
        """
        # Update boiler heating power
        self.boiler._update_heating_power()

        # Update building dimensions
        self._calculate_building_surface()
        self._calculate_building_volume()

        energy = self.boiler.current_power * TIME_STEP[time_step]  # Wh

        building_volume_to_liters = self.building_volume * 1000  # m³ to L
        building_heat_loss = (
            self._calculate_heat_loss() * TIME_STEP[time_step]
        )  # Building heat loss

        # New temperature
        delta_temperature = (energy - building_heat_loss) / (
            building_volume_to_liters * self.volume_heat_capacity
        )

        # Apply delta limit
        delta_temperature = max(
            min(delta_temperature, self.MAX_DELTA_TEMP), -self.MAX_DELTA_TEMP
        )
        self.building_temperature += delta_temperature
