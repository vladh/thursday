import numpy as np

def printTable(heading, info):
  """
  Prints a heading and some custom extra pairs of information.

  @param heading {str}
  @param info {List[List[str, str]]}
  """
  print '------------------------------'
  print heading
  for item in info:
    print
    print '- ' + str(item[0])
    print '  ' + str(item[1])
  print '------------------------------'
  print
  print

def unisonShuffle(a, b):
  p = np.random.permutation(len(a))
  return a[p], b[p]
