"""Contains class for windspeed anemometer
"""
from gpiozero import Button #Won't work unless on raspbi
import math
import statistics
import time

class anemo():
    """Class containing windspeed anemometer functionality
    """
    def __init__(self):
    # Electornic interface values
        self.sampletime = 5 # sample time in s  
        self.gpio_pin = 5
        self.windsensor = Button(self.gpio_pin) #Windsensor is a Button class from gpiozero library
        self.windsensor.when_pressed = self.spin # When the button is pressed, call the spin function to update wind count

        # Anemometer values
        self.radius = 0.09 # radius in m
        self.c = (2*math.pi)*(self.radius) # circumference in m
        self.adjustment = 1.18 # correction factor

        # Last values
        self.wind_count = 0 #number of counts 
       	self.v = 0 #wind speed
        self.spins = [0]
        self.stored_times = [time.time()]
        self.stored_speeds = [None]

    def spin(self):
        """Callback (?) for when "button" is pressed
        """
        self.wind_count = self.wind_count + 1
        self.stored_times.append(time.time())
        self.spins.append(self.wind_count)
        speed = self.calculate_speed2()
        self.stored_speeds.append(speed)

    def calculate_speed2(self):
        """Calculate windspeed based on saevd times, spins etc"""
        i = len(self.spins)
        latest_spins = self.spins[i-1] - self.spins[i-2]
        latest_time = self.stored_times[i-1] - self.stored_times[i-2]
        speed = self.calculate_speed(latest_spins, latest_time)
        return speed

    def calculate_speed(self, wind_count, sampletime):
        """Calculate windspeed based on anem geometry and number of ticks in sample period
        Should get called at end of sample period
        """
        rotations = wind_count / 2 # True rotations is half the counted pulses from button
        dist = self.c * rotations
        speed = dist / sampletime
        speed = round(speed * self.adjustment,2) # Perform correction on speed
        self.v = speed # Update speed
        self.reset_wind

    def reset_wind(self):
        """Reset the number of ticks"""
        self.wind_count = 0

    def one_minute(self):
        """Takes measurements for one minute and stores them"""
        start_time = time.time()
        while time.time() - start_time <= 5:
            self.reset_wind()
            time.sleep(self.sampletime)
            self.calculate_speed()
            self.stored_speeds.append(self.v)

        wind_gust = max(self.stored_speeds)
        wind_speed = statistics.mean(self.stored_speeds)
        print(f"Latest speed: {round(wind_speed,2)}m/s \nMax speed: {round(wind_gust,2)}m/s")

    def report(self):
        """Report on last sampled values, stored as member variables"""
        return self.v

    def test_vals(self):
        """Add some arbitrary test values to test other functions"""
        self.v = 4.81

   
