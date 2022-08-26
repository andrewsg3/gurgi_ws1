# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:05:45 2021
@author: Andrew Scott-George 
Main program from which webapp is run.
"""

## Import libraries
from distutils.log import error
from turtle import title # 
from flask import Flask, render_template, Response # Flask module. Webapp engine.
import datetime 
import numpy as np
import sys
import threading
import random
import json
import time
import psycopg2
from flask import make_response
import platform # Used to check OS, see whether being run on Pi
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

mysys = platform.system()
if mysys != "Linux":
    print("Not running on Raspberry Pi.\n")

print("### INITIALIZING SENSOR DRIVERS ###")
cam=config['SENSORS']['CAM']
cli=config['SENSORS']['CLI']
rai=config['SENSORS']['RAI']
wis=config['SENSORS']['WIS']
wid=config['SENSORS']['WID']

try:
    import drivers.climate as climate
except:
    print("BME280 driver could not be imported.")
    cli=False
try:
    import drivers.rainfall as rainfall
except:
    print("Rainfall driver could not be imported.")
    rai=False
try:
    import drivers.windspeed as windspeed
except:
    print("Windspeed driver could not be imported.")
    wis=False
try:
    import drivers.windv as windv
except:
    print("Wind direction driver could not be imported.")
    wid=False
try:
    import drivers.camera as camera
except:
    print("Camera driver could not be imported.")
    cam=False

## Set params
sampletime = float(config['SENSORS']['SAMPLETIME']) # 2 seconds sample rate for sensors
rolling_average = 0.5 # Rolling average in minutes

## Initialize things
app = Flask(__name__) # Instantiate Flask app object
print("Flask app initialized.")
#app.config.from_object('app.config') #Address for app config file, config.py
#from app.NAME.views import NAME_bp # Blueprints allow for different sections of webapp to be defined in different files and imported.
#app.register_blueprint(NAME_bp) # Register blueprints
print("\n\n")

## Connect to psql database
print("### DATABASE INITIALIZING ###")
dbname = config['DATABASE']['DBNAME'] # The name of an existing database
username = config['DATABASE']['USERNAME']
mypass = config['DATABASE']['PASSWORD']
tablename = config['DATABASE']['TABLENAME']
print(f"dbname: {dbname}, username: {username}, pass: {mypass}, tablename: {tablename}")
init_date = datetime.datetime.now().strftime(f"%Y_%m_%d_%Hh%Mm%Ss")
#tablename = f"Session_{init_date}"
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
user_cur = conn.cursor()
print("Testing an execute statement...")
cur.execute("SELECT version()")
print("Success. Cursor object is working correctly.")
print(f'PostgreSQL database version: {cur.fetchone()} ') 

cols = ["session", "epoch", "date", "time", "pressure", "humidity", "temperature", "wind_speed", "rain", "wind_direction"]
datatype = ["SMALLINT", "FLOAT", "VARCHAR(30)", "VARCHAR(30)", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT"]

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

#create_table(tablename, cols, datatype)
#print(f"Table {tablename} created.")

## Get new session ID
cur.execute("SELECT MAX(session) as latest_session FROM DATA;")
conn.commit()
session = cur.fetchone()[0];
if session == None:
    session = 1
else:
    session = session + 1
print(f"Database Session ID: {session}")

def insert(tablename, cur, conn, res):
    statement = f"INSERT INTO {tablename}(session, epoch, date, time, pressure, humidity, temperature, wind_speed, rain, wind_direction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" # 
    statement = cur.mogrify(statement, res)
    cur.execute(statement)
    conn.commit()

def query(tablename, user_cur, conn, cols, n):
    s1 = f"AVG({cols[0]}), AVG({cols[1]}), AVG({cols[2]}), AVG({cols[3]}), AVG({cols[4]}), AVG({cols[5]})"
    s2 = f"{cols[0]}, {cols[1]}, {cols[2]}, {cols[3]}, {cols[4]}, {cols[5]}"
    statement = f"SELECT {s1} FROM (SELECT {s2} FROM {tablename} ORDER BY epoch DESC LIMIT {n}) AS a"
    user_cur.execute(statement)
    conn.commit()
    res = []
    for i in user_cur.fetchone():
        if i != None:
            res.append(round(i,2))
        else:
            res.append(i)
    return res

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
    print("\nUpdated data")
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
        'time_elapsed': (time.time() - session_start),
        'coords': coords
    }
    return Response(json.dumps(documents_), mimetype='application/json')


@app.route('/update_sql', methods=["GET", "POST"])
def update_sql():
    print("\nClient requested update: querying SQL table.")
    global user_cur, conn, tablename, rolling_average, sampletime
    cols = ["pressure", "temperature", "humidity", "wind_speed", "rain", "wind_direction"]
    n = (rolling_average * 60) / sampletime
    res = query(tablename, user_cur, conn, cols, n)
    if res == None:
        res = [None, None, None, None, None, None]
    #print(res)
    global updates, coords, session_duration
    updates += 1
    documents_ = {
        'updates': updates,
        'session_duration': session_duration,
        'temperature': res[1],
        'pressure': res[0],
        'humidity': res[2],
        'windspeed': res[3],
        'windvector': res[5],
        'rainfall': res[4],
        'timenow': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'time_elapsed': (time.time() - session_start),
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
        print("Sensors updated.")
        global temp, pressure, humid, wind_v, wind_d, rain, coords, timenow, session_duration, cur, conn, tablename # Make reference to global variables
        if cli==True:
            climate_vals = bme.report() # Read BME values
            pressure = round(climate_vals[0]/1000,3)
            humid = round(climate_vals[1],3)
            temp = round(climate_vals[2],3)
        else:
            pressure = None
            humid = None
            temp = None
        if wis==True:
            wind_v = anemo.report()
        else:
            wind_v = None
        if wid==True:
            wind_d = windvane.report()
        else:
            wind_d = None
        if rai==True:
            rain = raingauge.report()
        else:
            rain = None
        t_datetime = datetime.datetime.now()
        t = t_datetime.timestamp()

        session_duration = str(datetime.timedelta(seconds=int(t - session_start)))
        timenow = time.strftime("%Y-%m-%d %H:%M", time.gmtime(t)),
        coords = coords

        ## Insert into database
        # Columns: true_time, date, time, pressure, humidity, temperature, wind_speed, rain_tips, wind_direction
        res = [session, t, t_datetime.strftime("%Y-%m-%d"), t_datetime.strftime("%H:%M:%S"), pressure, humid, temp, wind_v, rain, wind_d]
        insert(tablename, cur, conn, res)
        #print("Insertion made to SQL database.")
        time.sleep(sampletime)

"""
This route allows for camera streaming
"""
@app.route('/video_feed')
def video_feed():
    print("Video feed called")
    if cam==True:
        return Response(camera.gen_frames(),mimetype='multipart/x-mixed-replace;boundary=frame')
    else:
        return Response("Nothing.")

sensor_thread = threading.Thread(target = check_sensors, args = [sampletime]) # Bind check_sensors function to a new thread called sensor_thread
sensor_thread.start() # Begin sensor checking threads

session_start = time.time()
if __name__  == '__main__':
    print("### BEGINNING FLASK SERVER ###")
    app.run(debug=False,port=80,host='0.0.0.0') #Start listening on port 80.

if cam==True:
    camera.cap.release()
    cv2.destroyAllWindows()
