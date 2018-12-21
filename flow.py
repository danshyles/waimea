#Python script to measure flow rate with Water Flow Sensor Model: FS300A G3/4"
#Modified from tsbrownie, https://youtu.be/8JXd-2_zJQ0
#Nested WHILE version using RPi clock
#Input on pin 13, pin 6 gnd, 5Vcc pin to Rpi pin 2
#IMPORTANT: Input MUST go thru voltage divider circuit as it is running >3.3V
#Input -> 4.7k resistor -> RPi pin 13 + 10k -> Gnd RPi
#Warning: No stopped flow warning. Only approximate.*****

import RPi.GPIO as GPIO         #Import GPIO Library
import time, sys                #Import time (using internal clock), sys library
GPIO.setmode(GPIO.BOARD)        #GPIO pin numbering board
inpt = 13                       #Set input pin
GPIO.setup(inpt,GPIO.IN)        #Set input as inpt pin
rate_min_cnt = 0                #Hall Pulses counted in one minute (pulses/min)
rate_sec_cnt = 0                #Hall Pulses counted in one second (pulses/sec)
tot_cnt = 0                     #Total counts
minutes = 0                     #Total minutes
seconds = 0                     #Total seconds
constant = 0.00000278           #(l/pulse) Convert pulses to liters, measure by counting pulses to fill a 5 gal bucket
time_min = 0.0                  #Keep next minute
time_sec = 0.0                  #Keep next second

print('Water Flow - Approximate')
print('Control C to exit')

while True:                         #Loop forever
    time_min = time.time() + 60     #+60 = 1 minute
    rate_min_cnt = 0                    #Reset flow rate counter
    while time.time() <= time_min:  #keep looping until the next minute has elapsed
        rate_sec_cnt = 0            #reset second pulse counter after a second has elapsed
        time_sec = time.time() + 1      #+1 second for tracking rate per sec
        while time.time() <= time_sec: #internal loop to count pulses per second. 
            if GPIO.input(inpt)!= 0:    #if signal from the input is not zero, meaning we get a pulse
                rate_sec_cnt += 1       #add a pulse
                rate_min_cnt += 1
                tot_cnt += 1            #Total Pulses
            try:
                yo=0
                #print(GPIO.input(inpt), end='') #Status indicator
            except KeyboardInterrupt:   #Look for exit command
                print('\nCTRL C - Exiting nicely')
                GPIO.cleanup()          #Clean up GPIO
                sys.exit()              #Exit nicely
        seconds +=1                    #Increment total seconds       
        print('\nTotal Pulses: ', round(tot_cnt, 1)) #Include this to print how many pulses have occurred in total. 
        print('\nSeconds: ', seconds)
        print('\nTime Sec:: ', time_sec)
        print('\nLiters / sec ', round(rate_sec_cnt * constant, 4))
    minutes += 1                        #Increment total minutes
    print('\nLiters / min ', round(rate_min_cnt * constant, 4))
    print('Total Liters ', round(tot_cnt * constant,4))
    print('Time (min & clock) ', 'Sec: ', seconds, 'Min: ', minutes, '\t', 'Current Time: ', time.asctime(time.localtime()))

GPIO.cleanup() 			    #Reset ports
print('Done') 			    #Print 'Done'
            


