""" This class is responsible to test the turn_treshold_optimzer. """

import random

from operator import add
from src.wheel_scanner import turn_threshold_evaluator
from src.wheel_scanner import turn_threshold_optimizer

import src.utils.logger
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
  if not evaluate_signal(noisy_signal, 198, 203):
    return False

  # signal BM_0 sensor 0
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_0', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_0.dat', 'val_0')
  if (not signal): 
    return False
  if not evaluate_signal(signal, 90, 100, hall_signal_logger = None):  # ~95 Turns
    return False

  # signal BM_0 sensor 1
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_0_sensor_1', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_0.dat', 'val_1')
  if (not signal):
    return False
  if not evaluate_signal(signal, 95, 105, hall_signal_logger = None): # ~99 Turns
   return False
   
  # signal BM_1 sensor 0 
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_1_sensor_0', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_1.dat', 'val_0')
  if (not signal):
    return False
  if not evaluate_signal(signal, 154, 182, hall_signal_logger = None):  #168
    return False

  # signal BM_1 sensor 1 
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_1_sensor_1', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_1.dat', 'val_1')
  if (not signal):
    return False
  if not evaluate_signal(signal, 154, 182, hall_signal_logger = None):  #168
    return False

  # signal BM_2 sensor 0 (slightly slower revolutions) 
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_2_sensor_0', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_2.dat', 'val_0')
  if (not signal):
    return False
  if not evaluate_signal(signal, 140, 160, hall_signal_logger = None):  #150
    return False
  
  # signal BM_2 sensor 1 (slightly slower revolutions) 
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_2_sensor_1', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_2.dat', 'val_1')
  if (not signal):
    return False
  if not evaluate_signal(signal, 140, 160, hall_signal_logger = None):  #150
    return False
  
  # signal BM_3 sensor 0
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_3_sensor_0', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_3.dat', 'val_0')
  if (not signal):
    return False
  if not evaluate_signal(signal, 137, 153, hall_signal_logger = 
   logger.get_hall_signal_0_logger()):  #145
    return False

  # signal BM_3 sensor 1 
  logger =  src.utils.logger.Logger()
  logger.open(run_name = 'bm_3_sensor_1', log_to_mqtt_file = False,
      log_to_mqtt = False, log_to_stdout = False, log_to_txt_files = True)
  signal = src.utils.utils.get_signal_from_file('benchmark_3.dat', 'val_1')
  if (not signal):
    return False
  if not evaluate_signal(signal, 137, 153, hall_signal_logger = 
   logger.get_hall_signal_0_logger()):  #145
    return False
    
  return True

""" logic """

def evaluate_signal(signal, miv_value, max_value, hall_signal_logger = None):
  if hall_signal_logger:
    hall_signal_logger.log_raw_signal_lst(signal)
  thresholds = turn_threshold_optimizer.optimize_thresholds(signal)
  print ('thresholds: ', thresholds)
  if (thresholds == None):
    return False
  evaluation = turn_threshold_evaluator.evaluate_thrsholds(
      signal_lst = signal, bottom_threshold = thresholds['bottom_threshold'],
      top_threshold = thresholds['top_threshold'] , min_level_samples = 1,
      hall_signal_logger = hall_signal_logger)
  print('evaluation:', evaluation)
  return (evaluation['overall_shifts'] >= miv_value and
      evaluation['overall_shifts'] <= max_value)
