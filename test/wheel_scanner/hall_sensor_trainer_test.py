import json
import os
import traceback

from src.wheel_scanner import hall_sensor_trainer

class HallSensorTrainerTest():

  def test(self):
    try:
      dir = os.path.dirname(__file__)
      input_file_name = os.path.join(dir, '../runs/run_0.dat')
      input_file = open(input_file_name, 'r')
      trainer = hall_sensor_trainer.HallSensorTrainer()
      for line in input_file:
        try: 
          parsed = json.loads(line)
        except Exception as inst:
          print ('Parsing err, skipped line.')
          continue
        if (parsed['topic'] == 'cart/cartId/hall_reading'):
          trainer.add_sample(parsed['val_0'])
      input_file.close()
      
    except Exception as inst:
      print (inst)
      traceback.print_exc()
      return False
      
    return True