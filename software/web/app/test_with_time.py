# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:05:45 2021
@author: Andrew Scott-George 
Program to test flask functionality.
"""

from flask import Flask, render_template #Load flask module
import datetime
import numpy as np

app = Flask(__name__) #instantiate Flask object

# Weather; generate random variables
temp = round(np.random.rand() * 30, 2)
pressure = round(1 - np.random.rand(),2)
humid = round(np.random.rand(),2)
wind_v = round(np.random.rand() * 20,2)
wind_d = round(np.random.rand(),2)
rain = round(np.random.rand() * 10,2)


@app.route('/') #what to do in the root directorys
def index(): #Index function; when someone accesses root directory ("/") of flask webapp it will perform this.
    now = datetime.datetime.now() #get current time
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'GUR Weather Station',
        'time' : timeString, 
        'temp' : temp,
        'pressure' : pressure,
        'humid' : humid,
        'wind_v' : wind_v,
        'wind_d' : wind_d,
        'rain' : rain
        }
    return render_template('index.html', **templateData)
if __name__  == '__main__':
        app.run(debug=True,port=80,host='0.0.0.0') #Start listening on port 80.
        