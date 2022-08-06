
/* Fecha: 05 de Agosto de 2022
 * 
 * Equipo 15 -  Proyecto:
 * 
 * Este programa se conecta al broker en hivemq.com y se suscribe al topico "capstone/team15/command"
 * para escuchar los comandos enviados desde la caja sensora.
 * 
 * Si la alarma es disparada por un incremento en la temperatura del contenedor, se ilumina el flash led.
 * Solo cuando la temperatura alcanza los rangos establecidos, la alarma luminica se restablece.
 * 
 */

//Bibliotecas
#include <WiFi.h>  // Biblioteca para el control de WiFi
#include <PubSubClient.h> //Biblioteca para conexion MQTT
#include <ArduinoJson.h>
#include <Arduino.h>

//Datos de WiFi
const char* ssid = "MANILAN";  // Aquí debes poner el nombre de tu red
const char* password = "082310.aeld.";  // Aquí debes poner la contraseña de tu red
const char* TOPIC_COMMAND = "capstone/team15/command";
const char* CONTAINER_ID = "1001";
const IPAddress server(18,195,236,18);

int flashLedPin = 4;

WiFiClient wifiClient; // Este objeto maneja los datos de conexion WiFi
PubSubClient client (wifiClient); // Este objeto maneja los datos de conexion al broker

void setup() {
  Serial.begin (115200);
  
  pinMode (flashLedPin, OUTPUT);
  digitalWrite (flashLedPin, LOW);

  Serial.println ();
  Serial.print ("Connecting to...");
  Serial.print (ssid);

  WiFi.begin (ssid, password);
  while (WiFi.status () != WL_CONNECTED) {
    Serial.print (".");
    delay (500);
  }

  Serial.println ("WiFi Connected");
  Serial.println ("IP Address");
  Serial.println (WiFi.localIP ());

  client.setServer (server, 1883);
  client.setCallback (callback);
  delay (500);
}

void loop() {
  if (!client.connected ()) {
    reconnect ();
  }

  client.loop ();
}

void callback (char* topic, byte* payload, unsigned int length) {
  Serial.print ("Message incoming in topic: ");
  Serial.print (topic);
  Serial.println ();

  char json[length + 1];
  strncpy (json, (char*) payload, length);
  json[length] = '\0';

  DynamicJsonDocument message(1024);
  deserializeJson(message, json);

  String containerId = message["containerId"];
  Serial.print ("Container ID:");
  Serial.print (containerId);
  
  if (containerId != CONTAINER_ID) return;

  String alarm = message["alarm"];
  Serial.print ("Alarm status:");
  Serial.println (alarm);
  
  if (alarm == "on") {
    digitalWrite(flashLedPin, HIGH);
    Serial.println ("Alarm was triggered!");
  } else {
    digitalWrite(flashLedPin, LOW);
  }
}

void reconnect () {
  while (!client.connected ()) {
    Serial.print ("Trying to connect...");

    if (client.connect ("ESP32CAMClient")) {
      Serial.println ("Connected!");
      client.subscribe (TOPIC_COMMAND);
    } else {
      Serial.print ("Connection failed!");
      Serial.print ("Error rc=");
      Serial.print (client.state ());

      delay (5000);

      Serial.println (client.connected ());
    }
  }
}
