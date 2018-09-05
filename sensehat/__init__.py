"""
This module provides a class for interfacing with the Sense HAT add-on board for Raspberry Pi.
"""
import os
from multiprocessing.managers import RemoteError

from myDevices.utils.logger import error, exception, info
from sensehat.manager import connect_client


class SenseHAT():
    """Class for interacting with a Sense HAT device"""

    def __init__(self, use_emulator=False):
        """Initializes Sense HAT device.

        Arguments:
        use_emulator: True if the Sense HAT Emulator should be used. This requires the Emulator to be installed and running on the desktop.
        """
        self.use_emulator = use_emulator
        self.sense_hat = None
        self.digital_value = 0
        self.analog_value = 0.0
        self.image_file = os.path.join('/etc/myDevices/plugins/cayenne-plugin-sensehat/data/image.png')
        self.call_sense_hat_function('clear')

    def init_sense_hat(self):
        """Initializes connection to Sense HAT service and gets a SenseHat shared object."""
        if not self.sense_hat:
            try:
                self.manager = connect_client()
                self.manager.use_emulator(self.use_emulator)
                self.sense_hat = self.manager.SenseHat()
            except ConnectionRefusedError as e:
                info('Connection refused')
                error(e)
            except RemoteError as e:
                error('Failed to connect to Sense HAT device')

    def call_sense_hat_function(self, function_name, *args):
        """Calls a function of the SenseHat shared object.
        
        Arguments:
        function_name: Name of the function to call.
        args: Arguments to pass to the function.
        """
        self.init_sense_hat()
        try:
            if self.sense_hat is not None:
                func = getattr(self.sense_hat, function_name)
                value = func(*args)
                return value
        except EOFError as e:
            error(e)
            sense_hat = None
        except AttributeError as e:
            error(e)
            sense_hat = None

    def get_temperature(self):
        """Gets the temperature as a tuple with type and unit."""
        return (self.call_sense_hat_function('get_temperature'), 'temp', 'c')

    def get_humidity(self):
        """Gets the humidity as a tuple with type and unit."""
        value = self.call_sense_hat_function('get_humidity')
        if value is not None:
            return (value / 100, 'rel_hum', 'p')

    def get_pressure(self):
        """Gets the pressure as a tuple with type and unit."""
        value = self.call_sense_hat_function('get_pressure')
        if value is not None:
            return (value * 100, 'bp', 'pa')

    def get_acclerometer(self):
        """Gets the g-force as a tuple with type and unit."""
        values = self.call_sense_hat_function('get_accelerometer_raw')
        if values is not None:
            g_force = []
            g_force.append(values['x'])
            g_force.append(values['y'])
            g_force.append(values['z'])
            return (g_force, 'accel', 'g')

    def get_gyroscope(self):
        """Gets radians per second from the gyroscope."""
        #Not currently supported in Cayenne
        values = self.call_sense_hat_function('get_gyroscope_raw')
        if values is not None:
            rps = []
            rps.append(values['x'])
            rps.append(values['y'])
            rps.append(values['z'])
            return rps

    def get_magnetometer(self):
        """Gets microteslas from the magnetometer."""
        #Not currently supported in Cayenne
        values = self.call_sense_hat_function('get_compass_raw')
        if values is not None:
            gyro = []
            gyro.append(values['x'])
            gyro.append(values['y'])
            gyro.append(values['z'])
            return gyro

    def get_digital(self):
        """Gets the digital value as a tuple specifying this is a digital actuator."""
        return (self.digital_value, 'digital_actuator')

    def set_digital(self, value):
        """Displays an image on the Sense HAT LED matrix if the digital value is equal to True."""
        self.digital_value = value
        if self.digital_value:
            self.call_sense_hat_function('load_image', self.image_file)
        else:
            self.call_sense_hat_function('clear')

    def get_analog(self):
        """Gets the digital value as a tuple specifying this is an analog actuator."""
        return (self.analog_value, 'analog_actuator')

    def set_analog(self, value):
        """Displays the analog value on the Sense HAT LED matrix."""
        self.analog_value = value
        self.call_sense_hat_function('show_message', str(self.value))
