""" This class is responsible to evaluate the accuracy of the turn top and bottom
thresholds. """

from enum import Enum

class SignalLevel(Enum):
  LOW = 1
  MIDDLE = 2
  HIGH = 3
  
class State(Enum):
  UNDEFINED = 1
  LOW = 2
  LOW_TO_MIDDLE = 3
  HIGH_TO_MIDDLE = 4
  HIGH = 5
  
def evaluate_thrsholds(signal_lst, bottom_threshold, top_threshold, min_level_samples):
  """ Evaluates the impact of the given thresholds on a signal_lst.
    
  Args:
    signal_lst: Samples of an *active* cart.
    bottom_threshold: threshold for detecting a half turn event.
    top_threshold: dito.
    
  Returns:
    A dict evaluating the impact of these thresholds.
    A shift is a switch from a high state to a low state and vice versa.
    A short shift is a shift where either of the states is l.t. min_level_samples.
      (Short shifts are counted twice.)
    Example: {'overall_shifts' :  152, 'short_shifts' : 12}
  """
  state = State.UNDEFINED
  res = {'overall_shifts' :  0, 'short_shifts' : 0}
  for val in signal_lst:
    signal_level = compute_signal_level(val, bottom_threshold, top_threshold)
    new_state = compute_state(state, signal_level)
    # print (val, 'signal_level:', signal_level, 'state:', state, 'new_state:', new_state)
    if (compute_did_shift(state, new_state)):
      res['overall_shifts'] = res['overall_shifts'] + 1
    state = new_state
  return res

""" logic """

def compute_did_shift(old_state, new_state):
  if ((old_state == State.LOW or old_state == State.LOW_TO_MIDDLE) and
      new_state == State.HIGH):
    return True
  if ((old_state == State.HIGH or old_state == State.HIGH_TO_MIDDLE) and
      new_state == State.LOW):
    return True
  return False

def compute_signal_level(val, bottom_threshold, top_threshold):
  if val < bottom_threshold:
    return SignalLevel.LOW
  if val > top_threshold:
    return SignalLevel.HIGH
  return SignalLevel.MIDDLE
  
def compute_state(old_state, signal_level):
  if (old_state == State.UNDEFINED):
    if (signal_level == SignalLevel.LOW):
      return State.LOW
    if (signal_level == SignalLevel.HIGH):
      return State.HIGH
    # signal_level == SignalLevel.MIDDLE
    return State.UNDEFINED
    
  if (old_state == State.LOW):
    if (signal_level == SignalLevel.LOW):
      return State.LOW
    if (signal_level == SignalLevel.HIGH):
      return State.HIGH
    # signal_level == SignalLevel.MIDDLE
    return State.LOW_TO_MIDDLE
    
  if (old_state == State.LOW_TO_MIDDLE):
    if (signal_level == SignalLevel.LOW):
      return State.LOW
    if (signal_level == SignalLevel.HIGH):
      return State.HIGH
    # signal_level == SignalLevel.MIDDLE
    return State.LOW_TO_MIDDLE
    
  if (old_state == State.HIGH_TO_MIDDLE):
    if (signal_level == SignalLevel.LOW):
      return State.LOW
    if (signal_level == SignalLevel.HIGH):
      return State.HIGH
    # signal_level == SignalLevel.MIDDLE
    return State.HIGH_TO_MIDDLE
    
  if (old_state == State.HIGH):
    if (signal_level == SignalLevel.LOW):
      return State.LOW
    if (signal_level == SignalLevel.HIGH):
      return State.HIGH
    # signal_level == SignalLevel.MIDDLE
    return State.HIGH_TO_MIDDLE