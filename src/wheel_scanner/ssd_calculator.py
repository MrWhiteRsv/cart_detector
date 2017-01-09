""" This stateless class is responsible for calculating the Sampled Standard Deviation of
  a list of samples. """

import collections
import math

class SsdCalculator():
  
  @staticmethod 
  def compute_ssd_signal(lst, buffer_size = 80):
    local_ssd_buffer = collections.deque(maxlen = buffer_size)
    res = []
    for val in lst:
      local_ssd_buffer.append(val)
      ssd_value = SsdCalculator.compute_ssd_value(local_ssd_buffer)
      res.append(ssd_value)
    return res

  """ logic """
  
  @staticmethod    
  def compute_ssd_value(deq):
    sum = 0
    num_values = len(deq)
    if (num_values == 0):
      return None
    for val in deq:
      sum = sum + val
    avg = (sum / num_values)
    sN = 0
    for val in deq:
      sN = sN + pow((val - avg), 2)
    return math.sqrt(sN * 1. / num_values)

