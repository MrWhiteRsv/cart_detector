from src.wheel_scanner import revolution_counter
from src.wheel_scanner.signal_level import SignalLevel

def test():
  if not test_forward():
    return False
  if not test_forward_and_backward():
    return False
  if not test_illegal_transition_and_forward():
    return False
  return True

def test_forward():
  rev_counter = revolution_counter.RevolutionCounter()
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  if res['forward'] != 0 or res['backward'] != 0 or res['illegeal'] != 0:
    return False
  rev_counter.add_reading(SignalLevel.LOW, SignalLevel.HIGH)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.HIGH)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.LOW)
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  if res['forward'] != 4 or res['backward'] != 0 or res['illegeal'] != 0:
    return False
  return True
  
def test_forward_and_backward():
  rev_counter = revolution_counter.RevolutionCounter()
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  rev_counter.add_reading(SignalLevel.LOW, SignalLevel.HIGH)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.HIGH)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.LOW)
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.LOW)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.HIGH)
  rev_counter.add_reading(SignalLevel.LOW, SignalLevel.HIGH)
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  if res['forward'] != 4 or res['backward'] != 4 or res['illegeal'] != 0:
    return False
  return True

def test_illegal_transition_and_forward():
  rev_counter = revolution_counter.RevolutionCounter()
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  rev_counter.add_reading(SignalLevel.LOW, SignalLevel.HIGH)
  rev_counter.add_reading(SignalLevel.HIGH, SignalLevel.LOW)
  res = rev_counter.add_reading(SignalLevel.LOW, SignalLevel.LOW)
  
  if res['forward'] != 2 or res['backward'] != 0 or res['illegeal'] != 1:
    return False
  #if res['forward'] != 4 or res['backward'] != 0:
  #  return False
  print res
  return True
  
  