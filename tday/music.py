import music21
from collections import defaultdict, Counter
import operator

def keyFromKeySignature(keySignature):
  """
  Makes a music21.key.KeySignature into a music21.key.Key.

  @param keySignature {music21.key.KeySignature}
  @returns {music21.key.Key}
  """
  tonicAndMode = keySignature.getScale().name.split()
  key = music21.key.Key(tonicAndMode[0], tonicAndMode[1])
  return key

def makeNotesIntoTonicIntervals(notes, tonic):
  """
  Converts notes into their interval from the given tonic.
  If the notes are "C, D, E" and the tonic is "C", this will give "P1, M2, M3".

  @param notes {List[music21.note]}
  @param tonic {music21.note}
  @returns {List[music21.interval]}
  """
  # NOTE: Takes ~0.1s for 500 notes, ~1.5s for 5500 notes
  return [music21.interval.Interval(note, tonic) for note in notes]

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

