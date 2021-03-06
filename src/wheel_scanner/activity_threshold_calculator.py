""" This module is responsible to compute a threshold for the Standard Deviation (SD) 
that will differentiate between times in which the signal is active (rotating wheel) and
inactive (stationary). """

import src.utils.utils
import ssd_calculator

from .. utils import histogram

def compute_threshold(signal_lst):
  ssd_lst = ssd_calculator.SsdCalculator.compute_ssd_signal(signal_lst)
  ssd_range = get_range(ssd_lst)
  ssd_histogram = histogram.Histogram(num_bins = 100,
    min_val = ssd_range['min'], max_val = ssd_range['max'])
  for val in ssd_lst: 
    ssd_histogram.add_sample(val)
  sorted_sample_count = sorted(ssd_histogram.get_sample_counts())
  min_bin_value_threshold = sorted_sample_count[70]
  trimmed_sample_count = map(
    lambda x: x if x >= min_bin_value_threshold else 0,
    ssd_histogram.get_sample_counts())
  longest_run_indices = src.utils.utils.get_longest_central_run_indices(
    lst = trimmed_sample_count, val = 0)

  if (not longest_run_indices):
    return None
  
  bottom_threshold = ssd_histogram.get_bins()[longest_run_indices['start_index']]
  top_threshold = ssd_histogram.get_bins()[longest_run_indices['end_index'] + 1]
  activity_threshold = 0.5 * (bottom_threshold + top_threshold)
  if (False): # debug
    print('signal_lst:', signal_lst)
    print('\n\n')
    print('ssd_lst:', ssd_lst)
    print('\n\n')
    print('ssd_histogram: ', ssd_histogram.to_string())
    print('trimmed_ssd_count:', trimmed_sample_count) 
    print('longest_run_indices: ', longest_run_indices)
    print('bottom_threshold: ', bottom_threshold)
    print('top_threshold: ', top_threshold)
    print('activity threshold: ', activity_threshold)
    print('\n\n')
    print('activity signal (0:inactive, 1: active):',
        map(lambda x : 0 if x < activity_threshold else 1, ssd_lst))

  return activity_threshold

def get_range(lst):
  return {'min': min(lst), 'max': max(lst)}