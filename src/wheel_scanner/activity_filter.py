""" This module is responsible to filter a signal both statically and dynamically
according to activity level. """

import ssd_calculator

def filter_signal(signal, activity_thrshold):
  assert signal
  assert activity_thrshold
  ssd_signal = ssd_calculator.SsdCalculator.compute_ssd_signal(signal)
  assert len(ssd_lst) == len(signal)
  result == []
  for i in range(len(signal)):
    if (ssd_signal[i] > activity_thrshold):
      result.append(signal[i])
  return result

