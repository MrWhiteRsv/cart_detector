from src.wheel_scanner import hall_sensor_trainer

class HallSensorTrainerTest():

  def test(self):
    try:
      trainer = hall_sensor_trainer.HallSensorTrainer()
      trainer.add_sample(5)
    except Exception as inst:
      print (inst)
      return False
    return True