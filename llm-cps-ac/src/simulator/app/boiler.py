#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the Boiler class used in the heating simulation.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-04"
__version__ = "2.2"
__email__ = "philippe.marziale@edu.hefr.ch"


from app.constants import FUEL_EFFICIENCIES, FUEL_PRICE


class Boiler:
    """
    Class to simulate a boiler heating system.
    """

    def __init__(self, boiler_power, operating_percentage, fuel):
        """
        Initialize a Boiler with given parameters.

        Args:
            boiler_power (float): The nominal power of the boiler in W
            operating_percentage (float): The percentage of the nominal power that the boiler is operating at
            fuel (str): Fuel type
        """
        if boiler_power <= 0:
            raise ValueError("Boiler power must be positive")
        if operating_percentage < 0 or operating_percentage > 100:
            raise ValueError("Operating percentage must be between 0 and 100")
        if fuel not in FUEL_EFFICIENCIES:
            raise ValueError(f"Fuel type {fuel} not recognized")

        self.boiler_power = boiler_power
        self.operating_percentage = operating_percentage
        self.fuel = fuel

        self.current_power = self._update_heating_power()

    def _update_heating_power(self):
        """
        Calculate the heating power of the boiler.
        """
        self.current_power = self.boiler_power * (self.operating_percentage / 100)  # W
        return self.current_power

    def calculate_fuel_consumption(self):
        """
        Calculate the amount of fuel used based on the current power and fuel type.
        """
        # Convert power from W to kW
        power_kWh = self.current_power / 1000  # kW

        # Calculate fuel usage based on fuel calorific value
        fuel_consumption = power_kWh / FUEL_EFFICIENCIES[self.fuel]
        return fuel_consumption

    def calculate_fuel_price_per_year(self):
        """
        Calculate the annual fuel price based on the fuel consumption.
        """
        fuel_consumption = self.calculate_fuel_consumption()  # kg/h
        fuel_price = FUEL_PRICE[self.fuel]  # fuel price in ct./kWh

        # Convert fuel price from ct./kWh to CHF/kWh
        fuel_price_chf_per_kwh = fuel_price / 100

        # Calculate the total fuel consumption per year in kWh
        fuel_consumption_per_year = fuel_consumption * 24 * 365  # kWh/year

        # Calculate the annual fuel price in CHF
        annual_fuel_price = fuel_consumption_per_year * fuel_price_chf_per_kwh
        return annual_fuel_price
