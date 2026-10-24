from dataclasses import dataclass
from enum import Enum
from math import isfinite

class ThermostatState(str, Enum):
    """Operating modes supported by the thermostat."""

    OFF = "off"
    HEAT = "heat"
    COOL = "cool"

@dataclass(frozen=True)
class LightCommand:
    """Describes what the red and blue LEDs should do.
    Possible values: off, pulse, solid"""
    red: str
    blue: str

class ThermostatController:
    """Hardware-independent thermostat control logic.
    This class does not directly access Raspberry Pi GPIO,
    sensors, LEDs, buttons, the LCD, or serial communication."""

    def __init__(
            self,
            setpoint = 72,
            min_setpoint = 50,
            max_setpoint = 90
    ):
        if min_setpoint > max_setpoint:
            raise ValueError(
                "Minimum setpoint cannot be greater than maximum setpoint."
            )

        if not min_setpoint <= setpoint <= max_setpoint:
            raise ValueError(
                "Initial setpoint is ouside the allowed range."
            )

        self.state = ThermostatState.OFF
        self.setpoint = setpoint
        self.min_setpoint = min_setpoint
        self.max_setpoint = max_setpoint

    def cycle_state(self):
        """Cyle through off -> heat -> cool -> off"""

        order = [
            ThermostatState.OFF,
            ThermostatState.HEAT,
            ThermostatState.COOL
        ]

        current_index = order.index(self.state)

        self.state = order[
            (current_index + 1) % len(order)
        ]

        return self.state

    def increase_setpoint(self):
        """Increase the setpoint by one degree without exceeding
        the maximum allowed value."""

        self.setpoint = min(
            self.setpoint + 1,
            self.max_setpoint
        )

        return self.setpoint

    def decrease_setpoint(self):
        """Decrease the setpoint by one degree without going below 
        the minimum allowed value."""

        self.setpoint = max(
            self.setpoint - 1,
            self.min_setpoint
        )

        return self.setpoint

    def evaluate(self, temperature_f):
        """Determine the LED behavior based on the
        current thermostat state and temperature."""

        if isinstance(temperature_f, bool) or not isinstance(
            temperature_f, (int, float)
        ):
            raise TypeError(
                "temperature_f must be a numeric value."
            )
        if not isfinite(temperature_f):
            raise ValueError(
                "temperature_f must be a finite value."
            )

        if not -40 <= temperature_f <= 150:
            raise ValueError(
                "temperature_f is outside the expected range."
            )

        if self.state == ThermostatState.OFF:
            return LightCommand(
                red = "off",
                blue = "off"
            )

        if self.state == ThermostatState.HEAT:
            if temperature_f < self.setpoint:
                return LightCommand(
                    red = "pulse",
                    blue = "off"
                )

            return LightCommand(
                red = "solid",
                blue = "off"
            )

        if self.state == ThermostatState.COOL:
            if temperature_f > self.setpoint:
                return LightCommand(
                    red = "off",
                    blue = "pulse"
                )

            return LightCommand(
                red = "off",
                blue = "solid"
            )
        raise ValueError(
            f"Unsupported thermostat state: {self.state}"
        )
        