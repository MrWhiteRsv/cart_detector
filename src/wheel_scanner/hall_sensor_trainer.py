import collections
import math
import sys

import src.utils.utils

from .. utils import histogram
from .. utils import logger

class HallSensorTrainer():

  LAG = 2
  ACTIVE_BUFFER_SIZE = 10000
  LOCAL_SSD_BUFFER_SIZE = 80
  GLOBAL_SSD_BUFFER_SIZE = 10000
  
  """ state """
  activeBuffer = None
  local_ssd_buffer = None
  global_ssd_buffer = None
  
  """ logging """
  logger = None
  sample_index = None

  def __init__(self):
    self.activeBuffer = collections.deque(maxlen = self.ACTIVE_BUFFER_SIZE)
    self.local_ssd_buffer = collections.deque(maxlen = self.LOCAL_SSD_BUFFER_SIZE)
    self.global_ssd_buffer = collections.deque(maxlen = self.GLOBAL_SSD_BUFFER_SIZE)
    self.logger = logger.Logger()
          
    self.logger.open(run_name = None, log_to_mqtt_file = False,
        log_to_mqtt = False, log_to_stdout = False)
    self.sample_index = 0

  def add_sample(self, sample):
    self.activeBuffer.append(sample)
    self.update_ssd_values(sample)
    if (self.sample_index >= self.LAG):
      sampled_val = self.activeBuffer[-(1 +	 self.LAG)]
      self.logger.log_training_reading(val = sampled_val, filtered_val = 2,
          reading_counter = self.sample_index - self.LAG)
    self.sample_index = self.sample_index + 1
      
  def get_high_low_threshold(self):
    ssd_support = self.get_ssd_support()
    ssd_histogram = histogram.Histogram(num_bins = 100,
        min_val = ssd_support['min'], max_val = ssd_support['max'])
    for val in self.global_ssd_buffer: 
      ssd_histogram.add_sample(val)
    sorted_sample_count = sorted(ssd_histogram.get_sample_counts())
    min_bin_value_threshold = sorted_sample_count[70]
    trimmed_sample_count = map(
        lambda x: x if x >= min_bin_value_threshold else 0,
        ssd_histogram.get_sample_counts())
    indices = src.utils.utils.get_longest_run_indices(
        lst = trimmed_sample_count, val = 0)
    bottom_threshold = ssd_histogram.get_bins()[indices['start_index']]
    top_threshold = ssd_histogram.get_bins()[indices['end_index'] + 1]    
    # print('ssd_dupport: ', ssd_support)
    # print('ssd_histogram: ', ssd_histogram.to_string()) 
    # print(sorted_sample_count)
    # print(min_bin_value_threshold)
    # print(trimmed_sample_count)
    return 0.5 * (bottom_threshold + top_threshold)
    
  def to_string(self):
    res = ''
    #res = res + 'ssd_histogram: ' + self.ssd_histogram.to_string() + '\n'
    return res

  """ Logic """

  def get_ssd_support(self):
    return {'min': min(self.global_ssd_buffer), 'max': max(self.global_ssd_buffer)}

  def update_ssd_values(self, sample):
    self.local_ssd_buffer.append(sample)
    ssd_value = self.compute_ssd_value()
    self.global_ssd_buffer.append(ssd_value)
    
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
