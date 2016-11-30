import sys
import time
import threading
import utils

from envirophat import analog
    
class WheelScanner:
 
  worker = None
  logger = None
  revolution_counter = None
  reading_counter = None

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
    maxVal = -sys.float_info.max
    minVal = sys.float_info.max
    bottom_threshold = 1.55
    top_threshold = 1.72
    under = True
    while True:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      self.reading_counter = self.reading_counter + 1
      value = analog.read(0)
      self.logger.log_hall_reading(time.time(), value, self.reading_counter)
      maxVal = max(maxVal, value)
      minVal = min(minVal, value)
      if under and value > top_threshold:
        self.revolution_counter = self.revolution_counter + 1
        under = False
        self.logger.log_turn_event(time.time(), self.revolution_counter)
        print 'flip', self.revolution_counter
      if not under and value < bottom_threshold:
        self.revolution_counter = self.revolution_counter + 1
        under = True
        self.logger.log_turn_event(time.time(), self.revolution_counter)
        print 'flip', self.revolution_counter
