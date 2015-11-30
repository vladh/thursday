import random
import tday.plainScores

base40IntervalTable = {
  0: 'P1', 1: 'A1', 4: 'd2', 5: 'm2', 6: 'M2', 7: 'A2', 10: 'd3', 11: 'm3', \
  12: 'M3', 13: 'A3', 16: 'd4', 17: 'P4', 18: 'A4', 22: 'd5', 23: 'P5', \
  24: 'A5', 27: 'd6', 28: 'm6', 29: 'M6', 30: 'A6', 33: 'd7', 34: 'm7', \
  35: 'M7', 36: 'A7', 39: 'd8', 40: 'P8'
}

durationTable = [
  0.125, 0.25, 0.5, 1, 2, 4
]

def makeRandomFeature(score):
  """
  @param score {plainScore}
  @returns {List[numpy.array, music21.key, Dict]}
  """
  sample = [
    random.randint(1,10000),
    random.randint(1,10000),
    random.randint(1,10000),
    random.randint(1,10000),
    random.randint(1,10000)
  ]
  return sample

def makeDurationFrequencyFeature(score):
  """
  Extracts an interval frequencies feature.
  Returns some extra information too.

  @param score {plainScore}
  @returns {List[numpy.array, music21.key, Dict]}
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
  Returns some extra information too.

  @param score {plainScore}
  @returns {List[numpy.array, music21.key, Dict]}
  """
  freq = tday.plainScores.getKeyIntervalFrequencies(score)
  sample = [
    freq.get(intervalName, 0.0)
    for idx, intervalName in base40IntervalTable.iteritems()
  ]
  return sample
