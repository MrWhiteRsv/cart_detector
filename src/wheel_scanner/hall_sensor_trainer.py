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
    self.logger.open(mqtt_log_file_name = None, log_to_mqtt_file = True,
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
    print(trimmed_sample_count)
    indices = src.utils.utils.get_longest_run_indices(
        lst = trimmed_sample_count, val = 0)
    print indices
    bottom_threshold = ssd_histogram.get_bins()[indices['start_index']]
    top_threshold = ssd_histogram.get_bins()[indices['end_index'] + 1]
    print (0.5 * (bottom_threshold + top_threshold))
    
    #print('ssd_dupport: ', ssd_support)
    print('ssd_histogram: ', ssd_histogram.to_string()) 
    #print(sorted_sample_count)
    #print(min_bin_value_threshold)
    #print(trimmed_sample_count)
    return 0.5 * (bottom_threshold + top_threshold)
    
  def to_string(self):
    res = ''
    #res = res + 'ssd_histogram: ' + self.ssd_histogram.to_string() + '\n'
    return res

  """ Logic """

  """@staticmethod
  def get_longest_run_indices(lst, val):
    if len(lst) == 0: 
      return None
    min_run_length = 0
    current_run_length = 0
    max_start_index = None
    max_end_index = None
    max_run_length = 0
    
    before_first_instance = True
    for i in range(0, len(lst)):
      if before_first_instance:
        if lst[i] == val:
          max_start_index = i
          max_end_index = i
          before_first_instance = False
          current_run_length = 1
        continue
      curr_equal_val = (lst[i] == val)
      prev_equal_val = (lst[i - 1] == val)
      current_run_length = 0 if (not prev_equal_val) else current_run_length + 1
      if (current_run_length > max_run_length):
        max_run_length = current_run_length
        max_end_index = i
        max_start_index = i - current_run_length + 1
        
    
    print ('max_start_index:', max_start_index, 'max_end_index:', max_end_index, 'current_run_length:', max_run_length)
        """

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
