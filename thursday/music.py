from music21 import interval, note
from collections import defaultdict, Counter
import operator

def transposeScoreToKey(score, keyTonic):
  """
  Transposes a score to the key whose tonic is the supplied keyTonic.

  @param score {music21.score}
  @param keyTonic {music21.note}
  @returns {music21.score}
  """
  key = score.analyze('key')
  transposeInterval = interval.Interval(note.Note(key.getTonic()), keyTonic)
  tScore = score.transpose(transposeInterval)
  return tScore

def makeNotesIntoTonicIntervals(notes, tonic):
  """
  Converts notes into their interval from the given tonic.
  If the notes are "C, D, E" and the tonic is "C", this will give "P1, M2, M3".

  @param notes {List[music21.note]}
  @param tonic {music21.note}
  @returns {List[music21.interval]}
  """
  return map(lambda(note): interval.Interval(note, tonic), notes)

def getIntervalFrequencies(intervals):
  """
  Calculates the frequency of intervals in the given list of intervals.

  @param intervals {List[music21.interval]}
  @returns {Dict}
  """
  nrIntervals = float(len(intervals))
  intervalNames = map(lambda(d): d.name, intervals)
  freq = Counter(intervalNames)
  freq = {k: v / nrIntervals for k, v in freq.items()}
  return freq

def sortIntervalFrequencies(freq):
  """
  Returns a sorted representation of the interval frequency dictionary.

  @param freq {List[music21.interval]}
  @returns {Set}
  """
  return sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

def intervalFrequenciesToString(freq):
  """
  Gives a string representation of the given sorted interval frequencies.

  @param freq {Set}
  @returns {str}
  """
  strings = [interval + ' ' + ('{:.2f}'.format(count)) for interval, count in freq]
  string = ', '.join(strings)
  return string

