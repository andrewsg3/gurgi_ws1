"""Contains functions for interfacing with a connected BME280 sensor
"""
import bme280 #import the BME280 library; installed via: sudo pip3 install RPi.bme280
#import smbus2 #system management bus library, used for I2C devices. Will not import unless on raspbian.
from time import sleep #allows for timing functions

class climate_sensor():
	"""Class containing BME280 functionality
	"""
	def __init__(self):
		self.port = 1
		self.address = 0x76 #hexadecimal address of BME280 device; depends on manufacturer, refer to documentation
		#self.bus = smbus2.SMBus(self.port) #instantiate an SMBus object for I2C interactions
		#bme280.load_calibration_params(self.bus, self.address) #use a bme280 library function to apply the bus and address

		# Last values
		self.p = 0 # Last value of humidity
		self.h = 0 # Last value of pressure
		self.t = 0 # Last value of temperature

	def report(self):
		"""Report on last sampled values, stored as """
		return self.p, self.h, self.t

	def read_all(self):
		"""Takes a sample and updates 
		
		"""
		bme280_data = bme280.sample(self.bus,self.address) #Sample the bme280 device and assign the output ot a variable
		self.update(bme280_data.pressure, bme280_data.humidity, bme280_data.temperature) #return each output from the sensor

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
