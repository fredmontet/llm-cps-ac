#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the constants used in the heating simulation.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-07"
__version__ = "3.0"
__email__ = "philippe.marziale@edu.hefr.ch"


HEAT_CAPACITY = {"air": 1, "water": 4180, "house": 200}  # J/kg*K

FUEL_EFFICIENCIES = {  # kWh/kg - Calorific value
    "mazout": 11.9,
    "gas": 10,  # kWh/m³ - natural gas
    "wood": 3.9,
    "pellets": 4.8,
    "electricity": 1,
}

FUEL_PRICE = {  # ct./kWh
    "mazout": 10.14,
    "gas": 16.86,
    "wood": 13.5,
    "pellets": 10.07,
    "electricity": 23.43,
}

# Simulation parameters
TIME_STEP = {"minute": 60, "hour": 3600}  # seconds
MIN_SET_TEMPERATURE = -10
MAX_SET_TEMPERATURE = 40
MIN_OUTSIDE_TEMPERATURE = -50
MAX_OUTSIDE_TEMPERATURE = 50
MIN_BUILDING_EDGE = 1
MAX_BUILDING_EDGE = 100
MIN_HEAT_TRANSFER_COEFFICIENT = 0.1
MAX_HEAT_TRANSFER_COEFFICIENT = 10
MIN_BOILER_POWER = 1000
MAX_BOILER_POWER = 35000
MIN_VOLUME_HEAT_CAPACITY = 1
MAX_VOLUME_HEAT_CAPACITY = 5000
