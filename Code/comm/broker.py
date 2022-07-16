# -*- coding: utf-8 -*-

#MQTT Client
import paho.mqtt.client as mqtt

MQTT_HOST = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "capstone/team15/temperature"
MQTT_MSG = ""

'''
Helper to handle connection to MQTT broker
'''
class MQTT:
	def __init__ (self, client_id, host, port):		
		self.client = mqtt.Client (client_id)
		connected = self.client.connect (host, port)
		
		if (connected == 0):
			print ("Client connected to %s:%s" % (host, port))
		else:
			raise Exception ("Error connecting to %s:%s" % (host, port))

	'''
	Send message to broker using topic indicated 
	'''
	def publish (self, topic, message):
		return self.client.publish (topic, message).is_published ()
