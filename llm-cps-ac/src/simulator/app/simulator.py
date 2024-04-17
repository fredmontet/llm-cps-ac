#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interactive simulation of heating in a building.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-10"
__version__ = "3.1"
__email__ = "philippe.marziale@edu.hefr.ch"


import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import app.constants as cst


class Simulator:
    """
    Class to manage the simulator's Tkinter window and all the simulation's elements.
    """

    # Class constants
    SLIDER_SIZE = 200
    SECOND_IN_MILLISECONDS = 1000

    def __init__(
        self,
        boiler,
        building,
        regulator,
        time_step,
        built_in_screen=False,
    ):
        """
        Initialize the simulator with boiler, building, regulator and weather objects.
        If built_in_screen is True, the size of figure elements is reduced.

        Args:
            boiler (Boiler): Boiler object
            building (Building): Building object
            regulator (Regulator): Regulator object
            time_step (int): Time step for the simulation in seconds
            built_in_screen (bool): If True, the size of figure elements is reduced
        """
        # Initialize the simulator's elements
        self.boiler = boiler
        self.building = building
        self.regulator = regulator
        self.time_step = time_step

        # Initialize the old values of the scales and variables
        self.old_temperature_scale = None
        self.old_outside_temperature_scale = None
        self.old_volume_heat_capacity_scale = None
        self.old_building_edge_scale = None
        self.old_heat_transfer_coefficient_scale = None
        self.old_boiler_power_scale = None
        # self.old_boiler_operating_percentage_scale = None
        self.old_fuel_var = None
        self.old_volume_heat_capacity_var = None
        self.old_time_step_var = None

        # Initialize the lists of values to display
        self.temperatures = [building.building_temperature]
        self.outside_temperatures = [building.outside_temperature]
        self.set_temperatures = [building.set_temperature]
        self.boiler_operating_percentages = [boiler.operating_percentage]

        # Create Tkinter window
        self.window = tk.Tk()
        self.window.title("Heating Simulator")

        # Make sure window is at the foreground at launch, then turn off
        self.window.attributes("-topmost", True)
        self.window.after(1, lambda: self.window.attributes("-topmost", False))

        # Create sliders
        self._create_sliders()

        # Create options
        self._create_options()

        # Create the matplotlib plot embedded in the Tkinter window
        self.fig, self.ax, self.ax2 = self._create_plot(built_in_screen)

        # Create labels to display current values
        self._create_labels()

        # Create quit button
        self.quit_button = tk.Button(self.window, text="Stop", command=self.window.quit)
        self.quit_button.pack(pady=10)

        # Start the update loop
        self.update()

        # Start Tkinter event loop
        self.window.mainloop()

    def _create_slider(self, parent, label, length, from_, to_, initial, resolution=1):
        """
        Create and configure a single slider with the given parameters.

        Args:
            parent (tk.Frame): Parent frame of the slider
            label (str): Label of the slider
            length (int): Length of the slider
            from_ (int): Minimum value of the slider
            to_ (int): Maximum value of the slider
            initial (int): Initial value of the slider
            resolution (int): Resolution of the slider
        """
        scale = tk.Scale(
            parent,
            from_=from_,
            to=to_,
            resolution=resolution,
            orient="horizontal",
            label=label,
            length=length,
        )
        scale.set(initial)
        scale.pack(side="left", padx=5, pady=5)
        return scale

    def _create_sliders(self):
        """
        Create and configure sliders for outside temperature, volume heat capacity, building edge, U coefficient, boiler power and boiler power scale.
        """
        sliders_frame = tk.Frame(self.window)
        sliders_frame.pack()

        self.set_temperature_scale = self._create_slider(
            sliders_frame,
            "Set temperature (°C)",
            self.SLIDER_SIZE,
            cst.MIN_SET_TEMPERATURE,
            cst.MAX_SET_TEMPERATURE,
            self.building.set_temperature,
        )
        self.outside_temperature_scale = self._create_slider(
            sliders_frame,
            "Outside temperature (°C)",
            self.SLIDER_SIZE - 40,
            cst.MIN_OUTSIDE_TEMPERATURE,
            cst.MAX_OUTSIDE_TEMPERATURE,
            self.building.outside_temperature,
        )

        # Create the building.use_real_weather button (next to the outside temperature slider)
        self.building.use_real_weather_button = tk.Button(
            sliders_frame,
            text="x",
            command=self.building.toggle_use_real_weather,
        )
        self.building.use_real_weather_button.pack(pady=25)

        sliders_frame_2 = tk.Frame(self.window)
        sliders_frame_2.pack()

        self.building_edge_scale = self._create_slider(
            sliders_frame_2,
            "Cube edge (m)",
            self.SLIDER_SIZE,
            cst.MIN_BUILDING_EDGE,
            cst.MAX_BUILDING_EDGE,
            self.building.building_edge,
        )

        self.heat_transfer_coefficient_scale = self._create_slider(
            sliders_frame_2,
            "U coefficient (W/m²*K)",
            self.SLIDER_SIZE,
            cst.MIN_HEAT_TRANSFER_COEFFICIENT,
            cst.MAX_HEAT_TRANSFER_COEFFICIENT,
            self.building.heat_transfer_coefficient,
            resolution=0.1,
        )

        sliders_frame_3 = tk.Frame(self.window)
        sliders_frame_3.pack()

        self.boiler_power_scale = self._create_slider(
            sliders_frame_3,
            "Boiler power (W)",
            self.SLIDER_SIZE,
            cst.MIN_BOILER_POWER,
            cst.MAX_BOILER_POWER,
            self.boiler.boiler_power,
        )

        self.volume_heat_capacity_scale = self._create_slider(
            sliders_frame_3,
            "Volume heat capacity (J/kg*K)",
            self.SLIDER_SIZE,
            cst.MIN_VOLUME_HEAT_CAPACITY,
            cst.MAX_VOLUME_HEAT_CAPACITY,
            self.building.volume_heat_capacity,
        )

        """ # Boiler operating percentage scale if there is no auto regulation
        self.boiler_operating_percentage_scale = self._create_slider(
            sliders_frame_3,
            "Operating percentage (%)",
            self.SLIDER_SIZE,
            0,
            100,
            self.boiler.operating_percentage,
        ) """

    def _update_volume_heat_capacity(self, choice):
        """
        Update the volume heat capacity slider based on the choice from the option menu.

        Args:
            choice (str): The chosen 'alimentation'
        """
        self.volume_heat_capacity_scale.set(cst.HEAT_CAPACITY[choice])

    def _create_options(self):
        """
        Create and configure an option menu for fuel, volume heat capacity and time step.
        """
        options_frame = tk.Frame(self.window)
        options_frame.pack()

        # Fuel choice option
        fuel_label = tk.Label(options_frame, text="Fuel choice:")
        fuel_label.grid(row=0, column=0)
        self.fuel_var = tk.StringVar(self.window)
        self.fuel_var.set(self.boiler.fuel)
        fuel_options = list(cst.FUEL_EFFICIENCIES.keys())
        self.fuel_optionmenu = tk.OptionMenu(
            options_frame, self.fuel_var, *fuel_options
        )
        self.fuel_optionmenu.grid(row=0, column=1, padx=10, pady=10)

        # Volume heat capacity choice
        volume_heat_capacity_label = tk.Label(
            options_frame, text="Volume heat capacity:"
        )
        volume_heat_capacity_label.grid(row=0, column=2)
        self.volume_heat_capacity_var = tk.StringVar(self.window)
        for key, value in cst.HEAT_CAPACITY.items():
            if value == self.building.volume_heat_capacity:
                self.volume_heat_capacity_var.set(key)
        volume_heat_capacity_options = list(cst.HEAT_CAPACITY.keys())
        self.volume_heat_capacity_optionmenu = tk.OptionMenu(
            options_frame,
            self.volume_heat_capacity_var,
            *volume_heat_capacity_options,
            command=self._update_volume_heat_capacity,
        )
        self.volume_heat_capacity_optionmenu.grid(row=0, column=3, padx=10, pady=10)

        # Time step choice
        time_step_label = tk.Label(options_frame, text="Time step (s):")
        time_step_label.grid(row=0, column=4)
        self.time_step_var = tk.StringVar(self.window)
        self.time_step_var.set(self.time_step)
        time_step_options = list(cst.TIME_STEP.keys())
        self.time_step_optionmenu = tk.OptionMenu(
            options_frame, self.time_step_var, *time_step_options
        )
        self.time_step_optionmenu.grid(row=0, column=5, padx=10, pady=10)

    def _create_plot(self, built_in_screen):
        """
        Create and configure the matplotlib plot embedded in the Tkinter window.

        Args:
            built_in_screen (bool): If True, the size of figure elements is reduced
        """
        fig, ax = plt.subplots(figsize=(3.9, 2.7) if built_in_screen else None)
        ax2 = ax.twinx()  # Create a twin Y axis sharing the X axis with ax
        graph = FigureCanvasTkAgg(fig, master=self.window)
        graph.get_tk_widget().pack()

        # Size control of figure elements
        if built_in_screen:
            plt.rc("font", size=6)
            plt.rc("axes", titlesize=6)
            plt.rc("axes", labelsize=6)
            plt.rc("xtick", labelsize=6)
            plt.rc("ytick", labelsize=6)
            plt.rc("legend", fontsize=6)
            plt.rc("figure", titlesize=6)
            plt.rc("lines", linewidth=0.8)

        return fig, ax, ax2

    def _create_label(self, parent, text, row, column):
        """
        Create and configure a single label with the given parameters.

        Args:
            parent (tk.Frame): Parent frame of the label.
            text (str): Text of the label.
            row (int): Row of the label in the parent frame.
            column (int): Column of the label in the parent frame.
        """
        label = tk.Label(parent, text=text)
        label.grid(row=row, column=column, padx=10)
        return label

    def _create_labels(self):
        """
        Create and configure labels to display current values.
        """
        labels_frame = tk.Frame(self.window)
        labels_frame.pack()

        self.building_temperature_label = self._create_label(
            labels_frame, f"Current building temperature:", 0, 0
        )
        self.reached_temperature_label = self._create_label(
            labels_frame, f"Temperature that will be reached:", 0, 1
        )
        self.boiler_operating_percentage_label = self._create_label(
            labels_frame, f"Boiler operating percentage:", 1, 0
        )
        self.building_outside_temperature_label = self._create_label(
            labels_frame, f"Outside temperature:", 1, 1
        )
        self.energy_consumption_label = self._create_label(
            labels_frame, f"Energy consumption:", 2, 0
        )
        self.boiler_heat_power_label = self._create_label(
            labels_frame, f"Current boiler heat power:", 2, 1
        )
        self.fuel_consumption_label = self._create_label(
            labels_frame, f"Fuel consumption:", 3, 0
        )
        self.energy_price_label = self._create_label(
            labels_frame, f"Energy price:", 3, 1
        )

    def _update_labels(self):
        """
        Update labels with the latest values.
        """
        self.building_temperature_label.config(
            text=f"Current building temperature: {self.building.building_temperature:.2f} °C"
        )
        self.reached_temperature_label.config(
            text=f"Temperature that will be reached: {self.building.calculate_temperature_reached():.2f} °C"
        )
        self.boiler_operating_percentage_label.config(
            text=f"Boiler operating percentage: {self.boiler.operating_percentage:.2f} %"
        )
        self.building_outside_temperature_label.config(
            text=f"Outside temperature: {self.building.outside_temperature:.2f} °C"
        )
        self.energy_consumption_label.config(
            text=f"Energy consumption: {self.building.calculate_energy_consumption_kWh():.2f} kWh"
        )
        self.boiler_heat_power_label.config(
            text=f"Current boiler heat power: {self.boiler.current_power:.2f} W"
        )
        self.fuel_consumption_label.config(
            text=f"Fuel consumption: {self.boiler.calculate_fuel_consumption():.2f} kg/h or m³/h or kWh"
        )
        self.energy_price_label.config(
            text=f"Energy price: {self.boiler.calculate_fuel_price_per_year():.2f} CHF/year"
        )

    def _update_graph(self):
        """
        Update the graph with the latest temperatures.
        """
        self.ax.clear()
        self.ax2.clear()

        self.ax.set_title("Building temperature evolution")
        self.ax.plot(self.temperatures, label="Building temperature", color="red")
        self.ax.plot(
            self.set_temperatures,
            label="Set temperature",
            color="orange",
            linestyle="dashed",
        )
        self.ax.plot(
            self.outside_temperatures,
            label="Outside temperature",
            color="skyblue",
            linestyle="dotted",
        )
        if self.time_step == "minute":
            self.ax.set_xlabel("Time (minutes)")
        elif self.time_step == "hour":
            self.ax.set_xlabel("Time (hours)")
        else:
            self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperature (°C)")

        self.ax2.plot(
            self.boiler_operating_percentages,
            label="Boiler operating percentage",
            color="grey",
            linestyle="dotted",
        )
        self.ax2.set_ylim(0, 100)
        self.ax2.set_ylabel("Boiler operating percentage (%)", color="grey")
        self.ax2.yaxis.set_label_coords(1.1, 0.5)  # Shift the y-axis label to the right
        self.ax2.tick_params(axis="y", labelcolor="grey")

        # Combine legends
        lines, labels = self.ax.get_legend_handles_labels()
        lines2, labels2 = self.ax2.get_legend_handles_labels()
        self.ax.legend(lines + lines2, labels + labels2, loc="upper left")

        self.ax.grid(True)
        self.fig.canvas.draw()

    def _update_attribute(self, obj, attr_name, new_value, old_value):
        """
        Update an attribute of an object with his new value (from the scale or the variable).
        Use to correctly update the value when the attribute is changed by another method (e.g. FastAPI).
        """
        current_value = new_value.get()
        if old_value != current_value:
            setattr(obj, attr_name, current_value)
        elif getattr(obj, attr_name) != current_value:
            new_value.set(getattr(obj, attr_name))
        return current_value

    def update(self):
        """
        Update building and boiler parameters, calculate new building temperature, update the plot and labels.
        Repeat every second.
        """
        # Update building, boiler parameters and interface
        self.old_temperature_scale = self._update_attribute(
            self.building,
            "set_temperature",
            self.set_temperature_scale,
            self.old_temperature_scale,
        )
        self.old_outside_temperature_scale = self._update_attribute(
            self.building,
            "outside_temperature",
            self.outside_temperature_scale,
            self.old_outside_temperature_scale,
        )
        self.old_volume_heat_capacity_scale = self._update_attribute(
            self.building,
            "volume_heat_capacity",
            self.volume_heat_capacity_scale,
            self.old_volume_heat_capacity_scale,
        )
        self.old_building_edge_scale = self._update_attribute(
            self.building,
            "building_edge",
            self.building_edge_scale,
            self.old_building_edge_scale,
        )
        self.old_heat_transfer_coefficient_scale = self._update_attribute(
            self.building,
            "heat_transfer_coefficient",
            self.heat_transfer_coefficient_scale,
            self.old_heat_transfer_coefficient_scale,
        )
        self.old_boiler_power_scale = self._update_attribute(
            self.boiler,
            "boiler_power",
            self.boiler_power_scale,
            self.old_boiler_power_scale,
        )
        """ # Boiler operating percentage scale if there is no auto regulation
        self.old_boiler_operating_percentage_scale = self._update_attribute(
            self.boiler,
            "operating_percentage",
            self.boiler_operating_percentage_scale,
            self.old_boiler_operating_percentage_scale,
        ) """
        self.old_fuel_var = self._update_attribute(
            self.boiler, "fuel", self.fuel_var, self.old_fuel_var
        )
        self.old_volume_heat_capacity_var = self._update_attribute(
            self.building,
            "volume_heat_capacity_var",
            self.volume_heat_capacity_var,
            self.old_volume_heat_capacity_var,
        )
        self.old_time_step_var = self._update_attribute(
            self, "time_step", self.time_step_var, self.old_time_step_var
        )

        # Update the old values
        self.old_temperature_scale = self.set_temperature_scale.get()
        self.old_outside_temperature_scale = self.outside_temperature_scale.get()
        self.old_volume_heat_capacity_scale = self.volume_heat_capacity_scale.get()
        self.old_building_edge_scale = self.building_edge_scale.get()
        self.old_heat_transfer_coefficient_scale = (
            self.heat_transfer_coefficient_scale.get()
        )
        self.old_boiler_power_scale = self.boiler_power_scale.get()
        # self.old_boiler_operating_percentage_scale = self.boiler_operating_percentage_scale.get()
        self.old_fuel_var = self.fuel_var.get()
        self.old_volume_heat_capacity_var = self.volume_heat_capacity_var.get()
        self.old_time_step_var = self.time_step_var.get()

        # Update outside temperature (if we use real weather data)
        if self.building.use_real_weather:
            self.building.weather.update_building_outside_temperature(
                self.building, cst.TIME_STEP[self.time_step]
            )

        # Regulate boiler
        self.regulator.regulate_temperature(self.building)

        # Calculate new building temperature
        self.building.update_temperature(self.time_step)

        # Add the new temperature to the temperature list
        self.temperatures.append(self.building.building_temperature)
        self.outside_temperatures.append(self.building.outside_temperature)
        self.set_temperatures.append(self.building.set_temperature)
        self.boiler_operating_percentages.append(self.boiler.operating_percentage)

        # Update use_real_weather button
        if self.building.use_real_weather:
            self.building.use_real_weather_button.configure(text="☀")
        else:
            self.building.use_real_weather_button.configure(text="☼")

        # Update the graph
        self._update_graph()

        # Update labels
        self._update_labels()

        # Update window every second
        self.window.after(self.SECOND_IN_MILLISECONDS, self.update)
