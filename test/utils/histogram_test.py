from src.utils import histogram

class HistogramTest():

  def test(self):
    ovreall_res = True;
    
    res = self.test_getters()
    ovreall_res = ovreall_res and res
    print ('HistogramTest.test_getters: ' , 'pass' if res else 'fail')
    
    res = self.test_add_sample()
    ovreall_res = ovreall_res and res
    print ('HistogramTest.test_add_sample: ' , 'pass' if res else 'fail')
    
    return ovreall_res

  def test_add_sample(self):
    hist = histogram.Histogram(num_bins = 20, min_val = 0, max_val = 5)
    if (hist.get_sample_counts()[0] != 0):
      return False
    hist.add_sample(0.1)
    if (hist.get_sample_counts()[0] != 1):
      return False
    hist.add_sample(0.2)
    if (hist.get_sample_counts()[0] != 2):
      return False
    hist.add_sample(0.3)
    hist.add_sample(0.3)
    if (hist.get_sample_counts()[1] != 2):
      return False
    hist.add_sample(0.25)
    if (hist.get_sample_counts()[1] != 3):
      return False
    return True   
    
  def test_getters(self):
    hist = histogram.Histogram(num_bins = 20, min_val = 0, max_val = 5)
    hist.add_sample(0.1)
    if (len(hist.get_bins()) != 21):
      return False
    hist.get_bins().append(12)
    if (len(hist.get_bins()) != 21):
      return False
    if (len(hist.get_sample_counts()) != 20):
      return False
    hist.get_sample_counts().append(12)
    if (len(hist.get_sample_counts()) != 20):
      return False
    return True
    

    