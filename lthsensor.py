import time
import board
import busio
import adafruit_si7021
import RPi.GPIO as GPIO


#Script for Temperature/Humidity sensing
#Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_si7021.SI7021(busio.I2C(board.SCL, board.SDA))
reading = 0
#GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the light sensor circuit
pin_to_circuit = 4 
def rc_time(pin_to_circuit):
	count = 0
	#Output on the pin for 
	GPIO.setup(pin_to_circuit, GPIO.OUT)
	GPIO.output(pin_to_circuit, GPIO.LOW)
	time.sleep(0.1)

	#Change the pin back to input
	GPIO.setup(pin_to_circuit, GPIO.IN)
 
	#Count until the pin goes high
	while (GPIO.input(pin_to_circuit) == GPIO.LOW):
		count += 1

	return count


print("Reading Temperature(°C) Humidity(%) Light(rc_time)")
try:
	while True: 
		reading_str = str(reading)
		print("%d %f %f %d" % (reading, sensor.temperature, sensor.relative_humidity, rc_time(pin_to_circuit)))
		time.sleep(1)
		reading += 1 

		#Script for Light sensing


#Catch when script is interupted, cleanup correctly
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
