import tday.paths

import music21
import operator
from collections import defaultdict, Counter
from os import listdir
from os.path import isfile, join

def getComposerPaths(composer):
  """
  Returns the paths of scores for a certain composer from the composers
  directory.

  @param composer {str}
  @return {List<str>}
  """
  directory = tday.paths.paths['mxlComposerRoot'] + composer + '/'
  paths = [
    join(directory, path)
    for path in listdir(directory)
    if isfile(join(directory, path))
  ]
  return paths

def loadScores(paths):
  """
  Loads an array of paths and returns their associated scores.

  @param paths {List<str>}
  @return {List<music21.score.Score}>
  """
  scores = [music21.converter.parse(path) for path in paths]
  return scores

def getCorpusComposerPaths(composer, limit=None):
  """
  Returns the paths of scores for a certain composer from the music21 corpus.

  @param composer {str}
  @param limit {int} Maximum number of paths to get.
  """
  paths = music21.corpus.getComposer(composer)
  if limit != None and len(paths) > limit:
    paths = paths[:limit]
  return paths

def loadCorpusScores(paths):
  """
  Loads an array of corpus paths and returns their scores.

  @param paths {List<str>}
  @return {List<music21.score.Score>}
  """
  scores = [music21.corpus.parse(path) for path in paths]
  return scores

def keyFromKeySignature(keySignature):
  """
  Makes a music21.key.KeySignature into a music21.key.Key.

  @param keySignature {music21.key.KeySignature}
  @return {music21.key.Key}
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
  @return {List[music21.interval]}
  """
  # NOTE: Takes ~0.1s for 500 notes, ~1.5s for 5500 notes
  return [music21.interval.Interval(note, tonic) for note in notes]

def getIntervalFrequencies(intervals):
  """
  Calculates the frequency of intervals in the given list of intervals.

  @param intervals {List[music21.interval]}
  @return {Dict}
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
  @return {Set}
  """
  return sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

def intervalFrequenciesToString(freq):
  """
  Gives a string representation of the given sorted interval frequencies.

  @param freq {Set}
  @return {str}
  """
  strings = [interval + ' ' + ('{:.2f}'.format(count)) for interval, count in freq]
  string = ', '.join(strings)
  return string

