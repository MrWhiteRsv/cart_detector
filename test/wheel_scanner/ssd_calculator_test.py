from src.wheel_scanner import ssd_calculator

def test():

  lst = [0] * 50
  res = ssd_calculator.SsdCalculator.compute_ssd_signal(lst) 
  if (not res == [0] * 50):
    return False
    
  lst = [1] * 50
  res = ssd_calculator.SsdCalculator.compute_ssd_signal(lst) 
  if (not res == [0] * 50):
    return False

  return True
  