import json
import paho.mqtt.publish as publish
import time
import unicornhat as unicorn

from threading import Timer

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False
    
# Taken as is from:
# http://www.raspberrypi-spy.co.uk/2012/06/finding-the-mac-address-of-a-raspberry-pi/#prettyPhoto
def getMAC(interface):
  # Return the MAC address of interface
  try:
    str = open('/sys/class/net/' + interface + '/address').read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]
   
class Monitor():
  
  def __init__(self):
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
     
  def rgb_of_color(self, color):
    return {
        'red': (200, 30, 30),
        'green': (30, 200, 30),
        'blue': (30, 30, 200),
        'black': (0, 0, 0),
        'yellow': (255, 255, 80),
        'purple': (128,0,128),
    }.get(color, (255, 255, 255))
    
  def set_pixel(self, row, col, color):
     (r, g, b) = self.rgb_of_color(color);
     unicorn.set_pixel(row, 3 - col, r, g, b)
     
  def notify_beacon(self, color):
    for row in range(0, 2):
      for col in range(0, 4):
        self.set_pixel(row, col, color)
    unicorn.show()
    
  def notify_turn(self, counter):
    # print 'monitor half revolution:', counter
    self.set_pixel(2, 0, 'black' if counter & 1 == 0 else 'yellow')
    self.set_pixel(3, 0, 'black' if counter & 2 == 0 else 'yellow')
    self.set_pixel(2, 1, 'black' if counter & 4 == 0 else 'yellow')
    self.set_pixel(3, 1, 'black' if counter & 8 == 0 else 'yellow')
    self.set_pixel(2, 2, 'black' if counter & 16 == 0 else 'yellow')
    self.set_pixel(3, 2, 'black' if counter & 32 == 0 else 'yellow')
    self.set_pixel(2, 3, 'black' if counter & 64 == 0 else 'yellow')
    self.set_pixel(3, 3, 'black' if counter & 128 == 0 else 'yellow')
    unicorn.show()
    
class Logger():

  log_file = None
  hall_file_0 = None
  hall_file_1 = None
  do_log_to_file = None
  do_log_to_mqtt = None
  do_log_to_stdout = None
  
  def open(self, log_file = 'logfile.dat', log_to_file = False, log_to_mqtt = False,
      log_to_stdout = True):
    self.log_file = open(log_file, 'w')
    self.hall_file_0 = open('hall_0.txt', 'w')
    self.hall_file_1 = open('hall_1.txt', 'w')
    self.do_log_to_file = log_to_file
    self.do_log_to_mqtt = log_to_mqtt
    self.do_log_to_stdout = log_to_stdout
        
  def close(self):
    self.log_file.close()
    self.log_file = None
    
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
    
  def log_turn_event(self, start_time, revolution_counter):
    key_val = dict(
        start_time = start_time,
        forward_counter = revolution_counter,
        backward_counter = 0)
    topic = "cart/cartId/revolution"
    self.log_event(topic, key_val)
    
  def log_hall_reading(self, start_time, val_0, val_1, reading_counter):
    key_val = dict(start_time = start_time, val_0 = val_0,
        reading_counter = reading_counter)
    topic = "cart/cartId/hall_reading"
    self.log_event(topic, key_val, bypass_mqtt = True)
    self.hall_file_0.write(str(reading_counter) + ', ' + str(val_0) + '\n')
    self.hall_file_1.write(str(reading_counter) + ', ' + str(val_1) + '\n')
    
  def log_event(self, topic, key_val, bypass_mqtt = False):
    if not bypass_mqtt:
      self.log_to_mqtt(topic, json.dumps(key_val))
    key_val['topic'] = topic
    payload = json.dumps(key_val)
    self.log_to_stdout(payload)
    self.log_to_file(payload)
    
  def log_to_stdout(self, payload):
    if not self.do_log_to_stdout:
      return
    print payload
      
  def log_to_mqtt(self, topic, payload):
    if not self.do_log_to_mqtt:
      return
    hostname = "li1109-31.members.linode.com"
    publish.single(topic, payload, hostname=hostname) 
    
  def log_to_file(self, payload):
    if not self.do_log_to_file:
      return
    if self.log_file == None:
      print 'ouch'
    else:
      self.log_file.write(payload)
      self.log_file.write('\n')
      
# Taken as is from:
# http://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer     = None
    self.interval   = interval
    self.function   = function
    self.args       = args
    self.kwargs     = kwargs
    self.is_running = False

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
