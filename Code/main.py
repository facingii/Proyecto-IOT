#!/usr/bin/env python

from comm import broker
from sensors import dht11

import json
import datetime
import configparser

MQTT_HOST = ''
MQTT_PORT = 0
MQTT_TOPIC = ''
MQTT_CLIENT = ''
CONTAINER_ID = ''

def setup ():
	config = configparser.ConfigParser ()
	config.read ('config.ini')

	global MQTT_HOST
	MQTT_HOST = config ['MQTT']['HOST']
	
	global MQTT_PORT
	MQTT_PORT = int (config ['MQTT']['PORT'])

	global MQTT_TOPIC
	MQTT_TOPIC = config ['MQTT']['TOPIC']
	
	global MQTT_CLIENT
	MQTT_CLIENT = config ['MQTT']['CLIENT']
	
	global CONTAINER_ID
	CONTAINER_ID = int (config ['CONTAINER']['ID'])

if __name__ == "__main__":
	setup ()

	sensor = dht11.Temperature ()
	mqtt = broker.MQTT (MQTT_CLIENT, MQTT_HOST, MQTT_PORT)

	(temp, humidity) = sensor.get ()
	dt = datetime.datetime.now ()
	data = {'containerId': CONTAINER_ID, 'temperature': temp, 'humidity': humidity, 'timestamp': dt.__str__()}

	mqtt.publish (MQTT_TOPIC, json.dumps (data))