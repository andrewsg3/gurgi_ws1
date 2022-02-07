import climate

my_sensor1 = climate.climate_sensor()

print(my_sensor1.port)

my_sensor1.read_all() 

my_sensor1.report()


import rainfall

my_sensor2 = rainfall.raingauge()

my_sensor2.report()