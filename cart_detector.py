# Responsible for starting and stopping the different scanners 

import getopt
import sys
from threading import Timer
import time

from src.ble import ble_scanner
from src.gps import gps_scanner
from src.sensehat import sensehat_scanner
from src.wheel_scanner import wheel_scanner

import src.utils.logger

def scan(log_file):
  logger = src.utils.logger.Logger()
  logger.open(run_name = log_file, log_to_mqtt_file = True, log_to_mqtt = False,
      log_to_stdout = False)
  gps_scanner_inst = gps_scanner.GpsScanner()
  ble_scanner_inst = ble_scanner.BleScanner()
  # sensehat_scanner_inst = sensehat_scanner.SensehatScanner()
  wheel_scanner_inst = wheel_scanner.WheelScanner()
  
  gps_scanner_inst.open()
  gps_scanner_inst.start(logger)
  ble_scanner_inst.start(logger)
  wheel_scanner_inst.start(logger)

  time.sleep(1800)
  
  wheel_scanner_inst.stop()
  # sensehat_scanner_inst.stop()
  ble_scanner_inst.stop()
  gps_scanner_inst.stop()
  gps_scanner_inst.close()
  logger.close()

def main(argv):
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
