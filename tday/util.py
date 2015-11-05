import numpy as np
import operator

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
  if not len(a) == len(b):
    raise ValueError('a and b must have the same length')
  p = np.random.permutation(len(a))
  return a[p], b[p]

def crossfold(data, nrSlices, index):
  if not len(data) % nrSlices == 0:
    raise ValueError('nrSlices must be a divisor of the data length')
  foldSize = len(data) / nrSlices
  folds = [data[i * foldSize:(i + 1) * foldSize] for i in xrange(nrSlices)]
  otherFolds = np.concatenate(folds[:index] + folds[index + 1:])
  selectedFold = folds[index]
  return [otherFolds, selectedFold]

def sortDict(d):
  """
  Returns a sorted representation of a dictionary.

  @param d {Dict}
  @return {Set}
  """
  return sorted(d.items(), key=operator.itemgetter(1), reverse=True)

def setToString(s):
  """
  Gives a string representation of the given set.

  @param s {Set}
  @return {str}
  """
  strings = [str(interval) + ' ' + ('{:.2f}'.format(count)) for interval, count in s]
  string = ', '.join(strings)
  return string
