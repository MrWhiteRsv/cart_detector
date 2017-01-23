""" 
This module is responsible for the to count forward and backward revolutios based on signal
levels. It also retruns feedback regarding the synchronization behavior of both counters.
""" 

from enum import Enum
from signal_level import SignalLevel
from signal_level import SignalLevel

class RevolutionCounter():
  
  def __init__(self):
    LOW = SignalLevel.LOW
    HIGH = SignalLevel.HIGH
    self.forward_revolutions = 0
    self.backward_revolutions = 0
    self.illegeal_transition = 0
    self.direction = Direction.UNKNOWN
    self.sig_0_level = SignalLevel.UNKNOWN
    self.sig_1_level = SignalLevel.UNKNOWN
    self.state = None
    self.transition_table = {}
    if False:
      self.transition_table[((LOW, LOW), (HIGH, LOW))] = Direction.FORWARD
      self.transition_table[((HIGH, LOW), (HIGH, HIGH))] = Direction.FORWARD
      self.transition_table[((HIGH, HIGH), (LOW, HIGH))] = Direction.FORWARD
      self.transition_table[((LOW, HIGH), (LOW, LOW))] = Direction.FORWARD
    else:
      self.transition_table[((LOW, LOW), (LOW, HIGH))] = Direction.FORWARD
      self.transition_table[((LOW, HIGH), (HIGH, HIGH))] = Direction.FORWARD
      self.transition_table[((HIGH, HIGH), (HIGH, LOW))] = Direction.FORWARD
      self.transition_table[((HIGH, LOW), (LOW, LOW))] = Direction.FORWARD
    
      self.transition_table[((LOW, HIGH), (LOW, LOW))] = Direction.BACKWORD
      self.transition_table[((HIGH, HIGH), (LOW, HIGH))] = Direction.BACKWORD
      self.transition_table[((HIGH, LOW), (HIGH, HIGH))] = Direction.BACKWORD
      self.transition_table[((LOW, LOW), (HIGH, LOW))] = Direction.BACKWORD
  
  def add_reading(self, sig_0_level, sig_1_level):
    """ notifies the class of a new reading, and returns the forward and backward count.
  
    The system can be in either of 4 states:
      (SIG0_L, SIG1_L), (SIG0_L, SIG1_H), (SIG0_H, SIG1_H), (SIG0_H, SIG1_L) 
      
    A forward movement will be of the following:
      (SIG0_L, SIG1_L) -> (SIG0_L, SIG1_H) -> (SIG0_H, SIG1_H) -> (SIG0_H, SIG1_L) ->
    A backward movement will be of the following:
      (SIG0_H, SIG1_L) -> (SIG0_H, SIG1_H) -> (SIG0_L, SIG1_H) -> (SIG0_L, SIG1_L) ->
    
    Only 8 (out of 12) transitions are legal, which will raise the appropriate counter.
    In case of a legal transition either revolutions counter will be increased.
    Otherwise the ilegael transition counter will be increased.
    
    Args:
      sig_0_level: signal_0_level as in signal_level.SignalLevel.
      sig_1_level: dito.
      
    Returns:
      all 3 counters.
    """
    if self.sig_0_level == SignalLevel.UNKNOWN or self.sig_1_level == SignalLevel.UNKNOWN:
      self.sig_0_level = sig_0_level
      self.sig_1_level = sig_1_level
      self.state = (sig_0_level, sig_1_level)
    else:  # passed init.
      new_state = (sig_0_level, sig_1_level)
      if (new_state != self.state):
        if not (self.state, new_state) in self.transition_table:
          self.illegeal_transition = self.illegeal_transition + 1
        else:
          if self.transition_table[(self.state, new_state)] == Direction.FORWARD:
            self.forward_revolutions = self.forward_revolutions + 1
          else:
            self.backward_revolutions = self.backward_revolutions + 1
      self.state = new_state 
    return {
      'forward' : self.forward_revolutions,
      'backward' : self.backward_revolutions,
      'illegeal' : self.illegeal_transition
    }

""" internals """
class Direction(Enum):
  UNKNOWN = 1
  FORWARD = 2
  BACKWORD = 3