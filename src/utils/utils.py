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
  
def get_longest_central_run_indices(lst, val):
  """ same as get_longest_run_indices yet prefix val run and suffix val runs are
      ignored.
    Example: lst = [0, 0, 0, 1, 0, 0, 1, 1, 0 ,0], val = 0 should yield
        {'start_index' : 4,  'end_index' : 5}
  """
  first_different = first_different_index(lst, val)
  last_different = last_different_index(lst,val)
  if (not first_different or not last_different):
    return None
  center_lst = lst[first_different:last_different + 1]
  res = get_longest_run_indices(center_lst, val)
  if res['start_index'] == None or res['end_index'] == None:
    return None
  res['start_index'] = res['start_index'] + first_different
  res['end_index'] = res['end_index'] + first_different
  return res
  
  
def first_different_index(lst, val):
  """ Finds the index of the first item in lst that has value different then val.
  Args:
    lst: list of values.
    val: the checked value.
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
    val: the checked value.
  Returns:
    index of item. None if no such item exists.
  """
  for index, number in enumerate(reversed(lst)):
    if number != val: # or 'if number:'
      return len(lst) - index - 1
  return None
  
  
def get_prefix_index(lst, fraction):
  """ Finds index of item pointing to the max prefix with sum less than or equel
      fraction.
  Args:
    lst: list of numeric values.
    fraction: a fraction of the total sum of values in lst.  
  Returns:
    index of item pointing to the prefix with a sum less than fraction items.
  Example: get_prefix_index([1, 2, 2, 5, 15], fraction = 0.25) == 2
  """
  prefix_max_sum = fraction * reduce(lambda x, y: (x + y), lst)
  prefix_sum = 0
  for index in range(len(lst)):
    prefix_sum = prefix_sum + lst[index]
    if prefix_sum > prefix_max_sum:
      break;
  if index == 0 or index == len(lst):
    return None
  return index - 1

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

