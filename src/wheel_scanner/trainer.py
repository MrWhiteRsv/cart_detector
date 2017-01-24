""" 
This module is responsible for learning the specifics of the cart sensors.
""" 

import src.utils.monitor
import sys
import threading
import time

from envirophat import analog
from src.utils.colors import Colors
from src.wheel_scanner import turn_threshold_evaluator
from src.wheel_scanner import turn_threshold_optimizer
from src.wheel_scanner import wheel_scanner
from py_beacon.proximity import *

def train_cart(logger):
  monitor = src.utils.monitor
  wheel_scanner_inst = wheel_scanner.WheelScanner(thresholds = None)
  thresholds = [{'top_threshold': 0, 'bottom_threshold': 5},
    {'top_threshold': 0, 'bottom_threshold': 5}]
  while True:
    monitor.show_beacon_on(Colors.RED)
    wait_for_start()
    wheel_scanner_inst.start(logger = None, store_in_memory = True)
    monitor.show_quality(Colors.BLACK)
    monitor.show_beacon_on(Colors.YELLOW)
    time.sleep(3)
    monitor.show_beacon_on(Colors.GREEN)
    time.sleep(1)  
    monitor.show_beacon_off()
    monitor.show_arrow_top(Colors.GREEN)
    time.sleep(20)
    monitor.show_stop_moving()
    time.sleep(10)
    monitor.show_arrow_bottom(Colors.GREEN)
    time.sleep(20)
    wheel_scanner_inst.stop()
    signal_0 = wheel_scanner_inst.get_sensor_0_buffer()
    signal_1 = wheel_scanner_inst.get_sensor_1_buffer()
    if logger != None:
        logger.get_hall_signal_0_logger().log_raw_signal_lst(signal_0)
        logger.get_hall_signal_1_logger().log_raw_signal_lst(signal_1)
    thresholds[0] = turn_threshold_optimizer.optimize_thresholds(signal_0)
    thresholds[1] = turn_threshold_optimizer.optimize_thresholds(signal_1)
    evaluate_quality(signal_0, signal_1, thresholds, logger)
        
    if True: # TODO(oded): halt only if quality is ok.
      monitor.show_beacon_off()
      monitor.clear_direction()
      monitor.show_quality(Colors.GREEN)
      break
    monitor.show_quality(Colors.RED)
    continue
  return thresholds
    
def evaluate_quality(signal_0, signal_1, thresholds, logger):
  evaluation_0 = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signal_0, bottom_threshold = thresholds[0]['bottom_threshold'],
      top_threshold = thresholds[0]['top_threshold'] , min_level_samples = 1,
      hall_signal_logger = logger.get_hall_signal_0_logger())
  evaluation_1 = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signal_1, bottom_threshold = thresholds[1]['bottom_threshold'],
      top_threshold = thresholds[1]['top_threshold'] , min_level_samples = 1,
      hall_signal_logger = logger.get_hall_signal_1_logger())
  print('evaluation_0:', evaluation_0)
  print('evaluation1:', evaluation_1)
  
def wait_for_start():
  start_training_beacon = '34:b1:f7:d3:9c:cb'
  scanner = Scanner()
  continue_scan = True
  while continue_scan:
    for beacon in scanner.scan():
      fields = beacon.split(",")
      mac = fields[0]   
      if mac == start_training_beacon:
        rssi = int(fields[5])
        if rssi > -67:
          continue_scan = False