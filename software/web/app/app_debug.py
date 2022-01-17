# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:05:45 2021
@author: Andrew Scott-George 
Program to test flask functionality.
"""

from flask import Flask, render_template #Load flask module
from flask_socketio import SocketIO, emit
from flask_mongoengine import MongoEngine
import datetime
import numpy as np
import sys
import threading
import time
#sys.path.append('../../')
#import drivers.driver

#Create flask mongo engine
db = MongoEngine()

#Webapp
app = Flask(__name__) #instantiate Flask object
app.config.from_object('config') #Address for app config file, config.py

#Initialise DB
db.init_app(app)


## Blueprints allow for different sections of webapp to be defined in different files and imported.
#Import blueprints
#from app.NAME.views import NAME_bp

#Register blueprints
#app.register_blueprint(NAME_bp)



# Weather; generate random variables
temp = round(np.random.rand() * 30, 2)
pressure = round(1 + 0.1*np.random.rand(),2)
humid = round(np.random.rand(),2) * 100
wind_v = round(np.random.rand() * 20,2)
wind_d = round(np.random.rand(),2)
rain = round(np.random.rand() * 10,2)
coords = '''55°52'15.9"N 4°17'11.8"W'''

@app.route('/') #what to do in the root directorys, main route that loads htmlpage
def index(): #Index function; when someone accesses root directory ("/") of flask webapp it will perform this.
    now = datetime.datetime.now() #get current time
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'GUR Weather Station',
        'time' : timeString, 
        'temp' : round(np.random.rand() * 30,2),
        'pressure' : pressure,
        'humid' : humid,
        'wind_v' : wind_v,
        'wind_d' : wind_d,
        'rain' : rain,
        'coords' : coords
        }
    return render_template('index.html', **templateData)

#Initialize?
socketio = SocketIO(app)

#if __name__  == '__main__':
    #x = threading.Thread(target = checker_thread, daemon=True)
    #x.start()
#    app.run(debug=True,port=80,host='0.0.0.0') #Start listening on port 80.
        