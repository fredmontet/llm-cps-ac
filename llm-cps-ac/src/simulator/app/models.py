#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data models used in the FastAPI application.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "1.1"
__email__ = "philippe.marziale@edu.hefr.ch"


from pydantic import BaseModel
from enum import Enum


class Attribute(BaseModel):
    """Attribute model for the API"""

    value: float


class Boolean(BaseModel):
    """Boolean model for the API"""

    value: bool


class FuelChoice(str, Enum):
    """Fuel choice for the API"""

    mazout = "mazout"
    gas = "gas"
    wood = "wood"
    pellets = "pellets"
    electricity = "electricity"


class Fuel(BaseModel):
    """Fuel model for the API"""

    fuel: FuelChoice


class HeatCapacityChoice(str, Enum):
    """Heat capacity choice for the API"""

    air = "air"
    water = "water"
    house = "house"


class HeatCapacity(BaseModel):
    """Heat capacity model for the API"""

    heat_capacity: HeatCapacityChoice
