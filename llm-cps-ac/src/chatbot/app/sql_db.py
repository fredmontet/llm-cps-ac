#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQL database for the chatbot with the possibility to initialize it.
"""

__author__ = "Philippe Marziale"
__copyright__ = "Copyright 2023, School of Engineering and Architecture of Fribourg"
__license__ = "SPDX-License-Identifier: Apache-2.0"
__date__ = "2023-07-04"
__version__ = "1.0"
__email__ = "philippe.marziale@edu.hefr.ch"


from datetime import time

from app.config import Config

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Enum,
    Time,
    Table,
    ForeignKey,
    create_engine,
    inspect,
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


# Construct a base class for declarative class definitions
Base = declarative_base()


class Day(Enum):
    """
    Enum class representing the days of the week.
    """

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


# Association table for User and their PresenceHours
user_schedule = Table(
    "user_schedule",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("presence_hours_id", Integer, ForeignKey("presence_hours.id")),
)


class User(Base):
    """
    The User class represents the users table in the database.

    Each user has an id, name, age, preferred_temperature, and a schedule which
    is a relationship to the PresenceHours table.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    preferred_temperature = Column(Float)
    schedule = relationship(
        "PresenceHours", secondary=user_schedule, back_populates="users"
    )

    def to_json(self):
        """
        Converts the User object to a JSON format.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "preferredTemperature": self.preferred_temperature,
            "schedule": [sh.to_json() for sh in self.schedule],
        }


class PresenceHours(Base):
    """
    The PresenceHours class represents the presence_hours table in the database.

    Each presence_hours has an id, day (Enum), start_time, end_time, and a users
    which is a relationship to the User table.
    """

    __tablename__ = "presence_hours"
    id = Column(Integer, primary_key=True)
    day = Column(
        Enum(
            Day.MONDAY,
            Day.TUESDAY,
            Day.WEDNESDAY,
            Day.THURSDAY,
            Day.FRIDAY,
            Day.SATURDAY,
            Day.SUNDAY,
        )
    )
    start_time = Column(Time)
    end_time = Column(Time)
    users = relationship("User", secondary=user_schedule, back_populates="schedule")

    def to_json(self):
        """
        Converts the PresenceHours object to a JSON format.
        """
        return {
            "id": self.id,
            "day": self.day,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }


def create_schedule(user_data, days):
    """
    Helper function to create a schedule for given user data and days.
    """
    schedule = []
    start_time = user_data["start_time"]
    end_time = user_data["end_time"]

    # Create a PresenceHours object for each day with the start and end time
    for day in days:
        presence_hours = PresenceHours(
            day=day, start_time=start_time, end_time=end_time
        )
        schedule.append(presence_hours)

    return schedule


def init_db():
    """
    Function to initialize the database. It creates the tables and populates them with initial data.
    """
    # Check if the database is already initialized with the 'users' table
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        # Create the tables
        Base.metadata.create_all(bind=engine)

        with Session() as session:
            try:
                # Define the users data
                users_data = [
                    {
                        "name": "Steve",
                        "age": 28,
                        "preferred_temperature": 19,
                        "weekday_schedule": {
                            "start_time": time(7, 0),
                            "end_time": time(17, 0),
                        },
                        "weekend_schedule": {
                            "start_time": time(9, 0),
                            "end_time": time(23, 0),
                        },
                    },
                    {
                        "name": "Marie",
                        "age": 31,
                        "preferred_temperature": 20,
                        "weekday_schedule": {
                            "start_time": time(6, 30),
                            "end_time": time(16, 0),
                        },
                        "weekend_schedule": {
                            "start_time": time(8, 30),
                            "end_time": time(22, 30),
                        },
                    },
                ]

                # Create User instances
                for user_data in users_data:
                    user = User(
                        name=user_data["name"],
                        age=user_data["age"],
                        preferred_temperature=user_data["preferred_temperature"],
                    )

                    # Define separate schedules for weekdays and weekends
                    weekday_schedule = user_data["weekday_schedule"]
                    weekend_schedule = user_data["weekend_schedule"]

                    weekdays = [
                        Day.MONDAY,
                        Day.TUESDAY,
                        Day.WEDNESDAY,
                        Day.THURSDAY,
                        Day.FRIDAY,
                    ]
                    weekends = [Day.SATURDAY, Day.SUNDAY]

                    user.schedule.extend(create_schedule(weekday_schedule, weekdays))
                    user.schedule.extend(create_schedule(weekend_schedule, weekends))

                    # Add the user to the session
                    session.add(user)

                # Commit the changes
                session.commit()

            except Exception as e:
                # Rollback the changes if an error occurs
                session.rollback()
                print(f"Failed to initialize database. Error: {str(e)}")

            finally:
                # Close the session
                session.close()


# Setting up the engine and session
engine = create_engine(f"sqlite:///{Config.SQL_DB_PATH}")
Session = sessionmaker(bind=engine)
