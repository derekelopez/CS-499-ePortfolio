"""
Raspberry Pi hardware interface for the enhanced smart thermostat.
This module contains all the Raspberry Pi specific hardware access.
The thermostat decision logic is in thermostat_core.py.
"""

import board
import digitalio
import adafruit_ahtx0
import adafruit_character_lcd.character_lcd as characterlcd
import serial

from gpiozero import Button, PWMLED

from .config import (
    RED_LED_PIN,
    BLUE_LED_PIN,
    STATE_BUTTON_PIN,
    INCREASE_BUTTON_PIN,
    DECREASE_BUTTON_PIN,
    LCD_COLUMNS,
    LCD_ROWS,
    LCD_RS_PIN,
    LCD_EN_PIN,
    LCD_D4_PIN,
    LCD_D5_PIN,
    LCD_D6_PIN,
    LCD_D7_PIN,
    SERIAL_PORT,
    SERIAL_BAUDRATE,
    SERIAL_TIMEOUT,
)


class PiHardware:
    """
    Handles all Raspberry Pi hardware for the thermostat.
    """

    def __init__(self):
        # ----------------------------------------------------------
        # AHT20 temperature and humidity sensor
        # ----------------------------------------------------------
        self.i2c = board.I2C()
        self.sensor = adafruit_ahtx0.AHTx0(self.i2c)

        # ----------------------------------------------------------
        # LEDs
        # ----------------------------------------------------------
        self.red_led = PWMLED(RED_LED_PIN)
        self.blue_led = PWMLED(BLUE_LED_PIN)

        # ----------------------------------------------------------
        # Buttons
        # ----------------------------------------------------------
        self.state_button = Button(STATE_BUTTON_PIN, bounce_time=0.2)

        self.increase_button = Button(INCREASE_BUTTON_PIN, bounce_time=0.2)

        self.decrease_button = Button(DECREASE_BUTTON_PIN, bounce_time=0.2)

        # ----------------------------------------------------------
        # LCD
        # ----------------------------------------------------------
        self.lcd_rs = digitalio.DigitalInOut(getattr(board, f"D{LCD_RS_PIN}"))

        self.lcd_en = digitalio.DigitalInOut(getattr(board, f"D{LCD_EN_PIN}"))

        self.lcd_d4 = digitalio.DigitalInOut(getattr(board, f"D{LCD_D4_PIN}"))

        self.lcd_d5 = digitalio.DigitalInOut(getattr(board, f"D{LCD_D5_PIN}"))

        self.lcd_d6 = digitalio.DigitalInOut(getattr(board, f"D{LCD_D6_PIN}"))

        self.lcd_d7 = digitalio.DigitalInOut(getattr(board, f"D{LCD_D7_PIN}"))

        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs,
            self.lcd_en,
            self.lcd_d4,
            self.lcd_d5,
            self.lcd_d6,
            self.lcd_d7,
            LCD_COLUMNS,
            LCD_ROWS,
        )

        self.lcd.clear()

        # ----------------------------------------------------------
        # Serial connection
        # ----------------------------------------------------------
        self.serial_connection = serial.Serial(
            port=SERIAL_PORT,
            baudrate=SERIAL_BAUDRATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=SERIAL_TIMEOUT,
        )

    def read_environment(self):
        """
        Read the temperature and humidity from the AHT20.
        Returns:
        tuple: (temperature_f, humidity_percent)
        """

        temperature_c = self.sensor.temperature
        humidity = self.sensor.relative_humidity

        temperature_f = (temperature_c * 9 / 5) + 32

        return temperature_f, humidity

    def apply_lights(self, command):
        """
        Apply a LightCommand created by ThermostatController.
        """

        self.red_led.off()
        self.blue_led.off()

        if command.red == "pulse":
            self.red_led.pulse()

        elif command.red == "solid":
            self.red_led.on()

        if command.blue == "pulse":
            self.blue_led.pulse()

        elif command.blue == "solid":
            self.blue_led.on()

    def update_display(self, line1, line2):
        """
        Update the 16x2 LCD display.
        """

        line1 = str(line1)[:LCD_COLUMNS].ljust(LCD_COLUMNS)
        line2 = str(line2)[:LCD_COLUMNS].ljust(LCD_COLUMNS)

        self.lcd.clear()
        self.lcd.message = f"{line1}\n{line2}"

    def write_serial(self, message):
        """
        Send a message over the Raspberry Pi serial port.
        """

        self.serial_connection.write(message.encode("utf-8"))

    def register_button_callbacks(self, command_queue):
        """
        Button callbacks place commands into a queue.
        The buttons do not directly modify the thermostat state.
        """

        self.state_button.when_pressed = lambda: command_queue.put("cycle")

        self.increase_button.when_pressed = lambda: command_queue.put("increase")

        self.decrease_button.when_pressed = lambda: command_queue.put("decrease")

    def cleanup(self):
        """
        Safely shut down hardware resources.
        """

        self.red_led.off()
        self.blue_led.off()

        self.red_led.close()
        self.blue_led.close()

        self.state_button.close()
        self.increase_button.close()
        self.decrease_button.close()

        self.lcd.clear()

        self.lcd_rs.deinit()
        self.lcd_en.deinit()
        self.lcd_d4.deinit()
        self.lcd_d5.deinit()
        self.lcd_d6.deinit()
        self.lcd_d7.deinit()
        self.i2c.deinit()

        if self.serial_connection.is_open:
            self.serial_connection.close()
