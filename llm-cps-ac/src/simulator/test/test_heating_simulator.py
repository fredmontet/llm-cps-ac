#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This Python program tests the entire heating simulation.

Use the command "pytest" to run the tests.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-04"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


import unittest
from unittest.mock import patch
from datetime import timedelta

from app.boiler import Boiler
from app.building import Building
from app.simulator import Simulator
from app.regulator import Regulator
from app.weather import Weather


class TestBoiler(unittest.TestCase):
    """Test the boiler class."""

    # Set up a boiler with 1000 W power, 50% operating percentage and gas as fuel
    def setUp(self):
        self.boiler = Boiler(1000, 50, "gas")

    # Test the boiler initialization
    def test_init(self):
        self.assertEqual(self.boiler.boiler_power, 1000)
        self.assertEqual(self.boiler.operating_percentage, 50)
        self.assertEqual(self.boiler.fuel, "gas")

    # Test the boiler power update
    def test_update_heating_power(self):
        self.boiler._update_heating_power()
        self.assertEqual(self.boiler.current_power, 500)

    # Test the boiler fuel consumption calculation
    def test_calculate_fuel_consumption(self):
        consumption = self.boiler.calculate_fuel_consumption()
        self.assertAlmostEqual(consumption, 0.05)

    # Test the boiler fuel price calculation
    def test_calculate_fuel_price_per_year(self):
        price = self.boiler.calculate_fuel_price_per_year()
        self.assertGreaterEqual(price, 70)  # 0.05 * 16.86/100 * 24 * 365 = 73.8468

    # Test to check the boiler power with a negative power
    def test_check_boiler_power(self):
        with self.assertRaises(ValueError):
            Boiler(-1000, 50, "gas")

    # Test to check the operating percentage with an invalid percentage
    def test_check_operating_percentage(self):
        with self.assertRaises(ValueError):
            Boiler(1000, -50, "gas")
        with self.assertRaises(ValueError):
            Boiler(1000, 150, "gas")

    # Test to check the fuel type with an invalid fuel
    def test_check_fuel_type(self):
        with self.assertRaises(ValueError):
            Boiler(1000, 50, "nuclear")


class TestBuilding(unittest.TestCase):
    """Test the building class."""

    # Initialize the weather object with the city of Fribourg only once for all the tests
    @classmethod
    def setUpClass(cls):
        cls.weather = Weather("Fribourg, Suisse")

    # Set up a building with 20°C inside temperature, 24°C set temperature,
    # 10°C outside temperature,10m edge, 10 W/m^2K heat transfer coefficient,
    # 200 J/m^3K volume heat capacity and a boiler with 1000 W power, 50% operating
    # percentage and gas as fuel
    def setUp(self):
        boiler = Boiler(1000, 50, "gas")
        self.building = Building(
            20, 24, 10, 10, 10, 200, boiler, self.__class__.weather
        )

    # Test the building initialization
    def test_init(self):
        self.assertEqual(self.building.building_temperature, 20)
        self.assertEqual(self.building.set_temperature, 24)
        self.assertEqual(self.building.outside_temperature, 10)
        self.assertEqual(self.building.building_edge, 10)
        self.assertEqual(self.building.heat_transfer_coefficient, 10)
        self.assertEqual(self.building.volume_heat_capacity, 200)
        self.assertEqual(self.building.boiler.boiler_power, 1000)
        self.assertEqual(self.building.boiler.operating_percentage, 50)
        self.assertEqual(self.building.boiler.fuel, "gas")

    # Test the building surface calculation
    def test_calculate_building_surface(self):
        surface = self.building._calculate_building_surface()
        self.assertEqual(surface, 500)  # 10^2 * 5

    # Test the building volume calculation
    def test_calculate_building_volume(self):
        volume = self.building._calculate_building_volume()
        self.assertEqual(volume, 1000)  # 10^3

    # Test the building heat loss calculation
    def test_calculate_heat_loss(self):
        loss = self.building._calculate_heat_loss()
        self.assertEqual(loss, 50000)  # 10 * 500 * (20 - 10)

    # Test the toggle use real weather function
    def test_toggle_use_real_weather(self):
        self.building.toggle_use_real_weather()
        self.assertEqual(self.building.use_real_weather, True)

    # Test the building temperature update
    def test_calculate_energy_consumption_kWh(self):
        energy = self.building.calculate_energy_consumption_kWh()
        self.assertEqual(energy, 30.0)  # 500 / 1000 * 60

    # Test the building temperature update
    def test_calculate_temperature_reached(self):
        temperature = self.building.calculate_temperature_reached()
        self.assertEqual(temperature, 10.1)  # 10 + (500 / (10 * 500))

    # Test the building temperature update
    def test_update_temperature(self):
        self.building.update_temperature("minute")
        self.assertLessEqual(self.building.building_temperature, 20)
        self.building.update_temperature("hour")
        self.assertLessEqual(self.building.building_temperature, 20)

    # Test to check the edge size with a negative value
    def test_check_edge_size(self):
        with self.assertRaises(ValueError):
            Building(
                20, 24, 10, -10, 10, 200, self.building.boiler, self.building.weather
            )

    # Test to check the heat transfer coefficient with a negative value
    def test_check_heat_transfer_coefficient(self):
        with self.assertRaises(ValueError):
            Building(
                20, 24, 10, 10, -10, 200, self.building.boiler, self.building.weather
            )


