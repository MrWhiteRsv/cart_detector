""" This class is responsible to test the turn_treshold_evaluator. """

from src.wheel_scanner import turn_threshold_evaluator

def test():
  signals_lst = [0, 1] * 50
  res = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signals_lst, bottom_threshold = 0.1, top_threshold = 0.9,
      min_level_samples = 1)
  if (res['overall_shifts'] != 99):
    return False
    
  signals_lst = [0, 0.3, 0.7, 1, 0.7, 0.3] * 50
  res = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signals_lst, bottom_threshold = 0.1, top_threshold = 0.9,
      min_level_samples = 1)
  if (res['overall_shifts'] != 99):
    return False

  signals_lst = [0, 0.3, 0.7, 1] * 50
  res = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signals_lst, bottom_threshold = 0.1, top_threshold = 0.9,
      min_level_samples = 1)
  if (res['overall_shifts'] != 99):
    return False

  signals_lst = [0.2, 0.8] * 50
  res = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signals_lst, bottom_threshold = 0.3, top_threshold = 0.9,
      min_level_samples = 1)
  if (res['overall_shifts'] != 0):
    return False  
  return True
