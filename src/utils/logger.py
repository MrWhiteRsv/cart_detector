import json
import os
import paho.mqtt.publish as publish

import hall_signal_logger

class Logger():

  mqtt_log_file = None
  do_log_to_mqtt_file = None
  do_log_to_mqtt = None
  do_log_to_stdout = None
  
  do_log_to_txt_files = None
  
  """ Grapher txt files, for debugging purposes. """
  hall_signal_0_logger = None
  hall_signal_1_logger = None
    
  #hall_file = None
  #hall_turn_file = None
  
  """ Getters. """
  def get_hall_signal_0_logger(self):
    return self.hall_signal_0_logger

  def get_hall_signal_1_logger(self):
    return self.hall_signal_1_logger

  """ Event logging. """
    
  def log_gps_event(self, start_time, lat, lon):
    key_val = dict(start_time = start_time, lat = lat, lon = lon)
    topic = "cart/cartId/gps"
    self.log_event(topic, key_val)

  def log_ble_event(self, mac, start_time, end_time, nearest_time, nearest_rssi):
    key_val = dict(mac = mac, start_time = start_time, end_time = end_time,
        nearest_time = nearest_time, nearest_rssi = nearest_rssi)   
    topic = "cart/cartId/ble"
    self.log_event(topic, key_val)
            
  def log_ble_raw(self, mac, time_sec, rssi):
    key_val = dict(mac = mac, time_sec = time_sec, rssi = rssi)
    topic = "cart/cartId/raw_ble"
    self.log_event(topic, key_val, bypass_mqtt = True)

  def log_gyro(self, start_time, yaw, pitch, roll):
    key_val = dict(start_time = start_time, yaw = yaw, pitch = pitch, roll = roll)
    topic = "cart/cartId/gyro"
    self.log_event(topic, key_val)
    
  def log_gyro_raw(self, start_time, yaw, pitch, roll):
    key_val = dict(start_time = start_time, yaw = yaw, pitch = pitch, roll = roll)
    topic = "cart/cartId/raw_gyro"
    self.log_event(topic, key_val, bypass_mqtt = True)
    
  def log_turn_event(self, start_time, forward_counter, backward_counter):
    key_val = dict(
        start_time = start_time,
        forward_counter = forward_counter,
        backward_counter = backward_counter)
    topic = "cart/cartId/revolution"
    self.log_event(topic, key_val)
    
  """ Scan logging. """
    
  def log_hall_reading(self, start_time, val_0, val_1, reading_counter):
    key_val = dict(start_time = start_time, val_0 = val_0, val_1 = val_1,
        reading_counter = reading_counter)
    topic = "cart/cartId/hall_reading"
    self.log_event(topic, key_val, bypass_mqtt = True)


  """ Internals. """
   
  def open(self, run_name = 'test_run', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = True, log_to_txt_files = False):
      
    if (log_to_mqtt_file):
      assert run_name and len(run_name) > 0, 'missing run name'
      mqtt_log_file_name = run_name + '.dat'
      self.mqtt_log_file = open(mqtt_log_file_name, 'w')
    self.do_log_to_txt_files = log_to_txt_files
    if (self.do_log_to_txt_files):
      assert run_name and len(run_name) > 0, 'missing run name'
      self.hall_signal_0_logger = hall_signal_logger.HallSignalLogger()
      self.hall_signal_1_logger = hall_signal_logger.HallSignalLogger()
      self.hall_signal_0_logger.open(run_name + '_signal_0')
      self.hall_signal_1_logger.open(run_name + '_signal_1')
    self.do_log_to_mqtt_file = log_to_mqtt_file
    self.do_log_to_mqtt = log_to_mqtt
    self.do_log_to_stdout = log_to_stdout
    dir = os.path.dirname(__file__)
    
  def close(self):
    self.mqtt_log_file.close()
    self.mqtt_log_file = None
    self.hall_signal_0_logger.close()
    self.hall_signal_1_logger.close()
          
  def log_event(self, topic, key_val, bypass_mqtt = False):
    if not bypass_mqtt:
      self.log_to_mqtt(topic, json.dumps(key_val))
    key_val['topic'] = topic
    payload = json.dumps(key_val)
    self.log_to_stdout(payload)
    self.log_to_mqtt_file(payload)
    
  def log_to_stdout(self, str):
    if not self.do_log_to_stdout:
      return
    print str
      
  def log_to_mqtt(self, topic, payload):
    if not self.do_log_to_mqtt:
      return
    hostname = 'm13.cloudmqtt.com'
    auth = {'username':"oujibpyy", 'password':"-mKBDKwYQ1CC"}
    publish.single(topic, payload, hostname=hostname, auth=auth, port=11714) 
    # hostname = "li1109-31.members.linode.com"
    # publish.single(topic, payload, hostname=hostname) 
    
  def log_to_mqtt_file(self, payload):
    if not self.do_log_to_mqtt_file:
      return
    if self.mqtt_log_file == None:
      raise Excetption()
    else:
      self.mqtt_log_file.write(payload)
      self.mqtt_log_file.write('\n')