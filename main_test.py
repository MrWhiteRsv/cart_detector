import sys
from test.wheel_scanner import hall_sensor_trainer_test

def main(argv):
  print ('hall_sensor_trainer_test' , 
      'pass' if hall_sensor_trainer_test.HallSensorTrainerTest().test() else 'fail')

if __name__ == '__main__':
  main(sys.argv[1:])