import src.utils.utils
    
def test():
  ovreall_res = True;
  
  res = get_longest_run_indices_test()
  ovreall_res = ovreall_res and res
  print ('src.utils.utils.get_longest_run_indices_test: ' , 'pass' if res else 'fail') 
  return ovreall_res
  
def get_longest_run_indices_test():
  # Simple run.
  lst = [1, 0, 0, 1, 1]
  indices = src.utils.utils.get_longest_run_indices(lst = lst, val = 0)
  if indices['start_index'] != 1 or indices['end_index'] != 2:
    return False

  # Last run in list, val other then zero.
  lst = [1, 0, 1, 1]
  indices = src.utils.utils.get_longest_run_indices(lst = lst, val = 1)
  if indices['start_index'] != 2 or indices['end_index'] != 3:
    return False
    
  # First run in list.
  lst = [0, 0, 1, 0, 1, 1]
  indices = src.utils.utils.get_longest_run_indices(lst = lst, val = 0)
  if indices['start_index'] != 0 or indices['end_index'] != 1:
    return False
    
  # Three runs.
  lst = [0, 0, 1, 0, 1, 0, 0, 0, 1]
  indices = src.utils.utils.get_longest_run_indices(lst = lst, val = 0)
  if indices['start_index'] != 5 or indices['end_index'] != 7:
    return False

  # Value not in list.
  lst = [0, 0, 1, 0, 1, 0, 0, 0, 1]
  indices = src.utils.utils.get_longest_run_indices(lst = lst, val = 2)
  if indices['start_index'] != None or indices['end_index'] != None:
    return False

  # Empty list.
  lst = []
  print (lst)
  indices = src.utils.utils.get_longest_run_indices(lst = lst, val = 0)
  print (indices)
  if indices['start_index'] != None or indices['end_index'] != None:
    return False
    
  return True
