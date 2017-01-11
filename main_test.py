import sys

import src.utils.utils

from test.wheel_scanner import activity_threshold_calculator_test
from test.wheel_scanner import hall_sensor_trainer_test
from test.wheel_scanner import ssd_calculator_test
from test.wheel_scanner import turn_threshold_evaluator_test
from test.wheel_scanner import turn_threshold_optimizer_test

from test.utils import histogram_test
from test.utils import utils_test

def main(argv):
  if (False):
    raw = src.utils.utils.get_signal_from_file('run_0.dat', 'val_0')
    for i in range(len(raw)):
      print str(i) + ', ' + str(raw[i])
    return 
  
  print ('________ Turn Threshold Evaluator Test ________\n')
  res = turn_threshold_evaluator_test.test()
  print('pass' if res else 'fail')
  
  print ('________ Turn Threshold Optimizer Test ________\n')
  res = turn_threshold_optimizer_test.test()
  print('pass' if res else 'fail')

  print ('________ Activity Threshold Calculator Test ________\n')
  res = activity_threshold_calculator_test.test()
  print('pass' if res else 'fail')
  
  print ('________ SSD Calculator Test ________\n')
  res = ssd_calculator_test.test()
  print('pass' if res else 'fail')
  
  print ('________ Utils Test ________\n')
  res = utils_test.test()
  print('pass' if res else 'fail')
  
  print ('________ Histogram Test ________\n')
  res = histogram_test.HistogramTest().test()
  print('pass' if res else 'fail')
  
  print ('________ Hall Sensor Trainer Test ________\n')
  res = hall_sensor_trainer_test.HallSensorTrainerTest().test()
  print('pass' if res else 'fail')

if __name__ == '__main__':
  main(sys.argv[1:])