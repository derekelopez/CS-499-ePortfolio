"""
MongoDB access for the enhanced smart thermostat.

This module manages the MongoDB connection and provides
database operations for thermostat telemetry.
"""

import os
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://127.0.0.1:27017/",
)

DATABASE_NAME = "smart_thermostat"
READINGS_COLLECTION = "readings"


class ThermostatDatabase:
    """
    Manage MongoDB operations for thermostat telemetry.
    """

    def __init__(self, uri=MONGODB_URI):
        self.client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
        )

        self.database = self.client[DATABASE_NAME]
        self.readings = self.database[READINGS_COLLECTION]

    def test_connection(self):
        """
        Verify that MongoDB is reachable.

        Returns:
            bool: True when the database connection succeeds.
        """

        try:
            self.client.admin.command("ping")
            return True

        except PyMongoError as error:
            print(f"MongoDB connection error: {error}")
            return False

    def insert_reading(self, data):
        """
        Store one validated thermostat reading.

        Returns:
            str or None: Inserted document ID when successful.
        """

        try:
            document = data.copy()

            document["timestamp"] = datetime.fromisoformat(document["timestamp"])

            result = self.readings.insert_one(document)

            return str(result.inserted_id)

        except (PyMongoError, ValueError) as error:
            print(f"MongoDB insert error: {error}")
            return None

    def get_recent_readings(self, limit=20):
        """
        Return the most recent thermostat readings.
        """

        try:
            cursor = self.readings.find({}).sort("timestamp", -1).limit(limit)

            readings = []

            for document in cursor:
                document["_id"] = str(document["_id"])

                if isinstance(document.get("timestamp"), datetime):
                    document["timestamp"] = document["timestamp"].isoformat()

                readings.append(document)

            return readings

        except PyMongoError as error:
            print(f"MongoDB read error: {error}")
            return None

    def get_readings_by_date_range(self, start_time, end_time):
        """
        Return thermostat readings within a timestamp range.
        """

        try:
            start_datetime = datetime.fromisoformat(start_time)
            end_datetime = datetime.fromisoformat(end_time)

            cursor = self.readings.find(
                {
                    "timestamp": {
                        "$gte": start_datetime,
                        "$lte": end_datetime,
                    }
                }
            ).sort("timestamp", 1)

            readings = []

            for document in cursor:
                document["_id"] = str(document["_id"])

                if isinstance(document.get("timestamp"), datetime):
                    document["timestamp"] = document["timestamp"].isoformat()

                readings.append(document)

            return readings

        except (PyMongoError, ValueError) as error:
            print(f"MongoDB date-range read error: {error}")
            return None

    def get_statistics(self, start_time=None, end_time=None):
        """
        Return aggregate statistics for stored thermostat readings.
        """

        try:
            match_filter = {}

            if start_time is not None and end_time is not None:
                start_datetime = datetime.fromisoformat(start_time)
                end_datetime = datetime.fromisoformat(end_time)

                match_filter = {
                    "timestamp": {
                        "$gte": start_datetime,
                        "$lte": end_datetime,
                    }
                }

            pipeline = []

            if match_filter:
                pipeline.append({"$match": match_filter})

            pipeline.append(
                {
                    "$group": {
                        "_id": None,
                        "total_readings": {"$sum": 1},
                        "min_temperature_f": {"$min": "$temperature_f"},
                        "max_temperature_f": {"$max": "$temperature_f"},
                        "average_temperature_f": {"$avg": "$temperature_f"},
                        "average_humidity": {"$avg": "$humidity"},
                    }
                }
            )

            results = list(self.readings.aggregate(pipeline))

            if not results:
                return {
                    "total_readings": 0,
                    "min_temperature_f": None,
                    "max_temperature_f": None,
                    "average_temperature_f": None,
                    "average_humidity": None,
                    "state_counts": {
                        "OFF": 0,
                        "HEAT": 0,
                        "COOL": 0,
                    },
                    "state_durations_seconds": {
                        "OFF": 0.0,
                        "HEAT": 0.0,
                        "COOL": 0.0,
                    },
                }

            statistics = results[0]
            statistics.pop("_id", None)

            if statistics["average_temperature_f"] is not None:
                statistics["average_temperature_f"] = round(
                    statistics["average_temperature_f"],
                    2,
                )

            if statistics["average_humidity"] is not None:
                statistics["average_humidity"] = round(
                    statistics["average_humidity"],
                    2,
                )

            state_pipeline = []

            if match_filter:
                state_pipeline.append({"$match": match_filter})

            state_pipeline.append(
                {
                    "$group": {
                        "_id": "$state",
                        "count": {"$sum": 1},
                    }
                }
            )

            state_counts = {
                "OFF": 0,
                "HEAT": 0,
                "COOL": 0,
            }

            for result in self.readings.aggregate(state_pipeline):
                state = result["_id"]

                if state in state_counts:
                    state_counts[state] = result["count"]

            statistics["state_counts"] = state_counts

            state_durations = self.get_state_durations(
                start_time,
                end_time,
            )

            if state_durations is None:
                return None

            statistics["state_durations_seconds"] = state_durations
            

            return statistics

        except (PyMongoError, ValueError) as error:
            print(f"MongoDB statistics error: {error}")
            return None


    def get_state_durations(self, start_time=None, end_time=None):
        """
        Estimate time spent in each thermostat state.

        Duration is calculated from the time between each reading
        and the following reading.
        """

        try:
            match_filter = {}

            if start_time is not None and end_time is not None:
                start_datetime = datetime.fromisoformat(start_time)
                end_datetime = datetime.fromisoformat(end_time)

                match_filter = {
                    "timestamp": {
                        "$gte": start_datetime,
                        "$lte": end_datetime,
                    }
                }

            pipeline = []

            if match_filter:
                pipeline.append({"$match": match_filter})

            pipeline.extend(
                [
                    {
                        "$setWindowFields": {
                            "sortBy": {
                                "timestamp": 1
                            },
                            "output": {
                                "next_timestamp": {
                                    "$shift": {
                                        "output": "$timestamp",
                                        "by": 1,
                                    }
                                }
                            },
                        }
                    },
                    {
                        "$match": {
                            "next_timestamp": {
                                "$ne": None
                            }
                        }
                    },
                    {
                        "$project": {
                            "state": 1,
                            "duration_seconds": {
                                "$divide": [
                                    {
                                        "$subtract": [
                                            "$next_timestamp",
                                            "$timestamp",
                                        ]
                                    },
                                    1000,
                                ]
                            },
                        }
                    },
                    {
                        "$group": {
                            "_id": "$state",
                            "seconds": {
                                "$sum": "$duration_seconds"
                            },
                        }
                    },
                ]
            )

            state_durations = {
                "OFF": 0.0,
                "HEAT": 0.0,
                "COOL": 0.0,
            }

            for result in self.readings.aggregate(pipeline):
                state = result["_id"]

                if state in state_durations:
                    state_durations[state] = round(
                        result["seconds"],
                        2,
                    )

            return state_durations

        except (PyMongoError, ValueError) as error:
            print(f"MongoDB state-duration error: {error}")
            return None

    

    def close(self):
        """
        Close the MongoDB connection.
        """

        self.client.close()
