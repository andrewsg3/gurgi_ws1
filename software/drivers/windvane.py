"""Code for interfacing with wind vane via MCP3008 ADC"""

#https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/7
#https://www.argentdata.com/files/80422_datasheet.pdf

from gpiozero import MCP3008
import time
import math
import numpy as np

class windvane():
    """Windvane class
    """
    def __init__(self, r1=1450, vin=3.3):
        # Interfacing
        self.channel = 0 # Channel of ADC from which to read voltage 
        self.adc = MCP3008(channel = self.channel)
        self.r1 = r1 # The resistor used in the system
        self.vin = float(vin) #input voltage

        # Readings
        self.sampletime = 5

	self.resistances = [33000, 6570, 8200, 891, 1000, 688, 2200, 1410, 3900, 3140, 16000,
	14120, 120000, 42120, 64900, 21880]

	self.angles = [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 
	270, 292.5, 315, 337.5]

	self.voltages = np.zeros(len(self.angles))

	for i in range(len(self.resistances)):
		self.voltages[i] = round((self.vin * self.resistances[i]) / (self.r1 + self.resistances[i]), 1)

        self.volts = dict(zip(self.voltages, self.angles)) # Reference array for relating a read volage to an angle

        self.voltage = 0 # Last voltage read from ADC
        self.d = 0 # Last angle calculated from ADC voltage
        self.angles = [] # stored angles
    
    def read(self):
        """Read voltage from ADC and make correction / rounding
        """
        self.voltage = round(self.adc.value*3.3, 1)
        #self.lookup_angle()

    def lookup_angle(self):
        """Compare ADC input to lookup table and corresponding angle
        """
        if not self.voltage in self.volts:
            print("Unknown value of voltage from windvane. Check resistor configuration.\nMeasured voltage: " + str(self.voltage))
        else:
            print("Matched voltage: " + str(self.voltage) + "to table value: " + str(self.volts[self.voltage]))
            self.d = self.volts[self.voltage] # Update angle in deg

    def one_minute(self):
       	    """sample for one minute and print"""
	    start_time = time.time()
            record = []
	    print("Sampling windvane for 60 seconds")
	    while time.time() - start_time <= 20:
		    self.read()
		    record.append(self.voltage)	    
		    time.sleep(0.005)
	    print(record)
	    print(set(record))
	    print(len(set(record)))

    def sample(self):
        """Function to sample over some period and average
        """
        start_time = time.time()
        print("Sampling and averaging windvane for",self.sampletime,"seconds...")
        while time.time() - start_time <= self.sampletime:
            self.read()
            self.angles.append(self.d) # Append current value of d to angles list
        
        return self.get_average()

    def get_average(self):
        """Get the average of some angles in a period of time
        """
        sin_sum = 0.0
        cos_sum = 0.0

        for angle in self.angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(self.angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360
        
        return 0.0 if average == 360 else average

    def test_vals(self):
        """Report on last sampled values, stored as member variables
        """
        self.voltage = 2.0
        self.lookup_angle()
        
    def report(self):
        """Report on current value
        """
        return self.d



