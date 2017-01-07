import collections
import math
import sys

from .. utils import logger

class HallSensorTrainer():

  LAG = 2
  
  activeBuffer = None
  filter_buffer = None
  ssd_buffer = None
  
  logger = None
  sample_index = None
  

  def __init__(self):
    ACTIVE_BUFFER_SIZE = 10000
    SSD_BUFFER_SIZE = 80
    LPF_FILTER_WIDTH = 2
    
    self.activeBuffer = collections.deque(maxlen = ACTIVE_BUFFER_SIZE)
    self.ssd_buffer = collections.deque(maxlen = SSD_BUFFER_SIZE)
    self.filter_buffer = collections.deque(maxlen = 2 * LPF_FILTER_WIDTH + 1)
    self.logger = logger.Logger()
    self.logger.open(mqtt_log_file_name = None, log_to_mqtt_file = True,
        log_to_mqtt = False, log_to_stdout = True)
    self.sample_index = 0

  def add_sample(self, value):      
    self.activeBuffer.append(value)
    self.filter_buffer.append(value)
    self.ssd_buffer.append(value)
    filtered_val = self.compute_filter_value()
    ssd_value = self.compute_ssd_value()
    if (self.sample_index >= self.LAG):
      sampled_val = self.activeBuffer[-(1 +	 self.LAG)]
      self.logger.log_training_reading(val = sampled_val, filtered_val = ssd_value * 20,
          reading_counter = self.sample_index - self.LAG)
    self.sample_index = self.sample_index + 1
      
  def compute_filter_value(self):
    st = '('
    if (len(self.filter_buffer) == 0):
      return None
    sum = 0 
    for val in self.filter_buffer:
      sum = sum + val
      st = st + str(val) + ', '
    if False:
      st = st[:-2]
      st = st + ')'
      sys.stdout.flush()
      try:
        print st 
      except Exception as inst:
        print ('inst: ' + inst)
    return (sum / len(self.filter_buffer))
    
  def compute_ssd_value(self):
    sum = 0
    if (len(self.ssd_buffer) == 0):
      return None
    for val in self.ssd_buffer:
      sum = sum + val
    avg = (sum / len(self.ssd_buffer))
    sN = 0
    for val in self.ssd_buffer:
      sN = sN + pow((val - avg), 2)
    sN = math.sqrt(sN * 1./(len(self.ssd_buffer)))
    return sN

  def get_high_low_threshold(self):
   
    # find the the delta between extreme values
    # find the histogram of deltas
    # find the bigest threshold between histogram sorted values
    # find the set of 'clean' min max values
    # find a threshold based on these min / max values
    assert False, 'HallSensorTrainer.get_high_low_threshold not implemented yet!'

