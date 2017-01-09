
import src.utils.utils
import ssd_calculator

from .. utils import histogram

class ActicityThrehsoldCalculator():
  
  @staticmethod 
  def compute_threshold(signal_lst):
    ssd_lst = ssd_calculator.SsdCalculator.compute_ssd_signal(signal_lst)
    ssd_range = ActicityThrehsoldCalculator.get_range(ssd_lst)
    ssd_histogram = histogram.Histogram(num_bins = 100,
        min_val = ssd_range['min'], max_val = ssd_range['max'])
    for val in ssd_lst: 
      ssd_histogram.add_sample(val)
    sorted_sample_count = sorted(ssd_histogram.get_sample_counts())
    min_bin_value_threshold = sorted_sample_count[70]
    trimmed_sample_count = map(
        lambda x: x if x >= min_bin_value_threshold else 0,
        ssd_histogram.get_sample_counts())
    indices = src.utils.utils.get_longest_run_indices(
        lst = trimmed_sample_count, val = 0)
    bottom_threshold = ssd_histogram.get_bins()[indices['start_index']]
    top_threshold = ssd_histogram.get_bins()[indices['end_index'] + 1]
    # print indices
    # print('ssd_range: ', ssd_range)
    # print('ssd_histogram: ', ssd_histogram.to_string()) 
    # print(sorted_sample_count)
    # print(min_bin_value_threshold)
    # print(trimmed_sample_count)
    return 0.5 * (bottom_threshold + top_threshold)
    
  @staticmethod 
  def get_range(lst):
    return {'min': min(lst), 'max': max(lst)}