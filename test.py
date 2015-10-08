from music21 import converter, corpus, interval, note
from collections import defaultdict, Counter
import operator

sourceRoot = '../scores/'

scoreSources = {
  'bach/bwv563': {'type': 'file', 'path': 'bwv563.xml'},
  'bach/bwv127.5': {'type': 'corpus', 'path': 'bach/bwv127.5.mxl'},
  # 'beethoven/opus132': {'type': 'corpus', 'path': 'beethoven/opus132.mxl'},
  # 'essenFolksong/altdeu10': {'type': 'corpus', 'path': 'essenFolksong/altdeu10.abc'},
  'haydn/opus74no1/movement1': {'type': 'corpus', 'path': 'haydn/opus74no1/movement1.mxl'},
  'monteverdi/madrigal.3.1': {'type': 'corpus', 'path': 'monteverdi/madrigal.3.1.xml'},
  'schoenberg/opus19/movement2': {'type': 'corpus', 'path': 'schoenberg/opus19/movement2.mxl'},
  'trecento/Fava_Dicant_nunc_iudei': {'type': 'corpus', 'path': 'trecento/Fava_Dicant_nunc_iudei.xml'},
  'verdi/laDonnaEMobile': {'type': 'corpus', 'path': 'verdi/laDonnaEMobile.mxl'}
}

def loadScore(sourceId):
  """
  When given a source ID, looks it up in scoreSources and loads the
  corresponding score, be it from a file or the corpus.

  @param sourceId {str}
  @returns {music21.score}
  """
  source = scoreSources[sourceId]
  if source['type'] == 'file':
    return converter.parse(sourceRoot + source['path'])
  elif source['type'] == 'corpus':
    return corpus.parse(source['path'])

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

def processSource(sourceId):
  """
  Does various things with a score.
  """
  score = loadScore(sourceId)
  key = score.analyze('key')
  # NOTE: This (wrongly) always seems to get "4/4".
  sig = score.getTimeSignatures()[0]
  notes = score.flat.pitches
  intervals = makeNotesIntoTonicIntervals(notes, key.getTonic())
  freq = sortIntervalFrequencies(getIntervalFrequencies(intervals))

  print '# Score: ' + str(sourceId)
  print '- Key of'
  print '  ' + str(key)
  print
  print '- Time signature'
  print '  ' + str(sig.ratioString)
  print
  print '- Interval frequencies'
  print '  ' + intervalFrequenciesToString(freq)
  print
  print

def main():
  map(processSource, scoreSources.keys())

if __name__ == '__main__':
  main()