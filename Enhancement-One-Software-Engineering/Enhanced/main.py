"""
Main application for the enhanced Raspberry Pi smart thermostat.

This module coordinates the thermostat logic and Raspberry Pi hardware.
"""

import time
from queue import Empty, Queue

from .config import (
    DEFAULT_SETPOINT,
    MIN_SETPOINT,
    MAX_SETPOINT,
    MAIN_LOOP_INTERVAL,
    TELEMETRY_INTERVAL,
)

from .hardware_pi import PiHardware
from .telemetry_client import TelemetryClient
from .thermostat_core import ThermostatController


def process_commands(controller, command_queue):
    """
    Process all pending button commands.
    """

    while True:
        try:
            command = command_queue.get_nowait()

        except Empty:
            break

        if command == "cycle":
            controller.cycle_state()

        elif command == "increase":
            controller.increase_setpoint()

        elif command == "decrease":
            controller.decrease_setpoint()


def main():
    """
    Run the smart thermostat application.
    """

    command_queue = Queue()
    hardware = None

    telemetry_client = TelemetryClient()
    last_telemetry_time = 0.0

    try:
        # -------------------------------------------------
        # Create thermostat controller
        # -------------------------------------------------
        controller = ThermostatController(
            setpoint=DEFAULT_SETPOINT,
            min_setpoint=MIN_SETPOINT,
            max_setpoint=MAX_SETPOINT,
        )

        # -------------------------------------------------
        # Initialize Raspberry Pi hardware
        # -------------------------------------------------
        hardware = PiHardware()

        # Register button callbacks
        hardware.register_button_callbacks(command_queue)

        # -------------------------------------------------
        # Main thermostat loop
        # -------------------------------------------------
        while True:
            # Process button commands
            process_commands(
                controller,
                command_queue,
            )

            # Read AHT20 sensor
            temperature_f, humidity = hardware.read_environment()

            # Determine LED behavior
            light_command = controller.evaluate(temperature_f)

            # Apply LED command
            hardware.apply_lights(light_command)

            # Get current thermostat state
            state = controller.state.value.upper()

            # -------------------------------------------------
            # LCD display
            # -------------------------------------------------
            line1 = f"{temperature_f:.1f}F {humidity:.0f}%"
            line2 = f"{state} SP:{controller.setpoint}F"

            hardware.update_display(
                line1,
                line2,
            )

            # -------------------------------------------------
            # Serial output
            # -------------------------------------------------
            serial_message = (
                f"Temperature: {temperature_f:.2f} F, "
                f"Humidity: {humidity:.2f}%, "
                f"Setpoint: {controller.setpoint} F, "
                f"State: {state}\n"
            )

            hardware.write_serial(serial_message)

            # -------------------------------------------------
            # Telemetry
            # -------------------------------------------------
            current_time = time.monotonic()

            if current_time - last_telemetry_time >= TELEMETRY_INTERVAL:
                sent = telemetry_client.send_reading(
                    temperature_f=temperature_f,
                    humidity=humidity,
                    setpoint=controller.setpoint,
                    state=state,
                )

                if sent:
                    print("Telemetry reading sent successfully.")

                last_telemetry_time = current_time

            # Wait before next reading
            time.sleep(MAIN_LOOP_INTERVAL)

    except KeyboardInterrupt:
        print("\nThermostat stopped by user.")

    except Exception as error:
        print(f"Thermostat error: {error}")

    finally:
        if hardware is not None:
            hardware.cleanup()


if __name__ == "__main__":
    main()
