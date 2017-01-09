
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
