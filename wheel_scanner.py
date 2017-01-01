import sys
import time
import threading
import utils

from envirophat import analog
    
class WheelScanner:
 
  worker = None
  logger = None
  monitor = None
  revolution_counter = None
  reading_counter = None

  def start(self, logger, monitor):
    self.logger = logger
    self.monitor = monitor
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
    bottom_threshold = 2.35
    top_threshold = 2.45
    under = True
    value = 0  
    while True:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      self.reading_counter = self.reading_counter + 1
      value = analog.read(0)
      self.logger.log_hall_reading(time.time(), value, self.reading_counter)
      print ('hall value', value)
      if under and value > top_threshold:
        self.revolution_counter = self.revolution_counter + 1
        under = False
        self.logger.log_turn_event(time.time(), self.revolution_counter)
        #print 'half revolution:', self.revolution_counter
        self.monitor.notify_turn(self.revolution_counter)
      if not under and value < bottom_threshold:
        self.revolution_counter = self.revolution_counter + 1
        under = True
        self.logger.log_turn_event(time.time(), self.revolution_counter)
