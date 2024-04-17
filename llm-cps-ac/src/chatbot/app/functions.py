#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
List of all functions that can be called by the chatbot.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "1.3"


import json
import os
import requests

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from app.config import Config, ChatbotPrompt
from app.sql_db import Session, User
from app.vector_db import get_vectorstore


# Choose the right URL depending on the environment
if os.getenv("RUNNING_IN_DOCKER"):
    API_URL = "http://boiler-simulator:8000"
else:
    API_URL = "http://0.0.0.0:8000"


# Error message if the API is not available
error_message = "Error to connect to the heating system, please retry later."


#############################################
# Functions related to the simulator
#############################################


def get_value_from_API(endpoint):
    """
    Send a GET request to the specified endpoint and return the value.
    """
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        return response.json()
    except:
        return {"message": error_message}


def adjust_value_on_API(endpoint, value, action):
    """
    Adjust a value on the specified endpoint based on the action.
    """
    try:
        if action in ["increase", "decrease"]:
            get_endpoint = endpoint.replace("set", "get", 1)
            current_value = get_value_from_API(get_endpoint)[
                get_endpoint.replace("get-", "").replace("-", "_")
            ]
            if action == "increase":
                new_value = current_value + value
            else:
                new_value = current_value - abs(value)
        else:
            new_value = value
        payload = json.dumps({"value": new_value})
        response = requests.post(f"{API_URL}/{endpoint}", data=payload)
        return response.json()
    except:
        return {"message": error_message}


def get_set_temperature():
    """
    Get the current set temperature in the building in °C.
    """
    return get_value_from_API("get-set-temperature")


def adjust_set_temperature(temperature, action):
    """
    Adjust the set temperature in the building in °C.
    """
    return adjust_value_on_API("set-set-temperature", temperature, action)


def get_outside_temperature():
    """
    Get the current outside temperature in °C.
    """
    return get_value_from_API("get-outside-temperature")


def adjust_outside_temperature(temperature, action):
    """
    Adjust the outside temperature in °C.
    """
    return adjust_value_on_API("set-outside-temperature", temperature, action)


def use_real_weather(action):
    """
    Use real weather data instead of the outside temperature set by the user.
    """
    if action == True:
        payload = json.dumps({"value": True})
    else:
        payload = json.dumps({"value": False})
    response = requests.post(f"{API_URL}/set-use-real-weather", data=payload)
    return response.json()


def get_building_edge():
    """
    Get the current building edge in m.
    """
    return get_value_from_API("get-building-edge")


def adjust_building_edge(edge, action):
    """
    Adjust the building edge in m.
    """
    return adjust_value_on_API("set-building-edge", edge, action)


def get_heat_transfer_coefficient():
    """
    Get the current heat transfer coefficient (U) in W/(m²K).
    """
    return get_value_from_API("get-heat-transfer-coefficient")


def adjust_heat_transfer_coefficient(coefficient, action):
    """
    Adjust the heat transfer coefficient (U) in W/(m²K).
    """
    return adjust_value_on_API("set-heat-transfer-coefficient", coefficient, action)


def get_boiler_power():
    """
    Get the boiler power in W.
    """
    return get_value_from_API("get-boiler-power")


def adjust_boiler_power(power, action):
    """
    Adjust the boiler power in W.
    """
    return adjust_value_on_API("set-boiler-power", power, action)


def get_volume_heat_capacity():
    """
    Get the current volume heat capacity in J/(kg*K) or J/(m³*K).
    """
    return get_value_from_API("get-volume-heat-capacity")


def adjust_volume_heat_capacity(capacity, action):
    """
    Adjust the volume heat capacity in J/(kg*K) or J/(m³*K).
    """
    return adjust_value_on_API("set-volume-heat-capacity", capacity, action)


def get_boiler_fuel():
    """
    Get the current boiler fuel.
    """
    return get_value_from_API("get-boiler-fuel")


def change_boiler_fuel(fuel):
    """
    Change the boiler fuel.
    """
    payload = json.dumps({"fuel": fuel})
    response = requests.post(f"{API_URL}/set-boiler-fuel", data=payload)
    return response.json()


def get_volume_heat_capacity_var():
    """
    Get the current volume heat capacity variable.
    """
    return get_value_from_API("get-volume-heat-capacity-var")


def change_volume_heat_capacity_var(heat_capacity):
    """
    Change the volume heat capacity variable.
    """
    payload = json.dumps({"heat_capacity": heat_capacity})
    response = requests.post(f"{API_URL}/set-volume-heat-capacity-var", data=payload)
    return response.json()


def get_building_temperature():
    """
    Get the current building temperature in °C.
    """
    return get_value_from_API("get-current-building-temperature")


def get_temperature_reached():
    """
    Get the temperature that will be reached in °C.
    """
    return get_value_from_API("get-temperature-reached")


def get_boiler_operating_percentage():
    """
    Get the current boiler operating percentage.
    """
    return get_value_from_API("get-boiler-operating-percentage")


