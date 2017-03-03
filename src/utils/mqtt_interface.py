""" MQTT interface used to pub/sub from to the cloudmqtt message broker.
"""

import paho.mqtt.client as mqtt
import threading
    
class MqttInterface:
  worker = None
  client = None
  connection_statuts = None

  def connect(self):
    self.client = mqtt.Client()
    self.client.on_connect = self.on_connect
    self.client.on_message = self.on_message
    hostname = 'm13.cloudmqtt.com'
    self.client.username_pw_set(username = "oujibpyy", password = "-mKBDKwYQ1CC");
    self.client.connect(host = hostname, port = 11714)
    self.worker = threading.Thread(target = self.main_loop)
    self.worker.do_run = True
    self.worker.start()

  def disconnect(self):
    self.client.disconnect()
    self.client = None
    self.worker.join()
    self.worker = None

  def isConnected(self):
    return self.connection_statuts == 0
    
  def publish(self, topic, payload):
    if self.isConnected():
      self.client.publish(topic = topic, payload = payload)

  """ Internals """
  
  # The callback for when the client receives a CONNACK response from the server.
  def on_connect(self, client, userdata, flags, rc):
    print ("Connected with result code " + str(rc))
    self.connection_statuts = 0
    print ( self.client.subscribe('#'))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

  # The callback for when a PUBLISH message is received from the server.
  def on_message(self, client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
  def main_loop(self):
    self.client.loop_forever()





