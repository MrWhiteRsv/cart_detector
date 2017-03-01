"""  Count forward and backward revolutios based on signal levels. 

It also retruns feedback regarding the synchronization behavior of both counters.
""" 

from enum import Enum
from signal_level import SignalLevel
from signal_level import SignalLevel

class RevolutionCounter():
  
  def __init__(self):
    LOW = SignalLevel.LOW
    HIGH = SignalLevel.HIGH

    self.forward_revolutions_counter = 0
    self.backward_revolutions_counter = 0
    self.illegeal_transition = 0

    self.direction = Direction.UNKNOWN
    self.sig_0_level = SignalLevel.UNKNOWN
    self.sig_1_level = SignalLevel.UNKNOWN
    
    self.consecutive_legal_shifts = 0
    
    self.state = None
    self.transition_table = {}

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
    return self.temp_add_reading(sig_0_level, sig_1_level)
    
    completed_forward_revolution = False
    completed_backward_revolution = False
    if self.sig_0_level == SignalLevel.UNKNOWN or self.sig_1_level == SignalLevel.UNKNOWN:
      self.sig_0_level = sig_0_level
      self.sig_1_level = sig_1_level
      self.state = (sig_0_level, sig_1_level)
    else:  # passed init.
      new_state = (sig_0_level, sig_1_level)
      if (new_state != self.state):
        print ('new_state: ', new_state)
        if not (self.state, new_state) in self.transition_table:
          self.illegeal_transition = self.illegeal_transition + 1
          self.consecutive_legal_shifts = 0
        else:
          new_direction = self.transition_table[(self.state, new_state)]
          if (self.direction == new_direction):
            self.consecutive_legal_shifts = self.consecutive_legal_shifts + 1
            if self.consecutive_legal_shifts % 4 == 0:
              if self.transition_table[(self.state, new_state)] == Direction.FORWARD:
                completed_forward_revolution = True
                self.forward_revolutions_counter = self.forward_revolutions_counter + 1
              else:
                completed_backward_revolution = True
                self.backward_revolutions_counter = self.backward_revolutions_counter + 1
          else:
            self.consecutive_legal_shifts = 1 # Just shifted to the reverse direction.
            self.direction = new_direction
      self.state = new_state 
    return {
      'forward_revolutions_counter' : self.forward_revolutions_counter,
      'backward_revolutions_counter' : self.backward_revolutions_counter,
      'illegeal_transition' : self.illegeal_transition,
      'completed_forward_revolution' : completed_forward_revolution,
      'completed_backward_revolution' : completed_backward_revolution,
    }
    
  def temp_add_reading(self, sig_0_level, sig_1_level):
    completed_forward_revolution = False
    completed_backward_revolution = False
    if self.sig_0_level == SignalLevel.UNKNOWN:
      self.sig_0_level = sig_0_level
    if not self.sig_0_level == sig_0_level:
      completed_forward_revolution = True
      self.sig_0_level = sig_0_level
      self.forward_revolutions_counter = self.forward_revolutions_counter + 1
    return {
      'forward_revolutions_counter' : self.forward_revolutions_counter,
      'backward_revolutions_counter' : self.backward_revolutions_counter,
      'illegeal_transition' : self.illegeal_transition,
      'completed_forward_revolution' : completed_forward_revolution,
      'completed_backward_revolution' : completed_backward_revolution,
    }
          
""" internals """
class Direction(Enum):
  UNKNOWN = 1
  FORWARD = 2
  BACKWORD = 3