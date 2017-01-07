class Histogram():
  
  bins = None
  sample_counts = None

  def __init__(self, num_bins, min_val, max_val):
    bin_width = (max_val - min_val) / (1. * num_bins)
    self.bins = map(lambda x: x * bin_width, range(0, num_bins + 1, 1))
    bin_count = len(self.bins) - 1
    self.sample_counts = [0] * bin_count

  def add_sample(self, val):
    bin_count = len(self.bins) - 1
    for i in range(bin_count):
      if (self.bins[i] <= val) and (val < self.bins[i + 1]):
        self.sample_counts[i] += 1

  def get_bins(self):
    return list(self.bins)

  def get_sample_counts(self):
    return list(self.sample_counts)
    
  def to_string(self):
    res = ''
    res = res + 'bins: ' + str(self.bins) + '\n'
    res = res + 'sample_counts: ' + str(self.sample_counts) + '\n'
    return res
  

   