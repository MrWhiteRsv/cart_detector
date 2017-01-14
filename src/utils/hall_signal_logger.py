import os

class HallSignalLogger():
  """ state variables """
  
  raw_signal_file = None
  activity_file = None
  filtered_signal_file = None
  turn_events_file = None  # turn events of filtered signal
  
  """ API """

  def open(self, run_name):
    dir = os.path.dirname(__file__)
    assert run_name and len(run_name) > 0, 'missing run name'
    self.raw_signal_file = open(run_name + '_raw_signal_file.txt', 'w')
    self.activity_file = open(run_name + '_activity_file.txt', 'w')
    self.filtered_signal_file = open(run_name + '_filtered_signal_file.txt', 'w')
    self.turn_events_file = open(run_name + '_turn_events_file.txt', 'w')

  def close(self):
    self.raw_signal_file.close()
    self.activity_file.close()
    self.filtered_signal_file.close()
    self.turn_events_file.close()
    self.raw_signal_file = None
    self.activity_file = None
    self.filtered_signal_file = None
    self.turn_events_file = None

  def log_raw_signal_lst(self, lst):
    for reading_counter in range(len(lst)):
      self.log_raw_signal(reading_counter, lst[reading_counter])
    
  def log_activity_lst(self, lst):
    for reading_counter in range(len(lst)):
      self.log_activity(reading_counter, lst[reading_counter])
    
  def log_filtered_signal(self, reading_counter, val):
    self.filtered_signal_file.write(str(reading_counter) + ', ' + str(val) + '\n')

  def log_turn_event(self, reading_counter, val):
    self.turn_events_file.write(str(reading_counter) + ', ' + str(val) + '\n')
    
  """ Implementation """
  
  def log_raw_signal(self, reading_counter, val):
    self.raw_signal_file.write(str(reading_counter) + ', ' + str(val) + '\n')
    
  def log_activity(self, reading_counter, val):
    self.activity_file.write(str(reading_counter) + ', ' + str(val) + '\n')
  