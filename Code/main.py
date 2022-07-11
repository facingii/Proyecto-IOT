#!/usr/bin/env python

from comm import broker
from sensors import dht11, gps

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
	CONTAINER_ID = int (config ['CONTAINER']['ID'])

	global TEMP_MIN
	TEMP_MIN = int (config ['TEMPERATURE']['MIN'])

	global TEMP_MAX
	TEMP_MAX = int (config ['TEMPERATURE']['MAX'])

'''
Application entry point
'''
if __name__ == "__main__":
	setup ()

	#reading temperature data
	sensor = dht11.Temperature ()
	mqtt = broker.MQTT (MQTT_CLIENT, MQTT_HOST, MQTT_PORT)
	(temp, humidity) = sensor.get ()

	#reading geo point
	geo = gps.Geo (GPS_PORT, GPS_BAUD, GPS_TIMEOUT)
	geo_point = geo.get ()
	dt = datetime.datetime.now ()
	
	#building message to send via MQTT

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
	
	mqtt.publish (MQTT_TOPIC_COMMAND, json.dumps (command))
	time.sleep (0.3)
	mqtt.publish (MQTT_TOPIC_DATA, json.dumps (data))