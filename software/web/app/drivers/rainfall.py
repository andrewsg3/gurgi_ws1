"""Code for interacting with rain gauge
Should be connected via RJ11.
"""
#https://www.argentdata.com/files/80422_datasheet.pdf 
import time
from gpiozero import Button

class raingauge():
	"""Class for interacting with rain gauge"""
	def __init__(self):
        	#Interfacing
		self.gpiopin = 6 # Gpio pin
		self.tipsize = 0.2794 # Amount of rain that will tip bucket
		self.rain_sensor = Button(self.gpiopin)
		self.rain_sensor.when_pressed = self.tipped
		self.sampletime = 5

        	#Reading
		self.tipcount = 0
		self.rain = 0
		self.rain_hist = []

	def tipped(self):
		"""Tipcount updating callback for when gpiozero Button is pressed"""
		self.tipcount += 1

	def calculate_rain(self):
		"""Calculate amount of rain that has fallen"""
		self.rain = round(self.tipcount*self.tipsize,3)

	def one_minute(self):
		"""Takes measurements for one minute and stores them"""
		start_time = time.time()
		while time.time() - start_time <= 5:
			self.reset_rainfall()
			time.sleep(self.sampletime)
			self.calculate_rain()
			self.rain_hist.append(self.rain)

	def reset_rainfall(self):
		"""Reset the counts to 0"""
		self.tipcount = 0

	def report(self):
		"""Report on current value"""
		self.calculate_rain()
		return self.rain

	def test_vals(self):
		"""Add some test vals"""
		self.tipcount = 4
		self.calculate_rain()
