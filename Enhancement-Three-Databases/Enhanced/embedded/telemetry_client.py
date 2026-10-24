"""
Telemetry client for the enhanced smart thermostat.

This module sends thermostat readings to the server API.
Database access is handled by the server rather than directly
by the Raspberry Pi thermostat application.
"""

from datetime import datetime, timezone

import requests

from .config import (
    TELEMETRY_URL,
    HTTP_TIMEOUT,
    MIN_VALID_TEMPERATURE_F,
    MAX_VALID_TEMPERATURE_F,
    MIN_VALID_HUMIDITY,
    MAX_VALID_HUMIDITY,
)


class TelemetryClient:
    """
    Sends thermostat telemetry data to the server API.
    """

    def __init__(self, url=TELEMETRY_URL, timeout=HTTP_TIMEOUT):
        self.url = url
        self.timeout = timeout

    def build_payload(
        self,
        temperature_f,
        humidity,
        setpoint,
        state,
    ):
        """
        Create and validate a thermostat telemetry payload.

        Returns:
            dict: Validated thermostat reading.
        """

        if not MIN_VALID_TEMPERATURE_F <= temperature_f <= MAX_VALID_TEMPERATURE_F:
            raise ValueError(
                f"Temperature must be between "
                f"{MIN_VALID_TEMPERATURE_F} and "
                f"{MAX_VALID_TEMPERATURE_F} degrees Fahrenheit."
            )

        if not MIN_VALID_HUMIDITY <= humidity <= MAX_VALID_HUMIDITY:
            raise ValueError(
                f"Humidity must be between "
                f"{MIN_VALID_HUMIDITY} and "
                f"{MAX_VALID_HUMIDITY} percent."
            )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature_f": round(float(temperature_f), 2),
            "humidity": round(float(humidity), 2),
            "setpoint": int(setpoint),
            "state": str(state).upper(),
        }

    def send_reading(
        self,
        temperature_f,
        humidity,
        setpoint,
        state,
    ):
        """
        Send one thermostat reading to the server.

        Returns:
            bool: True if the server accepted the reading,
            otherwise False.
        """

        try:
            payload = self.build_payload(
                temperature_f,
                humidity,
                setpoint,
                state,
            )

            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return True

        except ValueError as error:
            print(f"Telemetry validation error: {error}")
            return False

        except requests.RequestException as error:
            print(f"Telemetry connection error: {error}")
            return False