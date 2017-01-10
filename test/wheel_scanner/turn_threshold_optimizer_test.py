""" This class is responsible to test the turn_treshold_optimzer. """

import random

from operator import add

from src.wheel_scanner import turn_threshold_evaluator
from src.wheel_scanner import turn_threshold_optimizer

def test():

  # Simple example.
  signal = [0] * 100 + [1, 0] * 100
  if not evaluate_signal(signal, expected_result = 200):
    return False
  # inactive + active.
  signal = [0] * 100 + [1, 0] * 100
  if not evaluate_signal(signal, expected_result = 200):
    return False
  # shifted.
  signal = [0] * 100 + [4, 3] * 100
  if not evaluate_signal(signal, expected_result = 200):
    return False
  # scaled.
  signal = [0] * 100 + [4, 2] * 100
  if not evaluate_signal(signal, expected_result = 200):
    return False
  # inactive + active + noise.
  signal = [0] * 100 + [1, 0] * 100
  noise = [0.2 * random.random() for i in xrange(len(signal))]
  noisy_signal = map(add, signal, noise)
  if not evaluate_signal(noisy_signal, expected_result = 200):
    return False
    
  return True

""" logic """

def evaluate_signal(signal, expected_result):
  thresholds = turn_threshold_optimizer.optimize_thresholds(signal)
  evaluation = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signal, bottom_threshold = thresholds['bottom_threshold'],
      top_threshold =thresholds['top_threshold'] , min_level_samples = 1)
  return (evaluation['overall_shifts'] == expected_result)
