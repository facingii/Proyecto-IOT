#!/usr/bin/env python
# -*- coding: utf-8 -*-

from locale import normalize
from comm import broker
from sensors import dht11, gps
from db import db

import os
import time
import json
import datetime
import configparser

MQTT_HOST = ''
MQTT_PORT = 0
MQTT_TOPIC_DATA = ''
MQTT_TOPIC_COMMAND = ''
MQTT_CLIENT = ''
GPS_PORT = 0
GPS_BAUD = 0
GPS_TIMEOUT = 0
CONTAINER_ID = ''
TEMP_MIN = 0
TEMP_MAX = 0
DB_FILENAME = ''

'''
Setting up environment variables
'''
def setup ():
	config_file_path = os.path.join (os.path.dirname (__file__), 'conf', 'config.ini')
	config = configparser.ConfigParser ()
	config.read (config_file_path)

	global MQTT_HOST
	MQTT_HOST = config ['MQTT']['HOST']
	
	global MQTT_PORT
	MQTT_PORT = int (config ['MQTT']['PORT'])

	global MQTT_TOPIC_DATA
	MQTT_TOPIC_DATA = config ['MQTT']['TOPIC']

	global MQTT_TOPIC_COMMAND
	MQTT_TOPIC_COMMAND = config ['MQTT']['COMMAND']
	
	global MQTT_CLIENT
	MQTT_CLIENT = config ['MQTT']['CLIENT']
	
	global GPS_PORT
	GPS_PORT = config ['GPS']['PORT']

	global GPS_BAUD
	GPS_BAUD = int (config ['GPS']['BAUD'])

	global GPS_TIMEOUT
	GPS_TIMEOUT = float (config ['GPS']['TIMEOUT'])

	global CONTAINER_ID
	CONTAINER_ID =  (config ['CONTAINER']['ID'])

	global TEMP_MIN
	TEMP_MIN = int (config ['TEMPERATURE']['MIN'])

	global TEMP_MAX
	TEMP_MAX = int (config ['TEMPERATURE']['MAX'])

	global DB_FILENAME
	DB_FILENAME = config ['DATABASE']['FILENAME']

'''
Application entry point
'''
if __name__ == "__main__":
	setup ()

	#reading temperature data
	sensor = dht11.Temperature ()
	(temp, humidity) = sensor.get ()

	#reading geo point
	geo = gps.Geo (GPS_PORT, GPS_BAUD, GPS_TIMEOUT)
	geo_point = geo.get ()
	dt = datetime.datetime.now ()
	
	#build messages to send via MQTT
	command = {'alarm': 'off'}

	data = {'containerId': CONTAINER_ID, 'temperature': temp, 
			'humidity': humidity, 
			'timestamp': dt.__str__(),
			'status': 'ok', 
			'geo': {'latitude': geo_point ['latitude'], 'longitude': geo_point ['longitude']}}

	#after each temperature read that value is compared against temperature threshold
	#and an alarm is triggered accordingly to it
	if temp < TEMP_MIN or temp > TEMP_MAX:
		command ['alarm'] = 'on'
		data ['status'] = 'failed'
	
	db_filepath = os.path.join (os.path.dirname (__file__), 'data', DB_FILENAME)

	try:
		mqtt = broker.MQTT (MQTT_CLIENT, MQTT_HOST, MQTT_PORT)
		#send data & commnd 
		mqtt.publish (MQTT_TOPIC_DATA, json.dumps (data))
		time.sleep (0.4)
		mqtt.publish (MQTT_TOPIC_COMMAND, json.dumps (command))

		#verify if exist any data storage locally, if so, send it
		persistance = db.Persistance (db_filepath)
		if persistance.num_rows () > 0:
			pending = persistance.get_data ()

			#normalize status for data stored
			for item in pending:
				if item ['temperature'] < TEMP_MIN or item ['temperature'] > TEMP_MAX:
					item ['status'] = 'failed'

			#sending pending data 
			#try:
			#	[mqtt.publish (MQTT_TOPIC_DATA, json.dumps (item)) for item in pending]
			#	persistance.remove ()
			#except:
			#	pass

			persistance.close ()
	except Exception as e:
		#if data wasn't sent to broker it is storage into local db
		persistance = db.Persistance (db_filepath)
		persistance.insert (data)
		persistance.close ()

		raise e

