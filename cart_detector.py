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

from src.ble import ble_scanner
from src.gps import gps_scanner
from src.sensehat import sensehat_scanner
from src.wheel_scanner import wheel_scanner

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

import src.utils.logger
import src.utils.monitor
import src.utils.mqtt_interface
import src.wheel_scanner.trainer

class Controller:

  def on_mqtt_message(self, client, userdata, msg):
    content = json.loads(msg.payload)
    if 'publishAd' in content:
      if content['publishAd']:
        src.utils.monitor.show_quality(src.utils.colors.Colors.GREEN)
      else:
        src.utils.monitor.show_quality(src.utils.colors.Colors.RED)
    if 'captureImageWithCart' in content:
      # TODO(oded): handle this.
      print ('image_name', content['image_name']);
      camera = PiCamera()
      rawCapture = PiRGBArray(camera)
      # allow the camera to warmup
      time.sleep(0.1)
      camera.capture(rawCapture, format="bgr")
      image = rawCapture.array
      cv2.imwrite('bla.png', image)
    if 'changeThreshold' in content:
      # TODO(oded): handle this.
      print ('mac', content['mac']);
      print ('threshold', content['threshold']);  

  def scan(self, log_file):
    mqtt_interface = src.utils.mqtt_interface.MqttInterface()
    mqtt_interface.connect(self.on_mqtt_message)
    mqtt_interface.publish('cart/cartId/test', 'hello mqtt pi')
    # mqtt_interface.publish(topic='cart/cartId/test', payload = 'hello mqtt pi')
    training_logger = src.utils.logger.Logger(run_name = log_file + '_training',
        log_to_mqtt_file = False, mqtt_interface = mqtt_interface, log_to_mqtt = False,
        log_to_stdout = True, log_to_txt_files = False)  
    #thresholds = src.wheel_scanner.trainer.train_cart(training_logger)
    thresholds = [{'top_threshold': 2.69, 'bottom_threshold': 2.23},
         {'top_threshold': 2.61, 'bottom_threshold': 2.16}]
    print thresholds     
    logger = src.utils.logger.Logger(run_name = log_file, log_to_mqtt_file = True,
        mqtt_interface = mqtt_interface, log_to_mqtt = True, log_to_stdout = True,
        log_to_txt_files = True)  
    #gps_scanner_inst = gps_scanner.GpsScanner()
    ble_scanner_inst = ble_scanner.BleScanner()
    # sensehat_scanner_inst = sensehat_scanner.SensehatScanner()
    wheel_scanner_inst = wheel_scanner.WheelScanner(thresholds)
    #gps_scanner_inst.open()
    #gps_scanner_inst.start(logger)
    ble_scanner_inst.start(logger)
    wheel_scanner_inst.start(logger)
    time.sleep(3600)
    wheel_scanner_inst.stop()
    # sensehat_scanner_inst.stop()
    ble_scanner_inst.stop()
    #gps_scanner_inst.stop()
    #gps_scanner_inst.close()
    logger.close()

def main(argv):
  src.utils.monitor.init()
  log_file = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print 'sudo python cart_detector.py -o <log_file>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'sudo python cart_detector.py -o <log_file>'
      sys.exit()
    elif opt in ("-o", "--ofile"):
      log_file = arg
  controller = Controller()
  controller.scan(log_file)

if __name__ == '__main__':
    main(sys.argv[1:])

