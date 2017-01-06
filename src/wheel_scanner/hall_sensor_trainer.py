import collections

from .. utils import logger

class HallSensorTrainer():

  activeBuffer = None
  logger = None
  sample_index = None

  def __init__(self):
    MAX_ACTIVE_BUFFER_SIZE = 10000
    self.activeBuffer = collections.deque(maxlen = MAX_ACTIVE_BUFFER_SIZE)
    self.logger = logger.Logger()
    self.logger.open(mqtt_log_file_name = None, log_to_mqtt_file = True,
        log_to_mqtt = False, log_to_stdout = True)
    self.sample_index = 0

  def add_sample(self, value):      
    self.activeBuffer.append(value)
    self.sample_index = self.sample_index + 1
    if (len(self.activeBuffer) > 2):
      val_n = self.activeBuffer[-1]
      val_nm1 = self.activeBuffer[-2]
      val_nm2 = self.activeBuffer[-3]
      self.logger.log_training_reading(val_n, self.sample_index)

  def get_high_low_threshold(self):
   
    # find the the delta between extreme values
    # find the histogram of deltas
    # find the bigest threshold between histogram sorted values
    # find the set of 'clean' min max values
    # find a threshold based on these min / max values
    assert False, 'HallSensorTrainer.get_high_low_threshold not implemented yet!'

