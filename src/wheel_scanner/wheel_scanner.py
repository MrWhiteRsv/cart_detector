import sys
import time
import threading

from envirophat import analog
    
class WheelScanner:
 
  worker = None
  logger = None
  revolution_counter = None
  reading_counter = None
  sensor_0_bottom_threshold = None
  sensor_0_top_threshold = None
  sensor_1_bottom_threshold = None
  sensor_1_top_threshold = None
  
  def __init__(self, thresholds):
    self.sensor_0_bottom_threshold = thresholds[0]['bottom_threshold']
    self.sensor_0_top_threshold = thresholds[0]['top_threshold']
    self.sensor_1_bottom_threshold = thresholds[1]['bottom_threshold']
    self.sensor_1_top_threshold = thresholds[1]['top_threshold']

  def start(self, logger):
    self.logger = logger
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.revolution_counter = 0
    self.reading_counter = 0
    self.worker.do_run = True 
    self.worker.start()
  
  def stop(self):
    self.logger = None
    self.worker.do_run = False
    self.worker.join()
    
  def start_continous_scan(self):
    under = True
    sensor_0_val = 0
    sensor_1_val = 0 
    while True:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      self.reading_counter = self.reading_counter + 1
      sensor_0_val = analog.read(0)
      sensor_1_val = analog.read(1)
      self.logger.log_hall_reading(time.time(), sensor_0_val,
          sensor_1_val, self.reading_counter)
      print ('hall sensor_0_val', sensor_0_val, 'hall sensor_1_val', sensor_1_val)
      if under and sensor_0_val > self.sensor_0_top_threshold:
        self.revolution_counter = self.revolution_counter + 1
        under = False
        self.logger.log_turn_event(time.time(), self.revolution_counter)
        # self.monitor.notify_turn(self.revolution_counter)
      if not under and sensor_0_val < self.sensor_0_bottom_threshold:
        self.revolution_counter = self.revolution_counter + 1
        under = True
        self.logger.log_turn_event(time.time(), self.revolution_counter)
