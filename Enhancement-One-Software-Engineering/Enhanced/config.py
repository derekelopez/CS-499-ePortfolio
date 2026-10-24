"""
Configuration settings for the enhanced smart thermostat.
Keeping hardware pins, setpoint limits, serial settings,
and timing values in one location makes the application
easier to maintain.
"""

#----------------------------------------------------------
# Thermostat settings
#----------------------------------------------------------

DEFAULT_SETPOINT = 72

MIN_SETPOINT = 50
MAX_SETPOINT = 90


#----------------------------------------------------------
# LED GPIO pins
#----------------------------------------------------------

RED_LED_PIN = 18
BLUE_LED_PIN = 23


#----------------------------------------------------------
# Button GPIO pins
#----------------------------------------------------------

STATE_BUTTON_PIN = 24
INCREASE_BUTTON_PIN = 25
DECREASE_BUTTON_PIN = 12


#----------------------------------------------------------
# LCD configuration
#----------------------------------------------------------

LCD_COLUMNS = 16
LCD_ROWS = 2

LCD_RS_PIN = 17
LCD_EN_PIN = 27
LCD_D4_PIN = 5
LCD_D5_PIN = 6
LCD_D6_PIN = 13
LCD_D7_PIN = 26

#----------------------------------------------------------
# Serial communication
#----------------------------------------------------------

SERIAL_PORT = "/dev/ttyS0"
SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 1


#----------------------------------------------------------
# Timing intervals
#----------------------------------------------------------

MAIN_LOOP_INTERVAL = 1
TELEMETRY_INTERVAL = 30
#----------------------------------------------------------
# Sensor validation
#----------------------------------------------------------

MIN_VALID_TEMPERATURE_F = -40
MAX_VALID_TEMPERATURE_F = 150

MIN_VALID_HUMIDITY = 0
MAX_VALID_HUMIDITY = 100

# ----------------------------------------------------------
# API communication
# ----------------------------------------------------------

TELEMETRY_URL = "http://10.0.0.187:5000/api/readings"
HTTP_TIMEOUT = 5