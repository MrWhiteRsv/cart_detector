import json
import os
import traceback

def get_longest_run_indices(lst, val):
  min_run_length = 0
  current_run_length = 0
  max_start_index = None
  max_end_index = None
  max_run_length = 0
    
  before_first_instance = True
  for i in range(0, len(lst)):
    if before_first_instance:
      if lst[i] == val:
        max_start_index = i
        max_end_index = i
        before_first_instance = False
        current_run_length = 1
      continue
    curr_equal_val = (lst[i] == val)
    prev_equal_val = (lst[i - 1] == val)
    current_run_length = current_run_length + 1 if curr_equal_val else 0
    if (current_run_length > max_run_length):
      max_run_length = current_run_length
      max_end_index = i
      max_start_index = i - current_run_length + 1
  return {'start_index' : max_start_index,  'end_index' : max_end_index}
  
def first_different_index(lst, val):
  """ Finds the index of the first item in lst that has value different then val.
    
  Args:
    lst: list of values.
    val: the checked value
  
  Returns:
    index of item. None if no such item exists.
  """
  for index, number in enumerate(lst):
    if number != val:  
      return index
  return None
    
def last_different_index(lst, val):
  """ Finds the index of the last item in lst that has value different then val.
    
  Args:
    lst: list of values.
    val: the checked value
  
  Returns:
    index of item. None if no such item exists.
  """
  for index, number in enumerate(reversed(lst)):
    if number != val: # or 'if number:'
      return len(lst) - index - 1
  return None

def get_signal_from_file(file_name, val_key):
  signal = []
  try:
    current_dir = os.path.dirname(__file__)
    full_input_file_name = os.path.join(current_dir, '../../test/runs/' + file_name)
    input_file = open(full_input_file_name, 'r')
    for line in input_file:
      try: 
        parsed = json.loads(line)
      except Exception as inst:
        continue
      if (parsed['topic'] == 'cart/cartId/hall_reading'):
        signal.append(parsed[val_key])
    input_file.close()
    return signal
  except Exception as inst:
    print (inst)
    traceback.print_exc()
    return None

