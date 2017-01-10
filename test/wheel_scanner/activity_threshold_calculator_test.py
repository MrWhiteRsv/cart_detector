from src.wheel_scanner import activity_threshold_calculator

def test():
  lst = [0] * 100 + [1, 0] * 100
  res = activity_threshold_calculator.compute_threshold(lst) 
  if (res > 0.15):
    return False
  return True
  