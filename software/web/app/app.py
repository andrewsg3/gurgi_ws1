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
from matplotlib.pyplot import table
import numpy as np
import sys
import threading
import random
import json
import time
import psycopg2
from flask import make_response

print("### INITIALIZING SENSOR DRIVERS ###")
try:
    import drivers.climate as climate
except:
    print("BME280 driver could not be imported.")
try:
    import drivers.rainfall as rainfall
except:
    print("Rainfall driver could not be imported.")
try:
    import drivers.windspeed as windspeed
except:
    print("Windspeed driver could not be imported.")
try:
    import drivers.windv as windv
except:
    print("Wind direction driver could not be imported.")
try:
    import drivers.camera as camera
except:
    print("Camera driver could not be imported.")

#print("\n\n")

## Set params
sampletime = 0.1 # 2 seconds sample rate for sensors

## Initialize things
app = Flask(__name__) # Instantiate Flask app object
print("Flask app initialized.")
#app.config.from_object('app.config') #Address for app config file, config.py
#from app.NAME.views import NAME_bp # Blueprints allow for different sections of webapp to be defined in different files and imported.
#app.register_blueprint(NAME_bp) # Register blueprints
print("\n\n")

## Connect to psql database
print("### DATABASE INITIALIZING ###")
dbname = "gurgibase" # The name of an existing database
username = "postgres"
mypass = "pass"
init_date = datetime.datetime.now().strftime(f"%Y_%m_%d_%Hh%Mm%Ss")
tablename = f"Session_{init_date}"
print("Connecting to SQL database...")
try:
    conn = psycopg2.connect( # Connect to database
        host="localhost",
        database=dbname,
        user=username,
        password=mypass,
    )
    print("Connected!")
except:
    print(f"ERROR! Could not connect to database '{dbname}'. Speak to a system admin. Exiting program...")
    raise SystemExit(0)

cur=conn.cursor() # Create a cursor
print("Testing an execute statement...")
cur.execute("SELECT version()")
print("Success. Cursor object is working correctly.")
print(f'PostgreSQL database version: {cur.fetchone()} ') 

cols = ["epoch", "date", "time", "pressure", "humidity", "temperature", "wind_speed", "rain", "wind_direction"]
datatype = ["FLOAT", "VARCHAR(30)", "VARCHAR(30)", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT"]

def create_table(tablename,cols, datatype):
    global conn, cur
    statement = f"CREATE TABLE {tablename}("
    i = 0
    while i < len(cols):
        statement += f"{cols[i]} {datatype[i]}"
        if i < len(cols)-1:
            statement +=", "
        i+=1
    statement += ");"
    print(statement)
    cur.execute(statement)
    conn.commit()

create_table(tablename, cols, datatype)
print(f"Table {tablename} created.")

def insert(tablename, cur, conn, res):
    statement = f"INSERT INTO {tablename}(epoch, date, time, pressure, humidity, temperature, wind_speed, rain, wind_direction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);" # 
    statement = cur.mogrify(statement, res)
    cur.execute(statement)
    conn.commit()

print("\n\n")

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
session_duration = 0

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
        'coords' : coords,
	'session_duration' : session_duration
        }
    return render_template('index.html', **templateData)


"""
Route: '/update'
This route is used to update the variables as seen by the client. It is called by javascript in index.html.
"""
@app.route('/update', methods=["GET","POST"])
def update():
    print("Updated data")
    global updates, temp, pressure, humid, wind_v, wind_d, rain, coords, session_duration
    updates += 1
    documents_ = {
        'updates': updates,
	'session_duration' : session_duration,
        'temperature': temp,
        'pressure': pressure,
        'humidity': humid,
        'windspeed': wind_v,
        'windvector': wind_d,
        'rainfall': rain,
        'timenow': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'time_elapsed': (time() - start_time),
        'coords': coords
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
    print("Raingauge could not be instantiated.")

try:
    anemo = windspeed.anemo()
except:
    print("Anemometer could not be instantiated.")

try:
    windvane = windv.windvane(r1=4940, decimals=1)
except:
    print("Windvane could not be instantiated.")

def check_sensors(sampletime):
    while True:
        global temp, pressure, humid, wind_v, wind_d, rain, coords, timenow, session_duration, cur, conn, tablename # Make reference to global variables
        climate_vals = bme.report() # Read BME values
        pressure = round(climate_vals[0]/1000,3)
        humid = round(climate_vals[1],3)
        temp = round(climate_vals[2],3)
        wind_v = anemo.report()
        wind_d = windvane.report()
        rain = raingauge.report()
        t_datetime = datetime.datetime()
        t = t_datetime.timestamp()
        session_duration = str(datetime.timedelta(seconds=int(t - session_start)))
        timenow = time.strftime("%Y-%m-%d %H:%M", time.gmtime(t)),
        coords = coords

        ## Insert into database
        #true_time, date, time, pressure, humidity, temperature, wind_speed, rain_tips, wind_direction
        res = [t, t_datetime.strftime("%Y-%m-%d"), t_datetime.strftime("%H:%M:%S"), pressure, humid, temp, wind_v, rain, wind_d]
        insert(tablename, cur, conn, res)
        time.sleep(sampletime)

"""
This route allows for camera streaming
"""
@app.route('/video_feed')
def video_feed():
    print("Video feed called")
    return Response(camera.gen_frames(),mimetype='multipart/x-mixed-replace;boundary=frame')

sensor_thread = threading.Thread(target = check_sensors, args = [sampletime]) # Bind check_sensors function to a new thread called sensor_thread
sensor_thread.start() # Begin sensor checking threads

session_start = time.time()
if __name__  == '__main__':
    app.run(debug=False,port=80,host='0.0.0.0') #Start listening on port 80.

camera.cap.release()
cv2.destroyAllWindows()
