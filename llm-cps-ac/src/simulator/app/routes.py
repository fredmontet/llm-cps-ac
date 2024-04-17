#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes module for the heating simulation.
Defines the routes of the FastAPI application.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "1.2"
__email__ = "philippe.marziale@edu.hefr.ch"


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import app.constants as cst
from app.instances import building, boiler
from app.models import Attribute, Boolean, HeatCapacity, Fuel


# Initialize the API router
router = APIRouter()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/static")


# Get the home page
@router.get("/", response_class=HTMLResponse, description="Home page.")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Set temperature
@router.get(
    "/get-set-temperature", description="Get the set temperature in the building in °C."
)
def get_set_temperature():
    return {"set_temperature": building.set_temperature}


@router.post(
    "/set-set-temperature", description="Set the set temperature in the building in °C."
)
def set_set_temperature(attr: Attribute):
    if attr.value < cst.MIN_SET_TEMPERATURE or attr.value > cst.MAX_SET_TEMPERATURE:
        return {
            "message": f"Set temperature must be between {cst.MIN_SET_TEMPERATURE} and {cst.MAX_SET_TEMPERATURE} °C"
        }
    building.set_temperature = attr.value
    return {"message": f"Set temperature successfully set to {attr.value} °C"}


# Outside temperature
@router.get(
    "/get-outside-temperature", description="Get the outside temperature in °C."
)
def get_outside_temperature():
    return {"outside_temperature": building.outside_temperature}


@router.post(
    "/set-outside-temperature", description="Set the outside temperature in °C."
)
def set_outside_temperature(attr: Attribute):
    if (
        attr.value < cst.MIN_OUTSIDE_TEMPERATURE
        or attr.value > cst.MAX_OUTSIDE_TEMPERATURE
    ):
        return {
            "message": f"Outside temperature must be between {cst.MIN_OUTSIDE_TEMPERATURE} and {cst.MAX_OUTSIDE_TEMPERATURE} °C"
        }
    if building.use_real_weather:
        return {"message": "Cannot set outside temperature when taking real weather"}
    building.outside_temperature = attr.value
    return {"message": f"Outside temperature successfully set to {attr.value} °C"}


@router.post(
    "/set-use-real-weather",
    description="Use or not the real weather of a parameterized location.",
)
def set_use_real_weather(attr: Boolean):
    if attr.value == building.use_real_weather:
        return {"message": f"Use real weather already set to {attr.value}"}
    building.use_real_weather = attr.value
    return {"message": f"Use real weather successfully set to {attr.value}"}


# Building edge
@router.get("/get-building-edge", description="Get the building edge in m.")
def get_building_edge():
    return {"building_edge": building.building_edge}


@router.post("/set-building-edge", description="Set the building edge in m.")
def set_building_edge(attr: Attribute):
    if attr.value < cst.MIN_BUILDING_EDGE or attr.value > cst.MAX_BUILDING_EDGE:
        return {
            "message": f"Building edge must be between {cst.MIN_BUILDING_EDGE} and {cst.MAX_BUILDING_EDGE} m"
        }
    building.building_edge = attr.value
    return {"message": f"Building edge successfully set to {attr.value} m"}


# U coefficient
@router.get(
    "/get-heat-transfer-coefficient",
    description="Get the heat transfer coefficient (U) in W/(m²K).",
)
def get_heat_transfer_coefficient():
    return {"heat_transfer_coefficient": building.heat_transfer_coefficient}


@router.post(
    "/set-heat-transfer-coefficient",
    description="Set the heat transfer coefficient (U) in W/(m²K).",
)
def set_heat_transfer_coefficient(attr: Attribute):
    if (
        attr.value < cst.MIN_HEAT_TRANSFER_COEFFICIENT
        or attr.value > cst.MAX_HEAT_TRANSFER_COEFFICIENT
    ):
        return {
            "message": f"Heat transfer coefficient must be between {cst.MIN_HEAT_TRANSFER_COEFFICIENT} and {cst.MAX_HEAT_TRANSFER_COEFFICIENT} W/(m²K)"
        }
    building.heat_transfer_coefficient = attr.value
    return {
        "message": f"Heat transfer coefficient successfully set to {attr.value} W/(m²K)"
    }


# Boiler power
@router.get("/get-boiler-power", description="Get the boiler power in W.")
def get_boiler_power():
    return {"boiler_power": boiler.boiler_power}


