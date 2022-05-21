"""Code for bla bla windvane MCP3008 ADC"""
from gpiozero import MCP3008
import time
import math
import numpy as np

class windvane():
	def __init__(self, r1=1450, vin=3.3, decimals=3):
		#Interfacing
		self.channel = 0
		self.adc = MCP3008(channel = self.channel)
		self.r1 = r1
		self.vin = float(vin)

		#Readings
		self.decimals = decimals
		self.ref_voltage = self.vin # Multiply ADC reading by this.
		self.resistances = [33000, 6570, 8200, 891, 1000, 688, 2200, 1410, 3900, 3140, 16000, 14120, 120000, 42120, 64900, 21880]
		self.angles = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
		self.voltages = np.zeros(len(self.angles))

		for i in range(len(self.resistances)):
			self.voltages[i] = round((self.vin * self.resistances[i]) / (self.r1 + self.resistances[i]), self.decimals)

		self.key = {self.voltages[i]: self.angles[i] for i in range(len(self.voltages))} # Dict for matching voltages and angles

		self.voltage = None # Stores last voltage
		self.angle = None # Stores last angle

	def read(self):
		"""Read voltage from ADC and round"""
		self.voltage = round(self.adc.value * self.ref_voltage, self.decimals)
		self.check()

	def check(self, p=False):
		"""Checks voltage against angle"""
		if not self.voltage in self.voltages:
			if p == True:
				print(f"Value {self.voltage} not found in known voltages.")
			self.angle = None
		else:
			self.angle = self.key[self.voltage]
			if p == True:
				print(f"Voltage {self.voltage} matched angle {self.key[self.voltage]}")

	def loopread(self, t=5):
		"""Continuosly read and print voltage for input seconds"""
		t0 = time.time()
		while time.time() - t0 <= t:
			self.read()
			time.sleep(self.sampletime)
