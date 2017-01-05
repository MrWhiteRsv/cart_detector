from src.wheel_scanner import hall_sensor_trainer

import os
import json

class HallSensorTrainerTest():

  def test(self):
    try:
      dir = os.path.dirname(__file__)
      file_name = os.path.join(dir, '../../runs/v3.dat')
      test_file = open(file_name, 'r')
      trainer = hall_sensor_trainer.HallSensorTrainer()
      for line in test_file:
        try: 
          parsed = json.loads(line)
        except Exception as inst:
          print ('parsing err')
          continue
        trainer.add_sample(parsed['val_0'])

    except Exception as inst:
      print (inst)
      return False
    return True