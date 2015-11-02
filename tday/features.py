import tday.music

import music21
import numpy as np
import time

def makeIntervalFrequencyFeature(score):
  """
  Extracts an interval frequencies feature.
  Returns some extra information too.

  @param score {music21.score}
  @returns {List[numpy.array, music21.key, Dict]}
  """
  print 'Making interval frequency feature for ' + str(getattr(score, 'corpusFilepath', score.filePath))
  intervalTable = music21.musedata.base40.base40IntervalTable.values()

  key = tday.music.keyFromKeySignature(score.flat.getKeySignatures()[0])

  intervals = tday.music.makeNotesIntoTonicIntervals(score.flat.pitches, key.getTonic())
  freq = tday.music.getIntervalFrequencies(intervals)

  sample = map(lambda(interval): freq.get(interval, 0), intervalTable)
  return [sample, key, freq]
