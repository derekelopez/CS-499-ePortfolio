import pytest

from embedded.thermostat_core import (
    ThermostatController,
    ThermostatState,
)

def test_default_state_and_setpoint():
    thermostat = ThermostatController()

    assert thermostat.state == ThermostatState.OFF
    assert thermostat.setpoint == 72

def test_cycle_order():
    thermostat = ThermostatController()

    assert thermostat.cycle_state() == ThermostatState.HEAT
    assert thermostat.cycle_state() == ThermostatState.COOL
    assert thermostat.cycle_state() == ThermostatState.OFF


def test_setpoint_increase():
    thermostat = ThermostatController(setpoint = 72)

    assert thermostat.increase_setpoint() == 73


def test_setpoint_decrease():
    thermostat = ThermostatController(setpoint = 72)

    assert thermostat.decrease_setpoint() == 71


def test_maximum_setpoint_limit():
    thermostat = ThermostatController(setpoint = 90)

    assert thermostat.increase_setpoint() == 90


def test_minimum_setpoint_limit():
    thermostat = ThermostatController(setpoint = 50)

    assert thermostat.decrease_setpoint() == 50


def test_heat_below_setpoint():
    thermostat = ThermostatController(setpoint = 72)

    thermostat.cycle_state()

    command = thermostat.evaluate(70.5)

    assert command.red == "pulse"
    assert command.blue == "off"


def test_heat_at_setpoint():
    thermostat = ThermostatController(setpoint = 72)

    thermostat.cycle_state()

    command = thermostat.evaluate(72.0)

    assert command.red == "solid"
    assert command.blue == "off"


def test_cool_above_setpoint():
    thermostat = ThermostatController(setpoint = 72)

    thermostat.cycle_state()
    thermostat.cycle_state()

    command = thermostat.evaluate(75.2)

    assert command.red == "off"
    assert command.blue == "pulse"


def test_cool_at_setpoint():
    thermostat = ThermostatController(setpoint = 72)

    thermostat.cycle_state()
    thermostat.cycle_state()

    command = thermostat.evaluate(72.0)

    assert command.red == "off"
    assert command.blue == "solid"


def test_off_turns_both_lights_off():
    thermostat = ThermostatController()

    command = thermostat.evaluate(72.0)

    assert command.red == "off"
    assert command.blue == "off"


def test_invalid_temperature_rejected():
    thermostat = ThermostatController()

    with pytest.raises(ValueError):
        thermostat.evaluate(500)


def test_non_numeric_temperature_rejected():
    thermostat = ThermostatController()

    with pytest.raises(TypeError):
        thermostat.evaluate("hot")