import sys

from test.wheel_scanner import hall_sensor_trainer_test
from test.utils import histogram_test

def main(argv):
  #print ('hall_sensor_trainer_test' , 
  #    'pass' if hall_sensor_trainer_test.HallSensorTrainerTest().test() else 'fail')
  print ('________ Histogram Test ________\n')
  res = histogram_test.HistogramTest().test()
  print ('histogram_test res:', 'pass' if res else 'fail')
  print('\n')

if __name__ == '__main__':
  main(sys.argv[1:])