#Contains functions for interfacing with a connected BME280 sensor
import bme280 #import the BME280 library; installed via: sudo pip3 install RPi.bme280
import smbus2 #system management bus library, used for I2C devices
from time import sleep #allows for timing functions

port = 1
address = 0x76 #hexadecimal address of BME280 device; depends on manufacturer, refer to documentation
bus = smbus2.SMBus(port) #instantiate an SMBus object for I2C interactions

bme280_load_calibration_params(bus, address) #use a bme280 library function to apply the bus and address

def read_all():
	bme280_data = bme.sample(bus,address) #Sample the bme280 device and assign the output ot a variable
	return bme280_data.humidity, bme280_data.pressure, bme280_data.temperature #return each output from the sensor
