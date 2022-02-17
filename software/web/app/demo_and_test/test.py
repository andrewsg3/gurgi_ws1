# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 13:05:45 2021
@author: Andrew Scott-George 
Program to test flask functionality.
"""

from flask import Flask #Load flask module

app = Flask(__name__) #instantiate Flask object

@app.route('/') #what to do in the root directorys
def index(): #Index function; when someone accesses root directory ("/") of flask webapp it will perform this.
    return "Hello World"
if __name__  == '__main__':
        app.run(debug=True,port=80,host='0.0.0.0') #Start listening on port 80.
        