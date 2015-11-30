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

import tday.mxlScores
import tday.config

import music21
import yaml
import cPickle as pickle
from collections import Counter
from os import mkdir, listdir
from os.path import basename, dirname, exists, isfile, splitext
from os.path import isfile, join

if tday.config.fileFormat == 'pickle':
  fileExt = '.pickle'
elif tday.config.fileFormat == 'yaml':
  fileExt = '.yml'

"""
Gets a measure's key from the key signature, or by analysis if that doesn't
work. If we can't get it by analysis either, default to C major, since there
is probably no key anyway (e.g. no notes).

@param measure {music21.stream.Measure}
@return {music21.key.Key}
"""
def getKeyFromMeasure(measure):
  keySignatures = measure.flat.getKeySignatures()
  if len(keySignatures) > 0:
    key = tday.mxlScores.keyFromKeySignature(keySignatures[0])
  else:
    print "" + \
      "[plainScores#getKeyFromMeasure] Could not get key for measure, using " + \
      "analysis to determine it"
    print measure.show('text')
    try:
      key = measure.analyze('key')
    except Exception:
      print "" + \
        "[plainScores#getKeyFromMeasure] Could not get key by analysis. " + \
        "Defaulting to C major. There probably *is* no key at all (no " + \
        "notes?)."
      key = music21.key.Key('C')
  return key

def fromMxl(score, name='Unknown'):
  if isinstance(score, music21.stream.Opus):
    print '[plainScores#fromMxl] WARNING: Merging Opus'
    score = score.mergeScores()

  plainScore = {
    'measures': [],
    'name': name
  }

  for part in score.parts:
    for measure in part.getElementsByClass('Measure'):
      timeSig = measure.getTimeSignatures()[0]
      plainMeasure = {
        'timeSignature': timeSig.ratioString,
        'notes': []
      }
      key = getKeyFromMeasure(measure)
      plainMeasure['key'] = key.tonicPitchNameWithCase
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

def getPaths(root, composer, limit=None):
  directory = join(root, composer)
  paths = [
    join(directory, path)
    for path in listdir(directory)
    if isfile(join(directory, path)) and splitext(join(directory, path))[1] == fileExt
  ]
  if limit != None and len(paths) > limit:
    paths = paths[:limit]
  return paths

def getComposerPaths(composer, limit=None):
  return getPaths(tday.config.paths['plainComposerRoot'], composer, limit)

def getCorpusComposerPaths(composer, limit=None):
  return getPaths(tday.config.paths['plainCorpusRoot'], composer, limit)

def loadScores(paths):
  scores = [loadScore(path) for path in paths]
  return scores

def writeScore(plainScore, path):
  path, ext = splitext(path)
  path += fileExt
  print '[plainScores#writeScore] ' + path

  dirName = dirname(path)
  if not exists(dirName): mkdir(dirName)

  with open(path, 'w') as fp:
    if tday.config.fileFormat == 'pickle':
      fileContent = pickle.dumps(plainScore)
    elif tday.config.fileFormat == 'yaml':
      fileContent = yaml.dump(stream)
    fp.write(fileContent)

def writeCorpusScore(plainScore, composer, name):
  path = join(tday.config.paths['plainCorpusRoot'], composer, name)
  writeScore(plainScore, path)

def writeComposerScore(plainScore, composer, name):
  path = join(tday.config.paths['plainComposerRoot'], composer, name)
  writeScore(plainScore, path)

def getGenericFrequencies(score, prop):
  """
  Calculates the frequency of a certain property in the given score's notes.

  @param intervals {plainScore}
  @return {Dict}
  """
  nrSamples = 0.0
  intervals = []
  for measure in score['measures']:
    for note in measure['notes']:
      intervals.append(note[prop])
      nrSamples += 1
  freq = Counter(intervals)
  freq = {k: v / nrSamples for k, v in freq.items()}
  return freq

def getDurationFrequencies(score):
  """
  Calculates the frequency of duration in the given score's notes.

  @param intervals {plainScore}
  @return {Dict}
  """
  return getGenericFrequencies(score, 'duration')

def getKeyIntervalFrequencies(score):
  """
  Calculates the frequency of keyInterval in the given score's notes.

  @param intervals {plainScore}
  @return {Dict}
  """
  return getGenericFrequencies(score, 'keyInterval')

def convertMxlCorpus(paths):
  for path in paths:
    score = tday.mxlScores.loadCorpusScores([path])[0]
    composer = basename(dirname(path))
    name = basename(path)
    plainScore = fromMxl(score, composer + '/' + name)
    writeCorpusScore(plainScore, composer, name)

def convertMxlComposer(paths):
  for path in paths:
    print '[plainScores#convertMxlComposer] Converting ' + path
    scores = tday.mxlScores.loadScores([path])
    if len(scores) == 0:
      print '[plainScores#convertMxlComposer] Could not load score ' + path
      continue
    score = scores[0]
    composer = basename(dirname(path))
    name = basename(path)
    plainScore = fromMxl(score, composer + '/' + name)
    writeComposerScore(plainScore, composer, name)
