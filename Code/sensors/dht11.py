#!/usr/bin/env python

import time
import json
# Adafruit
import board
import adafruit_dht

class Temperature:
	def __init__ (self):
		#Initialize the dht device, with data pin connected to:
		self.dhtDevice = adafruit_dht.DHT11(board.D4)

	def get (self):
		try:
			# Print the values to the serial port
			temperature_c = self.dhtDevice.temperature
			#temperature_f = temperature_c * (9 / 5) + 32
			humidity = self.dhtDevice.humidity
			return (temperature_c, humidity)
			#print(temperature_c)
			#print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
		except RuntimeError as error: # Errors happen fairly often, DHT's are hard to read, just keep going
			print(error.args[0])
