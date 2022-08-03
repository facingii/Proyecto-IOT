# -*- coding: utf-8 -*-

#MQTT Client
import paho.mqtt.client as mqtt

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
		print ("publishing to ", topic)
		return self.client.publish (topic, message).is_published ()
