import sys

from test.wheel_scanner import hall_sensor_trainer_test
from test.utils import histogram_test

def main(argv):
      
  print ('________ Histogram Test ________\n')
  res = histogram_test.HistogramTest().test()
  print ('res:', 'pass' if res else 'fail')
  print('\n')
  
  print ('________ Hall Sensor Trainer Test ________\n')
  res = hall_sensor_trainer_test.HallSensorTrainerTest().test()
  print ('res:', 'pass' if res else 'fail')
  print('\n')
  
if __name__ == '__main__':
  main(sys.argv[1:])