# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:05:45 2021
@author: Andrew Scott-George 
Main program from which webapp is run.
"""

## Import libraries
from turtle import title
from flask import Flask, render_template, Response #Load flask module
import datetime
import numpy as np
import sys
import threading
import random
import json
from time import time, sleep
from flask import make_response
try:
    import climate
except:
    print("Climate could not be imported.")
try:
    import rainfall
except:
    print("Rainfall could not be imported.")
try:
    import windspeed
except:
    print("Windspeed couldn not be imported.")

import camera

## Set params
sampletime = 0.1 # 2 seconds sample rate for sensors

## Initialize things
app = Flask(__name__) # Instantiate Flask app object
#app.config.from_object('app.config') #Address for app config file, config.py
#from app.NAME.views import NAME_bp # Blueprints allow for different sections of webapp to be defined in different files and imported.
#app.register_blueprint(NAME_bp) # Register blueprints

#db = MongoEngine() # Instantiate mongo DB

#db.init_app(app) # Bind mongo DB to flask app


## Set initial variables
title = 'GUR Weather Station'
temp = "Initializing..."
pressure = "Initializing..."
humid = "Initializing..."
wind_v = "Initializing..."
wind_d = "Initializing..."
rain = "Initializing..."
coords = "Initializing..."
updates = 0

"""
Route: '/'
This root is what to do on the homepage.
Basically, just render the main HTML.
"""
@app.route('/') #what to do in the root directorys, main route that loads htmlpage
def index(): #Index function; when someone accesses root directory ("/") of flask webapp it will perform this.
    # By redefining variables here, we can update what the page shows.
    now = datetime.datetime.now() #get current time
    timeString = now.strftime("%Y-%m-%d %H:%M")

    # Could we add the ability to poll the weather station thread here? 
    templateData = {
        'title' : title,
        'time' : timeString, 
        'temp' : temp,
        'pressure' : pressure,
        'humid' : humid,
        'wind_v' : wind_v,
        'wind_d' : wind_d,
        'rain' : rain,
        'coords' : coords
        }
    return render_template('index.html', **templateData)


"""
Route: '/update'
This route is used to update the variables as seen by the client. It is called by javascript in index.html.
"""
@app.route('/update', methods=["GET","POST"])
def update():
    print("Updated data")
    global updates, temp, pressure, humid, wind_v, wind_d, rain, coords
    updates += 1
    documents_ = {
        'updates': updates,
        'temperature': temp,
        'pressure': pressure,
        'humidity': humid,
        'windspeed': wind_v,
        'windvector': wind_d,
        'rainfall': rain,
        'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'coords:': coords
    }
    return Response(json.dumps(documents_), mimetype='application/json')


"""
The following thread is intended to sample the I2C sensors at a set interval. 
The sampling should update the local values of the variables which can be accessed when a client requests them.
"""
try:    
    bme = climate.climate_sensor()
except:
    print("BME280 could not be instantiated.")

try:
    raingauge = rainfall.raingauge()
except:
    print("Rain gauge could not be instantiated.")

try:
    anemo = windspeed.anemo()
except:
    print("Anemometer couldn not be instantiated.")

def check_sensors(sampletime):
    while True:
        print("Check sensors called")
        global temp, pressure, humid, wind_v, wind_d, rain, coords, time # Make reference to global variables
        bme.read_all() # Read weather values
       	climate_vals = bme.report()
        pressure = round(climate_vals[0]/1000,3)
        humid = round(climate_vals[1],3)
        temp = round(climate_vals[2],3)
        wind_v = anemo.report()
        wind_d = "Coming soon..."
        rain = raingauge.report()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        coords = coords
        print(climate_vals)
        sleep(sampletime)
"""
This route allows for camera streaming
"""
@app.route('/video_feed')
def video_feed():
    print("Video feed called")
    return Response(camera.gen_frames(),mimetype='multipart/x-mixed-replace;boundary=frame')

sensor_thread = threading.Thread(target = check_sensors, args = [sampletime]) # Bind check_sensors function to a new thread called sensor_thread
sensor_thread.start() # Begin sensor checking threads

if __name__  == '__main__':
    app.run(debug=False,port=80,host='0.0.0.0') #Start listening on port 80.

camera.cap.release()
cv2.destroyAllWindows()
