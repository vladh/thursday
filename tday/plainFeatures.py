import random
import tday.plainScores

base40IntervalTable = {
  0: 'P1', # X0
  1: 'A1', # X1
  4: 'd2', # X2
  5: 'm2', # X3
  6: 'M2', # X4
  7: 'A2', # X5
  10: 'd3', # X6
  11: 'm3', # X7
  12: 'M3', # X8
  13: 'A3', # X9
  16: 'd4', # X10
  17: 'P4', # X11
  18: 'A4', # X12
  22: 'd5', # X13
  23: 'P5', # X14
  24: 'A5', # X15
  27: 'd6', # X16
  28: 'm6', # X17
  29: 'M6', # X18
  30: 'A6', # X19
  33: 'd7', # X20
  34: 'm7', # X21
  35: 'M7', # X22
  36: 'A7', # X23
  39: 'd8', # X24
  40: 'P8' # X25
}

semitonesTable = range(0, 30) # X<i>: i semitones

durationTable = [
  # 0.125, 0.25, 0.5, 1, 2, 4
  0.0, 0.0625, 0.125, 0.1875, 0.25, 0.375, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0
  # 0.0
]

def makeRandomFeature(score):
  """
  @param score {plainScore}
  @returns {List[numpy.array, music21.key, Dict]}
  """
  sample = [
    1.0 - random.random(),
  ]
  return sample

def makeDurationFrequencyFeature(score):
  """
  Extracts an interval frequencies feature.

  @param score {plainScore}
  @returns {List[int]}
  """
  freq = tday.plainScores.getDurationFrequencies(score)
  sample = [
    freq.get(duration, 0.0)
    for duration in durationTable
  ]
  return sample

def makeIntervalFrequencyFeature(score):
  """
  Extracts a key interval frequencies feature.

  @param score {plainScore}
  @returns {List[int]}
  """
  freq = tday.plainScores.getKeyIntervalFrequencies(score)
  sample = [freq.get(semitones, 0.0) for semitones in semitonesTable]
  return sample
