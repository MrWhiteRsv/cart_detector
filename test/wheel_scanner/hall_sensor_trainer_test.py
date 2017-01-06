import json
import os
import traceback

from src.wheel_scanner import hall_sensor_trainer

class HallSensorTrainerTest():

  def test(self):
    try:
      dir = os.path.dirname(__file__)
      input_file_name = os.path.join(dir, '../runs/run_0.dat')
      v0_output_file_name = os.path.join(dir, '../gen/gen_v0.txt')
      v1_output_file_name = os.path.join(dir, '../gen/gen_v1.txt')
      #extreme_output_file_name = os.path.join(dir, '../../test/gen/gen_ext.txt')
      input_file = open(input_file_name, 'r')
      v0_output_file = open(v0_output_file_name, 'w')
      v1_output_file = open(v1_output_file_name, 'w')
      trainer = hall_sensor_trainer.HallSensorTrainer()
      logging_index = 0
      for line in input_file:
        try: 
          parsed = json.loads(line)
        except Exception as inst:
          print parsed
          print ('parsing err')
          continue
        if (parsed['topic'] == 'cart/cartId/hall_reading'):
          logging_index = logging_index + 1
          trainer.add_sample(parsed['val_0'], logging_index)
          v0_output_file.write(str(logging_index) + ', ' + str(parsed['val_0']) + '\n')
          v1_output_file.write(str(logging_index) + ', ' + str(parsed['val_1']) + '\n')
      input_file.close()
      v0_output_file.close()
      v1_output_file.close()
      
    except Exception as inst:
      print (inst)
      traceback.print_exc()
      return False
      
    return True