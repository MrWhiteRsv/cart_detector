""" This class is responsible to evaluate the accuracy of the turn top and bottom
thresholds. """

class TurnThresholdEvaluator():

  @staticmethod 
  def some_function():
    print('TurnThresholdOptimzer')
     
  @staticmethod 
  def evaluate_thrsholds(signal_lst, bottom_threshold, top_threshold):
    """ Evaluates the impact of the given thresholds on a signal_lst.
    
    Args:
        signal_lst: Samples of an *active* cart.
        bottom_threshold: threshold for detecting a half turn event.
        top_threshold: dito.
    
    Returns:
        A dict evaluating the impact of these thresholds. A complete_shifts would be
        a switch from a high state to a low state and vice versa. A partial_shifts would
        be a switch from high to not high and back to high (same regarding low):
        {'complete_shifts' :  152,
         'partial_shifts' : 11}
    """
    print 'evaluate_thrsholds'