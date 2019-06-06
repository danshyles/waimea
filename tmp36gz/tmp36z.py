#!/usr/bin/python
# -*- coding: utf-8 -*-
# mcp3008_lm35.py - read an LM35 on CH0 of an MCP3008 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer([1, 8 + adcnum << 4, 0])
    print (r)
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

while True:
    value = readadc(0)
    print ("output from adc: %4.3f" % (value))
    volts = (value * 3.3) / 1024
    temperature = volts / (10.0 / 1000)
    print ("%4d/1023 => %5.3f V => %4.1f �C" % (value, volts, temperature))
    time.sleep(0.5)
