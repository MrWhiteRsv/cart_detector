""" This class is responsible to test the turn_treshold_optimzer. """

import random
from operator import add
from src.wheel_scanner import turn_threshold_evaluator
from src.wheel_scanner import turn_threshold_optimizer
import src.utils.utils

def test():
  # Simple example.
  signal = [0] * 100 + [1, 0] * 100
  if not evaluate_signal(signal, 200, 200):
    return False
  # inactive + active.
  signal = [0] * 100 + [1, 0] * 100
  if not evaluate_signal(signal, 200, 200):
    return False
  # shifted.
  signal = [0] * 100 + [4, 3] * 100
  if not evaluate_signal(signal, 200, 200):
    return False
  # scaled.
  signal = [0] * 100 + [4, 2] * 100
  if not evaluate_signal(signal, 200, 200):
    return False
  # inactive + active + noise.
  signal = [0] * 100 + [1, 0] * 100
  noise = [0.2 * random.random() for i in xrange(len(signal))]
  noisy_signal = map(add, signal, noise)
  if not evaluate_signal(noisy_signal, 200, 200):
    return False
  
  # inactive + 4 level active + noise.
  signal = [0] * 100 + [4, 3, 2, 2.5, 2, 1.5, 2, 1, 0, 1, 2, 1.5, 2, 2.5, 2, 3] * 100
  signal = signal + [0] * 100
  noise = [0.2 * random.random() for i in xrange(len(signal))]
  noisy_signal = map(add, signal, noise)
  if not evaluate_signal(noisy_signal, 200, 200):
    return False

  # signal #1  
  signal = src.utils.utils.get_signal_from_file('benchmark_0.dat', 'val_0')
  if (not signal):
    return False
  if not evaluate_signal(signal, 80, 90):
    return False

  # signal #2  
  signal = src.utils.utils.get_signal_from_file('benchmark_0.dat', 'val_1')
  if (not signal):
    return False
  if not evaluate_signal(signal, 80, 90): # ~90 Turns
   return False
  return True

""" logic """



def evaluate_signal(signal, miv_value, max_value):
  thresholds = turn_threshold_optimizer.optimize_thresholds(signal)
  # print ('top_threshold', thresholds['top_threshold'], 'bottom_threshold', thresholds['bottom_threshold'])
  evaluation = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signal, bottom_threshold = thresholds['bottom_threshold'],
      top_threshold = thresholds['top_threshold'] , min_level_samples = 1)
  # print('evaluation:', evaluation)
  return (evaluation['overall_shifts'] >= miv_value and
      evaluation['overall_shifts'] <= max_value)
