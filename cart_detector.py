""" Entry point for the entire cart scanner.

This module is responsible for
  1. Training the wheel scanner.
  2. Allocating a logger.
  3. Relaying the logger to these scanners.
  4. Starting and stopping the different scanners.

"""

import getopt
import sys
from threading import Timer
import time

from src.ble import ble_scanner
from src.gps import gps_scanner
from src.sensehat import sensehat_scanner
from src.wheel_scanner import wheel_scanner

import src.utils.logger
import src.utils.monitor
import src.wheel_scanner.trainer

def scan(log_file):
  training_logger = src.utils.logger.Logger()
  training_logger.open(run_name = log_file + '_training', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)  
  #thresholds = src.wheel_scanner.trainer.train_cart(training_logger)
  #thresholds = [{'top_threshold': 2.56648, 'bottom_threshold': 2.15752}, {'top_threshold': 2.5726299999999998, 'bottom_threshold': 2.1522099999999997}]
  #thresholds = [{'top_threshold': 2.74027, 'bottom_threshold': 2.30809}, {'top_threshold': 2.640295, 'bottom_threshold': 2.200765}]
  thresholds = [{'top_threshold': 2.7380649999999997, 'bottom_threshold': 2.3073550000000003}, {'top_threshold': 2.636935, 'bottom_threshold': 2.185645}]
  print thresholds
  #return
    
  logger = src.utils.logger.Logger()
  logger.open(run_name = log_file, log_to_mqtt_file = True,
      log_to_mqtt = True, log_to_stdout = False, log_to_txt_files = True)  
  
  gps_scanner_inst = gps_scanner.GpsScanner()
  ble_scanner_inst = ble_scanner.BleScanner()
  # sensehat_scanner_inst = sensehat_scanner.SensehatScanner()
  wheel_scanner_inst = wheel_scanner.WheelScanner(thresholds)
  gps_scanner_inst.open()
  gps_scanner_inst.start(logger)
  ble_scanner_inst.start(logger)
  wheel_scanner_inst.start(logger)
  time.sleep(3600)
  wheel_scanner_inst.stop()
  # sensehat_scanner_inst.stop()
  ble_scanner_inst.stop()
  gps_scanner_inst.stop()
  gps_scanner_inst.close()
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
  scan(log_file)

if __name__ == '__main__':
    main(sys.argv[1:])

