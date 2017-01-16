""" This class is responsible to optimize the turn top and bottom thresholds. """

import activity_threshold_calculator
import ssd_calculator
import src.utils.utils
from src.utils import histogram

def optimize_thresholds_with_revolutions(signal_lst, revolutions):
  """ Evaluates the impact of the given thresholds on a signal_lst.
    
  Args:
    signal_lst: Samples of forward moving cart which has both an active and an
      inactive phase.
    revolutions: The number of revolutions the cart has done during training.
  
  Returns:
    A dict of the optimized thresholds, such that the most accurate rotation count
      will be detected. Example
    {'bottom_threshold' :  3.2, 'top_threshold' : 1.8}
  """
  print ('optimize_thrsholds_with_revolutions')
  return {}
    
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

  filtered_lst = []

  for i in range(len(ssd_lst)):
    if (ssd_lst[i] > activity_threshold):
      filtered_lst.append(signal_lst[i])
      if hall_signal_logger:
        hall_signal_logger.log_activity(i, 2.0)
  
  if (False):
    hist_range_bottom = min(float(s) for s in filtered_lst)
    hist_range_top = max(float(s) for s in filtered_lst)
  else:
    bottom_filtered_value = min(float(s) for s in filtered_lst)
    top_filtered_value = max(float(s) for s in filtered_lst)
  
    filtered_signals_histogram = histogram.Histogram(num_bins = 50,
        min_val = bottom_filtered_value, max_val = top_filtered_value)
    for val in filtered_lst:
      filtered_signals_histogram.add_sample(val)
    sorted_filtered_values = sorted(filtered_signals_histogram.get_sample_counts())
    min_bin_value_threshold = src.utils.utils.get_prefix_index(
        sorted_filtered_values, fraction = 0.03)
        
    trimmed_active_sample_count = map(
		    lambda x: x if x >= min_bin_value_threshold else 0,
		    filtered_signals_histogram.get_sample_counts())
    (hist_range_bottom, hist_range_top) = get_historam_range(
        filtered_signals_histogram.get_bins(), trimmed_active_sample_count)

  range_width = hist_range_top - hist_range_bottom
  res = {'bottom_threshold' : hist_range_bottom + 0.3 * range_width,
         'top_threshold' : hist_range_top -  0.3 * range_width}
         
  if (False): # debug
    print ('bottom_filtered_value:', bottom_filtered_value)
    print ('top_filtered_value:', top_filtered_value)
    print ('len(filtered_lst):', len(filtered_lst))
    print ('filtered_signals_histogram', filtered_signals_histogram.to_string())
    print ('sorted_filtered_values:', sorted_filtered_values)
    print ('min_bin_value_threshold:', min_bin_value_threshold)
    print('hist_range_bottom: ', hist_range_bottom)
    print('hist_range_top: ', hist_range_top)
    print res
    
  return res
  
""" logic """

def get_historam_range(bins, sample_count):
  bottom_bin_index = src.utils.utils.first_different_index(sample_count, 0)
  top_bin_index = src.utils.utils.last_different_index(sample_count, 0)
  return (bins[bottom_bin_index], bins[top_bin_index])
  