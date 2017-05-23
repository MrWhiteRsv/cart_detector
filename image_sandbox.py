""" Entry point for the entire cart scanner.

This module is responsible for
  1. Training the wheel scanner.
  2. Allocating a logger.
  3. Relaying the logger to these scanners.
  4. Starting and stopping the different scanners.

"""
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages/')

import getopt
import json

from threading import Timer
import time

import src.utils.logger
import src.utils.monitor
import src.utils.mqtt_interface

from src.gps import gps_scanner
from src.vision import image_scanner

class Controller:

  ble_scanner_inst = None
  mqtt_interface = None
  
  def publish_log(self, msg):
    json_msg = json.dumps({"msg" : msg})
    self.mqtt_interface.publish('cart/cartId/log', json_msg)

  def on_mqtt_message(self, client, userdata, msg):
    content = json.loads(msg.payload)
    if 'publishAd' in content:
      if content['publishAd']:
        src.utils.monitor.show_quality(src.utils.colors.Colors.GREEN)
      else:
        src.utils.monitor.show_quality(src.utils.colors.Colors.RED)
    elif 'command' in content:
      if content['command'] == 'snap':
        self.image_scanner_inst.snap()
      elif content['command'] == 'start_capture':
 		self.image_scanner_inst.start()
      elif content['command'] == 'stop_capture':
	  	self.image_scanner_inst.stop()
      elif content['command'] == 'set_name':
	  	self.image_scanner_inst.set_name(content['var'])
      else:
        print 'command: ' + content['command'] + ' not supported.' 
        
  def scan(self, log_file):
    self.mqtt_interface = src.utils.mqtt_interface.MqttInterface()
    self.mqtt_interface.connect(self.on_mqtt_message)
    logger = src.utils.logger.Logger(run_name = log_file, log_to_mqtt_file = True,
        mqtt_interface = self.mqtt_interface, log_to_mqtt = True, log_to_stdout = False,
        log_to_txt_files = True)  
    self.image_scanner_inst = image_scanner.ImageScanner()
    self.image_scanner_inst.init(logger, 'pic', self)
    
    time.sleep(3600)
    logger.close()

def main(argv):
  src.utils.monitor.init()
  log_file = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print 'sudo python image_sandox.py -o <log_file>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'sudo python image_sandox.py -o <log_file>'
      sys.exit()
    elif opt in ("-o", "--ofile"):
      log_file = arg
  controller = Controller()
  controller.scan(log_file)

if __name__ == '__main__':
    main(sys.argv[1:])




