import busio
import digitalio
import board
import time
import math
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
 
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
  
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
   
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
    
# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

#Steinhart-Hart Equation method of determining temperature
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    steinhart = math.log(r/Ro)/beta
    steinhart += 1.0/(To+273.15)
    steinhart = (1.0/steinhart)-273.15
    return steinhart

while True:
    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')
    resistance = 10000/((65535/chan.value)-1)
    print('resistance: ' + str(resistance) + 'Ohms')
    print('Temp: ' + str(math.log((resistance/(30.6881*1000)), 0.956118)) + 'C')
    print('Steinhart Temp: ' + str(steinhart_temperature_C(resistance)) + 'C')
    time.sleep(0.5)
