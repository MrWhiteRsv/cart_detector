import sys
import time
import threading

from envirophat import analog

from envirophat import motion

from signal_level import SignalLevel
from revolution_counter import RevolutionCounter
import src.utils.monitor
    
""" class responsible for any pinorinio sampling."""
class WheelScanner:
  worker = None
  logger = None
  reading_counter = None
  sensor_0_bottom_threshold = 0
  sensor_0_top_threshold = 5
  sensor_1_bottom_threshold = 0
  sensor_1_top_threshold = 5
  sensor_0_buffer = None
  sensor_1_buffer = None
  last_heading_sample_time = None
  heading_samples_counter = None
  accumelated_heading_sum = None
  sec_between_heading_loggings = 1
  
  def __init__(self, thresholds):
    if thresholds:  
      self.sensor_0_bottom_threshold = thresholds[0]['bottom_threshold']
      self.sensor_0_top_threshold = thresholds[0]['top_threshold']
      self.sensor_1_bottom_threshold = thresholds[1]['bottom_threshold']
      self.sensor_1_top_threshold = thresholds[1]['top_threshold']
      self.last_heading_sample_time = time.time()
      self.heading_samples_counter = 0
      self.accumelated_heading_sum = 0
    
  def get_sensor_0_buffer(self):
    return self.sensor_0_buffer

  def get_sensor_1_buffer(self):
    return self.sensor_1_buffer
    
  def start(self, logger, store_in_memory = False, monitor_wheel_turns = True):
    self.logger = logger
    self.worker = threading.Thread(target = self.start_continous_scan)
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

    while True:
      if (not getattr(self.worker, "do_run", True)) :
        break;
      self.reading_counter = self.reading_counter + 1
      sensor_0_val = analog.read(0)
      sensor_1_val = analog.read(1)
      #print ('sensor_0_val', sensor_0_val, 'sensor_1_val', sensor_1_val)
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
      if self.logger:
        if ((time.time() - self.last_heading_sample_time) > self.sec_between_heading_loggings) and self.heading_samples_counter > 0:
          self.logger.log_heading_event(start_time = time.time(), heading = (self.accumelated_heading_sum / self.heading_samples_counter))
          self.last_heading_sample_time = time.time()
          self.heading_samples_counter = 0
          self.accumelated_heading_sum = 0
        else:
          self.heading_samples_counter += 1
          self.accumelated_heading_sum += motion.heading()
      sensor_0_level = self.compute_signal_level(sensor_0_level,
          sensor_0_val, self.sensor_0_bottom_threshold, self.sensor_0_top_threshold)
      sensor_1_level = self.compute_signal_level(sensor_1_level,
          sensor_1_val, self.sensor_1_bottom_threshold, self.sensor_1_top_threshold)
      print ('sensor_1_level', sensor_1_level, 'sensor_1_val', sensor_1_val, self.sensor_1_bottom_threshold, self.sensor_1_top_threshold)
      rev_counter_res = rev_counter.add_reading(sensor_0_level, sensor_1_level)
      forward_counter = rev_counter_res['forward_revolutions_counter']
      backward_counter = rev_counter_res['backward_revolutions_counter']
      
      # ('forward_counter', forward_counter, 'backward_counter', backward_counter)      
      src.utils.monitor.show_counter_0(backward_counter)
      src.utils.monitor.show_counter_1(forward_counter)
      if (rev_counter_res['completed_forward_revolution'] or
          rev_counter_res['completed_backward_revolution']):
        if self.logger:
          self.logger.log_turn_event(time.time(), forward_counter, backward_counter,
              rev_counter_res['completed_forward_revolution'])

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