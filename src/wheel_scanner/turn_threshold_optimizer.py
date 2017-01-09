""" This class is responsible to optimize the turn top and bottom thresholds. """

class TurnThresholdOptimzer():

  @staticmethod 
  def some_function():
    print('TurnThresholdOptimzer')

  @staticmethod 
  def optimize_thrsholds_with_revolutions(training_signals, revolutions):
    """ Evaluates the impact of the given thresholds on a signal_lst.
    
    Args:
        training_signals: Samples of forward moving cart which has both an active and an
            inactive phase.
        revolutions: The number of revolutions the cart has done during training.
    
    Returns:
        A dict of the optimized thresholds, such that the most accurate rotation count
        will be detected. Example
        {'bottom_threshold' :  3.2,
         'top_threshold' : 1.8}
    """
    print ('optimize_thrsholds_with_revolutions')
    return {}
    
  @staticmethod 
  def optimize_thrsholds(training_signals):
    """ Evaluates the impact of the given thresholds on a signal_lst.
    
    Args:
        training_signals: Samples of forward moving cart which has both an active and an
            inactive phase.

    
    Returns:
        A dict of the optimized thresholds, such that the most accurate rotation count
        will be detected. Example
        {'bottom_threshold' :  3.2,
         'top_threshold' : 1.8}
    """
    print ('optimize_thrsholds_with_revolutions')
    return {}