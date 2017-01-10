
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

