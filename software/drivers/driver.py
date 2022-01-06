import climate
import windspeed
import winddirection
import rainfall

## Instantiate classes
s_bme280 = climate.climate_sensor()
anem = windspeed.windspeed_sensor()
vane = winddirection.windvane()
raingauge = rainfall.raingauge()

## Test BME280
#s_bme280.read_all()
s_bme280.test_vals()
print("Pressure =",s_bme280.report()[0],"Bar")
print("Humidity =",s_bme280.report()[1]*100,"%")
print("Temperature =",s_bme280.report()[2],"°C")

## Test anemometer
anem.test_vals()
print("Windspeed =",anem.report(),"m/s")

## Test windvane
vane.test_vals()
print("Wind direction =",vane.report(),"°")
#vane.sample()

## Test rain gauge
raingauge.test_vals()
print("Rainfall =",raingauge.report(),"mm")
