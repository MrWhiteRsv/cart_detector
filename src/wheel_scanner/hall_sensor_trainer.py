import collections

class HallSensorTrainer():

  activeBuffer = None
  
  def __init__(self):
    MAX_BUFFER_SIZE = 10000
    self.activeBuffer = collections.deque(maxlen = MAX_BUFFER_SIZE)

  def add_sample(self, value):
    print (value, len(self.activeBuffer))
    self.activeBuffer.append(value)
    
  def get_high_low_threshold(self):
    assert False, 'HallSensorTrainer.get_high_low_threshold not implemented yet!'
