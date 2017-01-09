import sys

from test.wheel_scanner import hall_sensor_trainer_test
from test.wheel_scanner import ssd_calculator_test

from test.utils import histogram_test
from test.utils import utils_test

def main(argv):

  print ('________ SSD Calculator Test ________\n')
  res = ssd_calculator_test.test()
  print ('res:', 'pass' if res else 'fail')
  print('\n')
  
  """ print ('________ Utils Test ________\n')
  res = utils_test.test()
  print ('res:', 'pass' if res else 'fail')
  print('\n')
  
  print ('________ Histogram Test ________\n')
  res = histogram_test.HistogramTest().test()
  print ('res:', 'pass' if res else 'fail')
  print('\n')
  
  print ('________ Hall Sensor Trainer Test ________\n')
  res = hall_sensor_trainer_test.HallSensorTrainerTest().test()
  print ('res:', 'pass' if res else 'fail')
  print('\n')
  """

if __name__ == '__main__':
  main(sys.argv[1:])