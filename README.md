# GUR | Ground Infrastructure | Weather Station Mk.1 <img src ="https://user-images.githubusercontent.com/77739968/148395312-861d6199-237d-4511-8b94-009211b821c4.png" width = "30" height = "30">

This repo contains all code necessary to run the GURGI Weather Station Mk. 1.
<br>
The weather station is designed to measure a variety of environmental variables and present them via a LAN webapp. 
<br>
To access the webapp, users connect to a wireless access point (WAP) via mobile or laptop, navigate to a browser, and type https://localhost.
<br>
The sensing portion of the weather station is largely based on the project available at https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/0.

<h2>Usage</h2>
<ol>
  <li>Install github on your computer: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git </li>
  <li>Clone the repo: open the command line (press windows key and type "cmd"), then navigate to the folder you want to keep the code in. You can do this using "cd" to change directory and "mkdir" to make a new folder. Once you're there, type "git clone https://github.com/andrewsg3/gurgi_ws1"</li>
  <li>Install Anaconda: https://www.anaconda.com/ </li>
  <li>Open Anaconda, and create an environment. This way we can install packages - bits of addon code - to a version of Anaconda/Python just for this project, without installing them ontop of our base version of Anaconda/Python. To do this, open Anaconda prompt and type: "conda create gurgi"</li>
  <li>Activate the environment you created. In Anaconda prompt, type "conda activate gurgi". You'll do this everytime you open Anaconda prompt and want to use the code.</li>
  <li>In Anaconda prompt navigate to the github repo you clonded. Type "pip3 install requirements.txt". This will install the required packages, which are kept in the requirements.txt file.</li>
  <li>Once that's finished, you have everything you need to run the weather station. To trial the webapp, navigate to "gurgi_ws1/software/web/app" and type "python app.py". Now open your browser and type "https://localhost".</li>
</ol>
    

<h2>Prerequisites:</h2>
<h3>Hardware</h3>
<ul>
  <li>Raspberry Pi <br>https://thepihut.com/products/raspberry-pi-4-model-b?gclid=Cj0KCQiAw9qOBhC-ARIsAG-rdn5R2-kfO6yMEr01fbIaPO6ap6t9Ut63xb4w5BCDGALVWb19lnMGfioaAr5iEALw_wcB</li>
  <li>BME280 Sensor <br>https://shop.pimoroni.com/products/bme280-breakout</li>
  <li>MCP3008 ADC <br>https://shop.pimoroni.com/products/microchip-analog-to-digital-convertor?variant=373567065</li>
  <li>Argent Data Systems Weather Sensor Assembly p/n 80422 <br>https://shop.pimoroni.com/products/wind-and-rain-sensors-for-weather-station-wind-vane-anemometer-rain-gauge</li>   
  <li>2 x RJ11 Breakout Boards <br>https://shop.pimoroni.com/products/rj11-6-pin-connector</li>
</ul>
