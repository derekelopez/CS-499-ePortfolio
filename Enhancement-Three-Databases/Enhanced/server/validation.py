"""
Validation functions for smart thermostat telemetry.

This module validates incoming thermostat readings before
they are stored in the database.
"""

from datetime import datetime

REQUIRED_FIELDS = {
    "timestamp",
    "temperature_f",
    "humidity",
    "setpoint",
    "state",
}

VALID_STATES = {
    "OFF",
    "HEAT",
    "COOL",
}

MIN_TEMPERATURE_F = -40
MAX_TEMPERATURE_F = 150

MIN_HUMIDITY = 0
MAX_HUMIDITY = 100

MIN_SETPOINT = 50
MAX_SETPOINT = 90


def is_number(value):
    """
    Return True when the value is an integer or float,
    but not a Boolean.
    """

    return isinstance(value, (int, float)) and not isinstance(value, bool)



def validate_reading(data):
    """
    Validate an incoming thermostat telemetry reading.

    Returns:
        list: Validation error messages. An empty list means
        the reading is valid.
    """

    errors = []

    if not isinstance(data, dict):
        return ["Telemetry data must be a JSON object."]

    # ---------------------------------------------------------
    # Required fields
    # ---------------------------------------------------------
    missing_fields = REQUIRED_FIELDS - data.keys()

    if missing_fields:
        errors.append("Missing required fields: " + ", ".join(sorted(missing_fields)))

        return errors

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------
    timestamp = data["timestamp"]

    if not isinstance(timestamp, str):
        errors.append("Timestamp must be a string.")

    else:
        try:
            parsed_timestamp = datetime.fromisoformat(timestamp)

            if parsed_timestamp.tzinfo is None:
                errors.append("Timestamp must include timezone information.")

        except ValueError:
            errors.append("Timestamp must use a valid ISO 8601 format.")

    # ---------------------------------------------------------
    # Temperature
    # ---------------------------------------------------------
    temperature = data["temperature_f"]

    if not is_number(temperature):
        errors.append("Temperature must be numeric.")

    elif not MIN_TEMPERATURE_F <= temperature <= MAX_TEMPERATURE_F:
        errors.append(
            f"Temperature must be between "
            f"{MIN_TEMPERATURE_F} and "
            f"{MAX_TEMPERATURE_F} degrees Fahrenheit."
        )

    # ---------------------------------------------------------
    # Humidity
    # ---------------------------------------------------------
    humidity = data["humidity"]

    if not is_number(humidity):
        errors.append("Humidity must be numeric.")

    elif not MIN_HUMIDITY <= humidity <= MAX_HUMIDITY:
        errors.append(
            f"Humidity must be between "
            f"{MIN_HUMIDITY} and "
            f"{MAX_HUMIDITY} percent."
        )

    # ---------------------------------------------------------
    # Setpoint
    # ---------------------------------------------------------
    setpoint = data["setpoint"]

    if not is_number(setpoint):
        errors.append("Setpoint must be numeric.")

    elif not MIN_SETPOINT <= setpoint <= MAX_SETPOINT:
        errors.append(
            f"Setpoint must be between "
            f"{MIN_SETPOINT} and "
            f"{MAX_SETPOINT} degrees Fahrenheit."
        )

    # ---------------------------------------------------------
    # Thermostat state
    # ---------------------------------------------------------
    state = data["state"]

    if not isinstance(state, str):
        errors.append("State must be a string.")

    elif state.upper() not in VALID_STATES:
        errors.append("State must be OFF, HEAT, or COOL.")

    return errors
