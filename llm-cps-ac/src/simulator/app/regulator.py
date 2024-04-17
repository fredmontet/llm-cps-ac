#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the Regulator class used in the heating simulation.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-06-23"
__version__ = "1.2"
__email__ = "philippe.marziale@edu.hefr.ch"


class Regulator:
    """
    Class to handle the regulation of the temperature of the boiler.
    """

    MIN_OPERATING_PERCENTAGE = 0  # Minimum operating percentage
    MAX_OPERATING_PERCENTAGE = 100  # Maximum operating percentage

    def __init__(self):
        self.cumulative_error = 0
        self.previous_error = 0
        self.Kp = 0.1  # Proportional gain
        self.Ki = 0.005  # Integral gain
        self.Kd = 0.01  # Derivative gain

    def _get_adjustment_rate(self, abs_delta_temperature):
        """
        Calculate the adjustment rate based on the absolute difference between the set and reached temperature.

        Args:
            abs_delta_temperature (float): The absolute difference between the set and reached temperature
        """
        if abs_delta_temperature >= 2:
            return abs_delta_temperature * 0.1
        if abs_delta_temperature >= 1:
            return abs_delta_temperature
        if abs_delta_temperature >= 0.5:
            return abs_delta_temperature * 2
        if abs_delta_temperature < 0.005:
            return abs_delta_temperature
        return abs_delta_temperature * 10

    def _get_adjustment_rate_PID(self, delta_temperature):
        """
        Calculate the adjustment rate based on the PID control strategy.

        Args:
            delta_temperature (float): The difference between the set and reached temperature
        """
        # Calculate the error terms
        self.cumulative_error += delta_temperature  # Integral term
        error_difference = delta_temperature - self.previous_error  # Derivative term
        self.previous_error = delta_temperature  # Update the previous error

        # PID controller
        P_term = self.Kp * delta_temperature
        I_term = self.Ki * self.cumulative_error
        D_term = self.Kd * error_difference

        return P_term + I_term + D_term

    def regulate_temperature(self, building):
        """
        Adjust the operating percentage of the boiler based on the difference between the current and set temperature.
        """
        # Calculate the difference between the set and reached temperature
        delta_temperature = building.set_temperature - building.building_temperature

        # Calculate the adjustment for the operating percentage based on the temperature difference
        # and increase the adjustment rate proportionally to the temperature difference
        adjustment_rate = self._get_adjustment_rate_PID(abs(delta_temperature))
        adjustment = delta_temperature * adjustment_rate

        # Adjust the operating percentage of the boiler
        building.boiler.operating_percentage += adjustment

        # Ensure that the operating percentage is within a reasonable range
        building.boiler.operating_percentage = min(
            self.MAX_OPERATING_PERCENTAGE,
            max(self.MIN_OPERATING_PERCENTAGE, building.boiler.operating_percentage),
        )

        # Recalculate the heating power of the boiler
        building.boiler._update_heating_power()
