"""Code for interfacing with wind vane via MCP3008 ADC"""

#https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/7
#https://www.argentdata.com/files/80422_datasheet.pdf

#from gpiozero import MCP3008
import time
import math

class windvane():
    """Windvane class
    """
    def __init__(self):
        # Interfacing
        self.channel = 0 # Channel of ADC from which to read voltage 
        #self.adc = MCP3008(channel = self.channel)
        self.r1 = 4700 # The resistor used in the system
        self.vin = 5 #input voltage
        

        # Readings
        self.sampletime = 5
        self.volts = { # Voltage lookup table: known values that should be taken when a 4.7k resistor forms voltage divider with anemometer.
            0.4: 0.0,
            1.4: 22.5,
            1.2: 45.0,
            2.8: 67.5,
            2.7: 90.0,
            2.9: 112.5,
            2.2: 135.0,
            2.5: 157.5,
            1.8: 180.0,
            2.0: 202.5,
            0.7: 225.0,
            0.8: 247.5,
            0.1: 270.0,
            0.3: 292.5,
            0.2: 315.0,
            0.6: 337.5
        }
        self.voltage = 0 # Last voltage read from ADC
        self.d = 0 # Last angle calculated from ADC voltage
        self.angles = [] # stored angles
    
    def read(self):
        """Read voltage from ADC and make correction / rounding
        """
        #self.voltage = round(self.adc.value*3.3, 1)
        self.lookup_angle()

    def lookup_angle(self):
        """Compare ADC input to lookup table and corresponding angle
        """
        if not self.voltage in self.volts:
            print("Unknown value of voltage from aneomemeter. Check resistor configuration." + str(self.voltage) + str(self.volts[self.voltage]))
        else:
            #print("Match " + str(self.voltage) + str(self.volts[self.voltage]))
            self.d = self.volts[self.voltage] # Update angle in deg

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



