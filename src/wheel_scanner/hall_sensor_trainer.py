import collections
import math
import sys

from .. utils import histogram
from .. utils import logger

class HallSensorTrainer():

  LAG = 2
  ACTIVE_BUFFER_SIZE = 10000
  LOCAL_SSD_BUFFER_SIZE = 80
  GLOBAL_SSD_BUFFER_SIZE = 10000
  LPF_FILTER_WIDTH = 2
  
  """ state """
  activeBuffer = None
  filter_buffer = None
  local_ssd_buffer = None
  global_ssd_buffer = None
  ssd_histogram = None
  
  """ logging """
  logger = None
  sample_index = None

  def __init__(self):
    self.activeBuffer = collections.deque(maxlen = self.ACTIVE_BUFFER_SIZE)
    self.local_ssd_buffer = collections.deque(maxlen = self.LOCAL_SSD_BUFFER_SIZE)
    self.global_ssd_buffer = collections.deque(maxlen = self.GLOBAL_SSD_BUFFER_SIZE)
    self.filter_buffer = collections.deque(maxlen = 2 * self.LPF_FILTER_WIDTH + 1)
    self.ssd_histogram = histogram.Histogram(num_bins = 150, min_val = 0, max_val = 0.05)
    self.logger = logger.Logger()
    self.logger.open(mqtt_log_file_name = None, log_to_mqtt_file = True,
        log_to_mqtt = False, log_to_stdout = False)
    self.sample_index = 0

  def add_sample(self, sample):
    self.activeBuffer.append(sample)
    self.filter_buffer.append(sample)
    filtered_val = self.compute_filter_value()
    self.update_ssd_values(sample)
    
    if (self.sample_index >= self.LAG):
      sampled_val = self.activeBuffer[-(1 +	 self.LAG)]
      self.logger.log_training_reading(val = sampled_val, filtered_val = filtered_val,
          reading_counter = self.sample_index - self.LAG)
    self.sample_index = self.sample_index + 1
      
  def get_high_low_threshold(self):
    assert False, 'HallSensorTrainer.get_high_low_threshold not implemented yet!'
    
  def to_string(self):
    res = ''
    res = res + 'ssd_histogram: ' + self.ssd_histogram.to_string() + '\n'
    return res

  """ Logic """

  def update_ssd_values(self, sample):
    self.local_ssd_buffer.append(sample)
    ssd_value = self.compute_ssd_value()
    self.global_ssd_buffer.append(ssd_value)
    self.ssd_histogram.add_sample(ssd_value)

  def compute_filter_value(self):
    if (len(self.filter_buffer) == 0):
      return None
    sum = 0 
    for val in self.filter_buffer:
      sum = sum + val
    return (sum / len(self.filter_buffer))
    
  def compute_ssd_value(self):
    sum = 0
    if (len(self.local_ssd_buffer) == 0):
      return None
    for val in self.local_ssd_buffer:
      sum = sum + val
    avg = (sum / len(self.local_ssd_buffer))
    sN = 0
    for val in self.local_ssd_buffer:
      sN = sN + pow((val - avg), 2)
    sN = math.sqrt(sN * 1./(len(self.local_ssd_buffer)))
    return sN