def get_energy_consumption():
    """
    Get the current energy consumption in kWh.
    """
    return get_value_from_API("get-current-building-energy-consumption")


def get_boiler_heat_power():
    """
    Get the current boiler heat power in W.
    """
    return get_value_from_API("get-current-boiler-heat-power")


def get_fuel_consumption():
    """
    Get the current fuel consumption in kg/h or m³/h or kWh.
    """
    return get_value_from_API("get-current-fuel-consumption")


def get_energy_price():
    """
    Get the current energy price in CHF/year.
    """
    return get_value_from_API("get-current-energy-price")


#############################################
# Functions related to the SQL database
#############################################


def get_user_by_name_or_id(session, user_name, user_id):
    """
    Get a user by name or id
    """
    user = None
    if user_name and user_name != "x-x-x-x-x":
        user = session.query(User).filter(User.name == user_name).first()
    elif user_id and user_id != 9999999:
        user = session.query(User).filter(User.id == user_id).first()
    return user


def get_user_info(user_name="x-x-x-x-x", user_id=9999999):
    """
    Get information about a specific user by name or id
    """
    session = Session()
    user = get_user_by_name_or_id(session, user_name, user_id)

    # Check if user exists
    if user:
        user_info = json.dumps(user.to_json())
        db_user_name = json.loads(user_info)["name"]
        db_user_id = json.loads(user_info)["id"]

        # Check if user name and id match
        if user_name in (db_user_name, "x-x-x-x-x") and user_id in (
            db_user_id,
            9999999,
        ):
            session.close()
            return user_info
        else:
            session.close()
            return "User name and id do not match, please provide name and id of the same user"
    else:
        session.close()
        return "User not found"


def modify_user_preferred_temperature(
    temperature, action, user_name="x-x-x-x-x", user_id=9999999
):
    """
    Modify preferred temperature for a specific user
    """
    session = Session()
    user = get_user_by_name_or_id(session, user_name, user_id)

    # Check if user exists
    if user:
        user_info = json.dumps(user.to_json())
        db_user_name = json.loads(user_info)["name"]
        db_user_id = json.loads(user_info)["id"]

        # Check if user name and id match
        if user_name in (db_user_name, "x-x-x-x-x") and user_id in (
            db_user_id,
            9999999,
        ):
            if action == "increase":
                new_temperature = user.preferred_temperature + temperature
            elif action == "decrease":
                new_temperature = user.preferred_temperature - abs(temperature)
            else:
                new_temperature = temperature
            user.preferred_temperature = new_temperature
            session.commit()
            session.close()
            return f"Preferred temperature modified to {new_temperature}°C"
        else:
            session.close()
            return "User name and id do not match, please provide name and id of the same user"
    else:
        session.close()
        return "User not found"


#############################################
# Functions related to the vector database
#############################################


def ask_vector_db(question: str):
    """
    Ask a question to the vector database.
    Ask any questions about the heating system. This may include questions about operating hours
    features, usage, optimization methods, eco-friendly modes, heating brand and model, and so on.
    https://python.langchain.com/docs/modules/chains/additional/openai_functions_retrieval_qa

    """
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=Config.OPENAI_API_KEY),
        chain_type="stuff",
        retriever=get_vectorstore().as_retriever(),
        chain_type_kwargs={"prompt": ChatbotPrompt.PROMPT},
    )
    result = qa.run(question)
    return result


# List of all functions that can be called by the chatbot
all_functions = {
    "get_set_temperature": get_set_temperature,
    "adjust_set_temperature": adjust_set_temperature,
    "get_outside_temperature": get_outside_temperature,
    "adjust_outside_temperature": adjust_outside_temperature,
    "use_real_weather": use_real_weather,
    "get_building_edge": get_building_edge,
    "adjust_building_edge": adjust_building_edge,
    "get_heat_transfer_coefficient": get_heat_transfer_coefficient,
    "adjust_heat_transfer_coefficient": adjust_heat_transfer_coefficient,
    "get_boiler_power": get_boiler_power,
    "adjust_boiler_power": adjust_boiler_power,
    "get_volume_heat_capacity": get_volume_heat_capacity,
    "adjust_volume_heat_capacity": adjust_volume_heat_capacity,
    "get_boiler_fuel": get_boiler_fuel,
    "change_boiler_fuel": change_boiler_fuel,
    "get_volume_heat_capacity_var": get_volume_heat_capacity_var,
    "change_volume_heat_capacity_var": change_volume_heat_capacity_var,
    "get_building_temperature": get_building_temperature,
    "get_temperature_reached": get_temperature_reached,
    "get_boiler_operating_percentage": get_boiler_operating_percentage,
    "get_energy_consumption": get_energy_consumption,
    "get_boiler_heat_power": get_boiler_heat_power,
    "get_fuel_consumption": get_fuel_consumption,
    "get_energy_price": get_energy_price,
    "get_user_info": get_user_info,
    "modify_user_preferred_temperature": modify_user_preferred_temperature,
    "ask_vector_db": ask_vector_db,
}
