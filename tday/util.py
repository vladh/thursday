import tday.music

import music21
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

def music21ScoreToPlainScore(score):
  plainScore = {
    'measures': []
  }

  for part in score.parts:
    for measure in part.getElementsByClass('Measure'):
      key = tday.music.keyFromKeySignature(measure.flat.getKeySignatures()[0])
      sig = measure.getTimeSignatures()[0]
      plainMeasure = {
        'key': key.tonicPitchNameWithCase,
        'timeSignature': sig.ratioString,
        'notes': []
      }
      for note in measure.flat.notes:
        offset = score.offset + part.offset + measure.offset + note.offset
        interval = music21.interval.Interval(note.pitch, key.getTonic())
        semitones = interval.cents / 100
        plainNote = {
          'start': offset,
          'duration': note.duration.quarterLength,
          'keyDegree': interval.intervalClass,
          'keySemitones': semitones
        }
        plainMeasure['notes'].append(plainNote)
      plainScore['measures'].append(plainMeasure)

  return plainScore

def unisonShuffle(a, b):
  p = np.random.permutation(len(a))
  return a[p], b[p]