class TestRegulator(unittest.TestCase):
    """Test the regulator class."""

    # Take previously initialized weather object
    @classmethod
    def setUpClass(cls):
        cls.weather = Weather("Fribourg, Suisse")

    # Set up a building with 20°C inside temperature, 24°C set temperature,
    # 10°C outside temperature,10m edge, 10 W/m^2K heat transfer coefficient,
    # 200 J/m^3K volume heat capacity, a boiler with 1000 W power, 50% operating
    # percentage and gas as fuel and a regulator
    def setUp(self):
        boiler = Boiler(1000, 50, "gas")
        self.building = Building(
            20, 24, 10, 10, 10, 200, boiler, self.__class__.weather
        )
        self.regulator = Regulator()

    # Test the regulator initialization
    def test_init(self):
        self.assertEqual(self.regulator.cumulative_error, 0)
        self.assertEqual(self.regulator.previous_error, 0)
        self.assertEqual(self.regulator.Kp, 0.1)
        self.assertEqual(self.regulator.Ki, 0.005)
        self.assertEqual(self.regulator.Kd, 0.01)

    # Test the regulator initialization
    def test_get_adjustment_rate(self):
        abs_delta_temperature = abs(
            self.building.set_temperature - self.building.building_temperature
        )
        adjustment_rate = self.regulator._get_adjustment_rate(abs_delta_temperature)
        self.assertLessEqual(adjustment_rate, 0.5)

    # Test the regulator initialization
    def test_get_adjustment_rate_PID(self):
        delta_temperature = (
            self.building.set_temperature - self.building.building_temperature
        )
        adjustment_rate = self.regulator._get_adjustment_rate_PID(delta_temperature)
        self.assertLessEqual(adjustment_rate, 0.5)

    # Test the regulator initialization
    def test_regulate_temperature(self):
        self.regulator.regulate_temperature(self.building)
        self.assertGreaterEqual(self.building.boiler.operating_percentage, 50)


class TestWeather(unittest.TestCase):
    """Test the weather class."""

    # Set up a weather object with the address of the Eiffel Tower
    def setUp(self):
        self.address = "Eiffel Tower, 5, Avenue Anatole France"
        self.weather = Weather(self.address)

    # Test the weather initialization
    def test_init(self):
        self.assertEqual(self.weather.address, self.address)
        self.assertEqual(self.weather.index, 0)
        self.assertEqual(self.weather.counter, 0)

    # Test the geocoding
    @patch("requests.get")
    def test_geocode(self, mock_get):
        # Mock the response from the API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"lat": "48.858260200000004", "lon": "2.2944990543196795"}
        ]

        lat, lon = self.weather.geocode()

        self.assertEqual(lat, 48.858260200000004)
        self.assertEqual(lon, 2.2944990543196795)

    # Test the weather API call
    @patch("requests.get")
    def test_get_weather(self, mock_get):
        # Mock the response from the API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "hourly": {
                "time": [
                    self.weather.current_time,
                    self.weather.current_time + timedelta(hours=1),
                ],
                "temperature_2m": [20, 22],
            }
        }

        weather_data = self.weather.get_weather(self.weather.current_time)

        self.assertEqual(
            weather_data,
            [
                (self.weather.current_time, 20),
                (self.weather.current_time + timedelta(hours=1), 22),
            ],
        )

    # Test the weather API call
    def test_update_building_outside_temperature(self):
        # Mock a Building object
        mock_building = unittest.mock.Mock()
        mock_building.outside_temperature = 20

        # Mock the weather data
        self.weather.weather_data = [(self.weather.current_time, 22)]

        self.weather.update_building_outside_temperature(mock_building, 60)

        # Check if the outside temperature of the building has been updated
        self.assertEqual(mock_building.outside_temperature, 22)


class TestSimulator(unittest.TestCase):
    """Test the simulator class."""

    @classmethod
    def setUpClass(cls):
        cls.weather = Weather("Fribourg, Suisse")

    # Set up a building with 20°C inside temperature, 24°C set temperature,
    # 10°C outside temperature,10m edge, 10 W/m^2K heat transfer coefficient,
    # 200 J/m^3K volume heat capacity, a boiler with 30000 W power, 50% operating
    # percentage and gas as fuel, a regulator and a weather object
    def setUp(self):
        self.boiler = Boiler(30000, 50, "gas")
        self.building = Building(
            20, 24, 10, 10, 10, 200, self.boiler, self.__class__.weather
        )
        self.regulator = Regulator()
        self.time_step = "hour"
        self.simulator = Simulator(
            self.boiler,
            self.building,
            self.regulator,
            self.time_step,
            built_in_screen=False,
        )

    # Test the simulator initialization
    def test_init(self):
        self.assertEqual(self.simulator.boiler, self.boiler)
        self.assertEqual(self.simulator.building, self.building)
        self.assertEqual(self.simulator.regulator, self.regulator)
        self.assertEqual(self.simulator.time_step, self.time_step)


if __name__ == "__main__":
    unittest.main()
