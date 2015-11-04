import tday.music
import tday.paths

import music21
import yaml
from os import mkdir, listdir
from os.path import dirname, exists, isfile
from os.path import isfile, join

def fromMxl(score):
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
      for generalNote in measure.flat.notes:
        if isinstance(generalNote, music21.chord.Chord):
          notes = []
          for pitch in generalNote.pitches:
            note = music21.note.Note(pitch)
            note.offset = generalNote.offset
            note.duration = generalNote.duration
            notes.append(note)
        elif isinstance(generalNote, music21.note.Note):
          notes = [generalNote]
        for note in notes:
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

def loadScore(path):
  with open(path, 'r') as stream:
    return yaml.load(stream)

def getCorpusComposerPaths(composer):
  directory = tday.paths.paths['plainCorpusRoot'] + composer + '/'
  paths = [
    join(directory, path)
    for path in listdir(directory)
    if isfile(join(directory, path))
  ]
  return paths

def loadScores(paths):
  scores = [loadScore(path) for path in paths]
  return scores

def writeCorpusScore(plainScore, composer, name):
  plainPath = tday.paths.paths['plainCorpusRoot'] + composer + '/' + name
  plainDirName = dirname(plainPath)
  if not exists(plainDirName): mkdir(plainDirName)
  with open(plainPath, 'w') as fp:
    fp.write(str(plainScore))