@router.post("/set-boiler-power", description="Set the boiler power in W.")
def set_boiler_power(attr: Attribute):
    if attr.value < cst.MIN_BOILER_POWER or attr.value > cst.MAX_BOILER_POWER:
        return {
            "message": f"Boiler power must be between {cst.MIN_BOILER_POWER} and {cst.MAX_BOILER_POWER} W"
        }
    boiler.boiler_power = attr.value
    return {"message": f"Boiler power successfully set to {attr.value} W"}


# Volume heat capacity
@router.get(
    "/get-volume-heat-capacity",
    description="Get the volume heat capacity in J/(kg*K) or J/(m³*K).",
)
def get_volume_heat_capacity():
    return {"volume_heat_capacity": building.volume_heat_capacity}


@router.post(
    "/set-volume-heat-capacity",
    description="Set the volume heat capacity in J/(kg*K) or J/(m³*K).",
)
def set_volume_heat_capacity(attr: Attribute):
    if (
        attr.value < cst.MIN_VOLUME_HEAT_CAPACITY
        or attr.value > cst.MAX_VOLUME_HEAT_CAPACITY
    ):
        return {
            "message": f"Volume heat capacity must be between {cst.MIN_VOLUME_HEAT_CAPACITY} and {cst.MAX_VOLUME_HEAT_CAPACITY} J/(kg*K) or J/(m³*K)"
        }
    building.volume_heat_capacity = attr.value
    return {
        "message": f"Volume heat capacity successfully set to {attr.value} J/(kg*K) or J/(m³*K)"
    }


# Boiler fuel
@router.get("/get-boiler-fuel", description="Get the boiler fuel.")
def get_boiler_fuel():
    return {"boiler_fuel": boiler.fuel}


@router.post("/set-boiler-fuel", description="Set the boiler fuel.")
def set_boiler_fuel(attr: Fuel):
    if attr.fuel == boiler.fuel:
        return {"message": f"Boiler fuel already set to {attr.fuel[0:]}"}
    boiler.fuel = attr.fuel
    return {"message": f"Boiler fuel successfully set to {attr.fuel[0:]}"}


# Volume heat capacity (variable)
@router.get(
    "/get-volume-heat-capacity-var",
    description="Get the volume heat capacity variable.",
)
def get_volume_heat_capacity_var():
    return {"volume_heat_capacity_variable": building.volume_heat_capacity_var}


@router.post(
    "/set-volume-heat-capacity-var",
    description="Set the volume heat capacity variable.",
)
def set_volume_heat_capacity_var(attr: HeatCapacity):
    if attr.heat_capacity == building.volume_heat_capacity_var:
        return {
            "message": f"Volume heat capacity variable already set to {attr.heat_capacity[0:]}"
        }
    building.volume_heat_capacity_var = attr.heat_capacity
    building.volume_heat_capacity = cst.HEAT_CAPACITY[attr.heat_capacity]
    return {
        "message": f"Volume heat capacity variable successfully set to {attr.heat_capacity[0:]}"
    }


# Building temperature
@router.get(
    "/get-current-building-temperature",
    description="Get the current building temperature in °C.",
)
def get_building_temperature():
    return {
        "current_building_temperature": float(f"{building.building_temperature:.2f}")
    }


# Temperature reached
@router.get(
    "/get-temperature-reached",
    description="Get the temperature that will be reached in °C.",
)
def get_temperature_reached():
    return {
        "temperature_reached": float(f"{building.calculate_temperature_reached():.2f}")
    }


# Boiler operating percentage
@router.get(
    "/get-boiler-operating-percentage",
    description="Get the boiler operating percentage.",
)
def get_boiler_operating_percentage():
    return {"boiler_operating_percentage": float(f"{boiler.operating_percentage:.2f}")}


# Current energy consumption
@router.get(
    "/get-current-building-energy-consumption",
    description="Get the current building energy consumption in kWh.",
)
def get_energy_consumption():
    return {
        "current_building_energy_consumption": float(
            f"{building.calculate_energy_consumption_kWh():.2f}"
        )
    }


# Current boiler heat power
@router.get(
    "/get-current-boiler-heat-power",
    description="Get the current boiler heat power in W.",
)
def get_boiler_heat_power():
    return {"current_boiler_heat_power": float(f"{boiler.current_power:.2f}")}


# Current fuel consumption
@router.get(
    "/get-current-fuel-consumption",
    description="Get the current fuel consumption kg/h or m³/h or kWh.",
)
def get_fuel_consumption():
    return {
        "current_fuel_consumption": float(f"{boiler.calculate_fuel_consumption():.2f}")
    }


# Current energy price
@router.get(
    "/get-current-energy-price", description="Get the current energy price in CHF/year."
)
def get_energy_price():
    return {
        "current_energy_price": float(f"{boiler.calculate_fuel_price_per_year():.2f}")
    }
