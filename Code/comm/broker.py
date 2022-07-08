#!/usr/bin/env python

#MQTT Client
import time
import paho.mqtt.client as mqtt

MQTT_HOST = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "capstone/team15/temperature"
MQTT_MSG = ""


class MQTT:
	def __init__ (self, client_id, host, port):		
		self.client = mqtt.Client (client_id)
		connected = self.client.connect (host, port)
		
		if (connected == 0):
			print ("Client connected to %s:%s" % (host, port))
		else:
			raise Exception ("Error connecting to %s:%s" % (host, port))

	def publish (self, topic, message):
		return self.client.publish (topic, message).is_published ()


#def on_publish (client, userdata, mid):
#    print ("on_publish")
#    print (userdata)
#    print (client)
#    print (mid)

#def on_connect (client, userdata, flags, rc):
#    print ("on_connect")
#    if (rc == 0):
#        print ("Connected to MQTT Broker!")
#    else:
#        print ("Failed to connect, return code %d\n", rc)
    #client.subscribe (MQTT_TOPIC)
    #client.publish (MQTT_TOPIC, "PERLA KARINA")

#def on_message (client, userdata, msg):
#    print ("on_message")
#    print (msg)

# Setting up MQTT Client
#mqttc = mqtt.Client("PKATGASM")
#mqttc.on_publish = on_publish
#mqttc.on_connect = on_connect
#mqttc.on_message = on_message

#mqttc.connect (MQTT_HOST, MQTT_PORT)
#mqttc.subscribe (MQTT_TOPIC)
#mqttc.publish (MQTT_TOPIC)
#mqttc.loop_start ()
#time.sleep (5)
#mqttc.loop_stop ()
#mqttc.disconnect ()