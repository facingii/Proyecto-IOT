# -*- coding: utf-8 -*-

from lib2to3.pgen2.parse import ParseError
import pynmea2
import serial

class Geo:
	def __init__ (self, port, baudrate, timeout):
		self.port = port
		self.serial = serial.Serial (port, baudrate=baudrate, timeout=timeout)
		pynmea2.NMEAStreamReader ()

	'''
	Recover 
	'''
	def get (self):
		geo_point = {"latitude": 0, "longitude": 0}

		while True:
			try:
				data = self.serial.readline ()
				
				if str (data).__contains__ ('$GPRMC'): #if position is read successfully
					msg = pynmea2.parse (str (data, 'utf-8'))
					geo_point ["latitude"] = msg.latitude
					geo_point ["longitude"] = msg.longitude

					return geo_point
			except UnicodeDecodeError: #this error is expected when data doesn't contain parseable chars
				pass
			except ParseError:
				pass
			except Exception as error:
				raise error

