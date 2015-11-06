"""
Plain score format:
{
  'name': 'bach/bwv381',
  'measures': [
    {
      'key': 'C major',
      'timeSignature': '3/4'
      'notes': [
        {
          'start': 0.5,
          'duration': 2,
          'keyInterval': 'P5',
          'keyDegree': 5,
          'keySemitones': 7
        },
        {
          ...
        },
        ...
      ]
    },
    {
      ...
    },
    ...
  ]
}
"""

import tday.music
import tday.config

import music21
import yaml
import cPickle as pickle
from collections import Counter
from os import mkdir, listdir
from os.path import dirname, exists, isfile, splitext
from os.path import isfile, join

if tday.config.fileFormat == 'pickle':
  fileExt = '.pickle'
elif tday.config.fileFormat == 'yaml':
  fileExt = '.yml'

def fromMxl(score, name='Unknown'):
  plainScore = {
    'measures': [],
    'name': name
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
          plainNote = {
            'start': offset,
            'duration': note.duration.quarterLength,
            'keyInterval': interval.name,
            'keyDegree': interval.intervalClass,
            'keySemitones': interval.cents / 100
          }
          plainMeasure['notes'].append(plainNote)
      plainScore['measures'].append(plainMeasure)

  return plainScore

def loadScore(path):
  with open(path, 'r') as stream:
    if tday.config.fileFormat == 'pickle':
      return pickle.load(stream)
    elif tday.config.fileFormat == 'yaml':
      return yaml.load(stream)

def getCorpusComposerPaths(composer, limit=None):
  directory = join(tday.config.paths['plainCorpusRoot'], composer)
  paths = [
    join(directory, path)
    for path in listdir(directory)
    if isfile(join(directory, path)) and splitext(join(directory, path))[1] == fileExt
  ]
  if limit != None and len(paths) > limit:
    paths = paths[:limit]
  return paths

def loadScores(paths):
  scores = [loadScore(path) for path in paths]
  return scores

def writeCorpusScore(plainScore, composer, name):
  path = join(tday.config.paths['plainCorpusRoot'], composer, name)
  path, ext = splitext(path)
  path += fileExt
  print '[plainScores#writeCorpusScore] ' + path

  dirName = dirname(path)
  if not exists(dirName): mkdir(dirName)

  with open(path, 'w') as fp:
    if tday.config.fileFormat == 'pickle':
      fileContent = pickle.dumps(plainScore)
    elif tday.config.fileFormat == 'yaml':
      fileContent = yaml.dump(stream)
    fp.write(fileContent)

def getKeyIntervalFrequencies(score):
  """
  Calculates the frequency of keyInterval in the given score's notes.

  @param intervals {plainScore}
  @return {Dict}
  """
  nrIntervals = 0.0
  intervals = []
  for measure in score['measures']:
    for note in measure['notes']:
      intervals.append(note['keyInterval'])
      nrIntervals += 1
  freq = Counter(intervals)
  freq = {k: v / nrIntervals for k, v in freq.items()}
  return freq
