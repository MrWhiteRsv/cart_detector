""" This class is responsible to test the turn_treshold_optimzer. """

import random

from operator import add
from src.wheel_scanner import turn_threshold_optimizer


def test():
  signal = [0] * 100 + [1, 0] * 100
  res = turn_threshold_optimizer.optimize_thresholds(signal)
  if (res['bottom_threshold'] < 0.0 or res['bottom_threshold'] > 0.4):
    return False
  if (res['top_threshold'] < 0.6 or res['top_threshold'] > 1.1):
    return False  
  
  # shifted signal
  signal = [0] * 100 + [2, 1] * 100
  res = turn_threshold_optimizer.optimize_thresholds(signal)
  if (res['bottom_threshold'] < 0.9 or res['bottom_threshold'] > 1.4):
    return False
  if (res['top_threshold'] < 1.6 or res['top_threshold'] > 2.1):
    return False
  
  # scaled signal
  signal = [0] * 100 + [1, 0] * 100
  noise = [0.2 * random.random() for i in xrange(len(signal))]
  noisy_signal = map(add, signal, noise)
  res = turn_threshold_optimizer.optimize_thresholds(noisy_signal)
  if (res['bottom_threshold'] < 0.0 or res['bottom_threshold'] > 0.5):
    return False
  if (res['top_threshold'] < 0.7 or res['top_threshold'] > 1.2):
    return False

  return True