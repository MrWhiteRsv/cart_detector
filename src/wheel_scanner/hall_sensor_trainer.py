import collections
import sys

from .. utils import logger

class HallSensorTrainer():

  LAG = 2
  
  activeBuffer = None
  filter_buffer = None
  logger = None
  sample_index = None
  

  def __init__(self):
    MAX_ACTIVE_BUFFER_SIZE = 10000
    LPF_FILTER_WIDTH = self.LAG
    
    self.activeBuffer = collections.deque(maxlen = MAX_ACTIVE_BUFFER_SIZE)
    self.filter_buffer = collections.deque(maxlen = 2 * LPF_FILTER_WIDTH + 1)
    self.logger = logger.Logger()
    self.logger.open(mqtt_log_file_name = None, log_to_mqtt_file = True,
        log_to_mqtt = False, log_to_stdout = True)
    self.sample_index = 0

  def add_sample(self, value):      
    self.activeBuffer.append(value)
    self.filter_buffer.append(value)
    filtered_val = self.compute_filter_value()
    if (self.sample_index >= self.LAG):
      val = self.activeBuffer[-(1 +	 self.LAG)]
      self.logger.log_training_reading(val = val, filtered_val = filtered_val,
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

  def get_high_low_threshold(self):
   
    # find the the delta between extreme values
    # find the histogram of deltas
    # find the bigest threshold between histogram sorted values
    # find the set of 'clean' min max values
    # find a threshold based on these min / max values
    assert False, 'HallSensorTrainer.get_high_low_threshold not implemented yet!'

