"""Contains functions for interfacing with a connected BME280 sensor
"""
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from time import sleep #allows for timing functions

class climate_sensor():
	"""Class containing BME280 functionality
	"""
	def __init__(self):
		self.port = 1
		self.address = 0x76 #hexadecimal address of BME280 device; depends on manufacturer, refer to documentation
		self.bus = SMBus(1) #instantiate an SMBus object for I2C interactions
		self.bme280 = BME280(i2c_dev = self.bus) #use a bme280 library function to apply the bus and address

		# Last values
		self.p = 0 # Last value of humidity
		self.h = 0 # Last value of pressure
		self.t = 0 # Last value of temperature

	def report(self):
		"""Report on last sampled values, stored as """
		self.read_all()
		return self.p, self.h, self.t

	def read_all(self):
		"""Takes a sample and updates 
		
		"""
		self.update(self.bme280.get_pressure(),self.bme280.get_humidity(),self.bme280.get_temperature()) #return each output from the sensor

	def update(self,p,h,t):
		"""Updates member variable values for humidity, pressure, temperature
		"""
		self.h = h
		self.p = p
		self.t = t

	def test_vals(self):
		"""Add some arbitrary test values to test other functions"""
		self.h = 0.76
		self.p = 1.0121
		self.t = 23.0
