#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Instances module for the heating simulation.
This module is used to initialize the boiler, building, regulator and weather objects.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


from app.boiler import Boiler
from app.building import Building
from app.regulator import Regulator
from app.weather import Weather

from app.constants import HEAT_CAPACITY


# Set the default values of the elements
BOILER_POWER = 30000  # W
OPERATING_PERCENTAGE = 0  # %
CHOOSEN_FUEL = "pellets"
BUILDING_TEMPERATURE = 15  # °C
SET_TEMPERATURE = 20  # °C
OUTSIDE_TEMPERATURE = 15  # °C
BUILDING_EDGE = 10  # m
HEAT_TRANSFER_COEFFICIENT = 0.2  # W/m²*K
CHOOSE_HEAT_CAPACITY = "house"
TIME_STEP = "hour"
LOCATION = "HEIA-FR, Fribourg"


# Initialization of the boiler with given parameters
boiler = Boiler(
    boiler_power=BOILER_POWER,
    operating_percentage=OPERATING_PERCENTAGE,
    fuel=CHOOSEN_FUEL,
)

# Initialization of the weather
weather = Weather(LOCATION)

# Initialization of the building with given parameters
building = Building(
    building_temperature=BUILDING_TEMPERATURE,
    set_temperature=SET_TEMPERATURE,
    outside_temperature=OUTSIDE_TEMPERATURE,
    building_edge=BUILDING_EDGE,
    heat_transfer_coefficient=HEAT_TRANSFER_COEFFICIENT,
    volume_heat_capacity=HEAT_CAPACITY[CHOOSE_HEAT_CAPACITY],
    boiler=boiler,
    weather=weather,
)

# Initialization of the regulator
regulator = Regulator()
