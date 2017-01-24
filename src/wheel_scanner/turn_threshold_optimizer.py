""" This class is responsible to optimize the turn top and bottom thresholds. """

import activity_threshold_calculator
import ssd_calculator
import src.utils.utils
from src.utils import histogram
    
def optimize_thresholds(signal_lst, hall_signal_logger = None):
  """ Evaluates the impact of the given thresholds on a signal_lst.
    
  Args:
    signal_lst: Samples of forward moving cart which has both an active and an
      inactive phase.
  
  Returns:
    A dict of the optimized thresholds, such that the most accurate rotation count
      will be detected. Example
    {'bottom_threshold' :  3.2, 'top_threshold' : 1.8}
  """

  activity_threshold = activity_threshold_calculator.compute_threshold(signal_lst)  
  ssd_lst = ssd_calculator.SsdCalculator.compute_ssd_signal(signal_lst)
  if hall_signal_logger:
    hall_signal_logger.log_activity_lst(ssd_lst)

  active_signal_lst = []

  for i in range(len(ssd_lst)):
    if (ssd_lst[i] > activity_threshold):
      active_signal_lst.append(signal_lst[i])
      if hall_signal_logger:
        hall_signal_logger.log_activity(i, 2.0)

  bottom_active_value = min(float(s) for s in active_signal_lst)
  top_active_value = max(float(s) for s in active_signal_lst)
  active_signals_histogram = histogram.Histogram(num_bins = 50,
      min_val = bottom_active_value, max_val = top_active_value)
  for val in active_signal_lst:
    active_signals_histogram.add_sample(val)
  sorted_active_values = sorted(active_signals_histogram.get_sample_counts())
  # filter outliers.
  min_bin_value_threshold = sorted_active_values[src.utils.utils.get_prefix_index(
      sorted_active_values, fraction = 0.03)]
  trimmed_active_sample_count = map(
      lambda x: x if x >= min_bin_value_threshold else 0,
      active_signals_histogram.get_sample_counts())
  hist_range = get_historam_range(
      active_signals_histogram.get_bins(), trimmed_active_sample_count)
  if hist_range == None:
    return hist_range
  (hist_range_bottom, hist_range_top) = hist_range
  range_width = hist_range_top - hist_range_bottom
  if (False): # debug
    print('signal_lst:', signal_lst)
    print('bottom_active_value:', bottom_active_value)
    print('top_active_value:', top_active_value)
    print('\n\n')
    print('active_signal_lst:', active_signal_lst)
    print('active_signals_histogram', active_signals_histogram.to_string())
    print('\n\n')
    print('sorted_active_values:', sorted_active_values)
    print('min_bin_value_threshold:', min_bin_value_threshold)
    print('hist_range_bottom: ', hist_range_bottom)
    print('hist_range_top: ', hist_range_top)
    print res

  res = {'bottom_threshold' : hist_range_bottom + 0.25 * range_width,
         'top_threshold' : hist_range_top -  0.25 * range_width}
         
  return res
  
""" logic """

def get_historam_range(bins, sample_count):
  bottom_bin_index = src.utils.utils.first_different_index(sample_count, 0)
  top_bin_index = src.utils.utils.last_different_index(sample_count, 0)
  if bottom_bin_index == None or top_bin_index == None:
    return None
  return (bins[bottom_bin_index], bins[top_bin_index])
  