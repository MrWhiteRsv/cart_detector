import sys
import time
import threading

from envirophat import analog

from signal_level import SignalLevel
from revolution_counter import RevolutionCounter
import src.utils.monitor
    
class WheelScanner:
 
  worker = None
  logger = None
  forward_counter = None
  backward_counter = None
  reading_counter = None
  sensor_0_bottom_threshold = 0
  sensor_0_top_threshold = 5
  sensor_1_bottom_threshold = 0
  sensor_1_top_threshold = 5
  sensor_0_buffer = None
  sensor_1_buffer = None
  
  def __init__(self, thresholds):
    if thresholds:  
      self.sensor_0_bottom_threshold = thresholds[0]['bottom_threshold']
      self.sensor_0_top_threshold = thresholds[0]['top_threshold']
      self.sensor_1_bottom_threshold = thresholds[1]['bottom_threshold']
      self.sensor_1_top_threshold = thresholds[1]['top_threshold']
    
  def get_sensor_0_buffer(self):
    return self.sensor_0_buffer

  def get_sensor_1_buffer(self):
    return self.sensor_1_buffer
    
  def start(self, logger, store_in_memory = False, monitor_wheel_turns = True):
    self.logger = logger
    self.worker = threading.Thread(target = self.start_continous_scan)
    self.forward_counter = 0
    self.backward_counter = 0
    self.reading_counter = 0
    self.worker.do_run = True 
    if store_in_memory:
      self.sensor_0_buffer = []
      self.sensor_1_buffer = []
    self.worker.start()
  
  def stop(self):
    self.logger = None
    self.worker.do_run = False
    self.worker.join()

  def start_continous_scan(self):
    sensor_0_level = SignalLevel.UNKNOWN
    sensor_1_level = SignalLevel.UNKNOWN
    rev_counter = RevolutionCounter()
    
    old_0 = None
    old_1 = None
    old_sum = 0
    while True:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      self.reading_counter = self.reading_counter + 1
      sensor_0_val = analog.read(0)
      sensor_1_val = analog.read(1)
      if self.logger != None:
        self.logger.get_hall_signal_0_logger().log_raw_signal_lst([sensor_0_val])
        self.logger.get_hall_signal_1_logger().log_raw_signal_lst([sensor_1_val])
      if self.sensor_0_buffer != None:
        self.sensor_0_buffer.append(sensor_0_val)
      if self.sensor_1_buffer != None:
        self.sensor_1_buffer.append(sensor_1_val)
      if self.logger:
        self.logger.log_hall_reading(time.time(), sensor_0_val, sensor_1_val,
            self.reading_counter)
      
      sensor_0_level = self.compute_signal_level(sensor_0_level,
          sensor_0_val, self.sensor_0_bottom_threshold, self.sensor_0_top_threshold)
      sensor_1_level = self.compute_signal_level(sensor_1_level,
          sensor_1_val, self.sensor_1_bottom_threshold, self.sensor_1_top_threshold)
      rev_counter_res = rev_counter.add_reading(sensor_0_level, sensor_1_level)
      src.utils.monitor.show_counter_0(rev_counter_res['forward'])
      src.utils.monitor.show_counter_1(rev_counter_res['backward'])

      """if old_0 != sensor_0_level or old_1 != sensor_1_level:
        old_0 = sensor_0_level 
        old_1 = sensor_1_level
        print ('old_0:' ,old_0  ,'old_1:' ,old_1) 
      if old_sum != rev_counter_res['forward'] + rev_counter_res['forward']:
        old_sum = rev_counter_res['forward'] + rev_counter_res['forward']
        print('sensor_0_level:', sensor_0_level, 'sensor_1_level:', sensor_1_level)   """   


  """ internals """
  def compute_signal_level(self, old_level, sensor_val, bottom_threshold, top_threshold):
    # Always return either HIGH or LOW value.
    # Switch state only if opposite threshold has been passed by sensor level.
    if old_level == SignalLevel.UNKNOWN:
      return SignalLevel.HIGH if sensor_val > top_threshold else SignalLevel.LOW
    if old_level == SignalLevel.LOW:
      return SignalLevel.HIGH if sensor_val > top_threshold else SignalLevel.LOW
    if old_level == SignalLevel.HIGH:
      return SignalLevel.HIGH if sensor_val > bottom_threshold else SignalLevel.LOW