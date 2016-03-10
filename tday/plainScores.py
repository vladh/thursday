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
from os.path import basename, dirname, exists, isfile, splitext, join

if tday.config.fileFormat == 'pickle':
  fileExt = '.pickle'
elif tday.config.fileFormat == 'yaml':
  fileExt = '.yml'

#
# ANALYSIS
#

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
  Calculates the frequency of keySemitones in the given score's notes.

  @param intervals {plainScore}
  @return {Dict}
  """
  return getGenericFrequencies(score, 'keySemitones')

#
# LOADING
#

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

def loadScores(paths):
  scores = [loadScore(path) for path in paths]
  return scores

def getComposerPaths(composer, limit=None):
  return getPaths(tday.config.paths['plainComposerRoot'], composer, limit)

def getCorpusComposerPaths(composer, limit=None):
  return getPaths(tday.config.paths['plainCorpusRoot'], composer, limit)

def getCorpusComposerData(composers, limit=None, splits=None):
  """
  Gets scores and labels for a given set of composers, from the corpus.

  @param composers {List}
  @param limit {int} Optional per-composer score limit
  @param splits {int} If given, will do split and merge on scores with this
    many splits
  @return {List<List, List>}
  """
  allScoreSets = []
  for composer in composers:
    composerScores = loadScores(getCorpusComposerPaths(composer, limit))
    if splits != None:
      mergedComposerScore = tday.plainScores.mergeScores(composerScores)
      composerScores = tday.plainScores.splitScore(mergedComposerScore, splits)
    allScoreSets.append([composer, composerScores])
  allScores = []
  allLabels = []
  for scoreSet in allScoreSets:
    allScores += scoreSet[1]
    allLabels += ([scoreSet[0]] * len(scoreSet[1]))
  return [allScores, allLabels]

def getComposerData(composers, limit=None, splits=None):
  """
  Gets scores and labels for a given set of composers, from our data.

  @param composers {List}
  @param limit {int} Optional per-composer score limit
  @param splits {int} If given, will do split and merge on scores with this
    many splits
  @return {List<List, List>}
  """
  allScoreSets = []
  for composer in composers:
    composerScores = loadScores(getComposerPaths(composer, limit))
    if splits != None:
      print '[plainScores#getComposerData] Splitting ' + \
        str(len(composerScores)) + ' scores into ' + str(splits)
      mergedComposerScore = tday.plainScores.mergeScores(composerScores)
      composerScores = tday.plainScores.splitScore(mergedComposerScore, splits)
    allScoreSets.append([composer, composerScores])
  allScores = []
  allLabels = []
  for scoreSet in allScoreSets:
    allScores += scoreSet[1]
    allLabels += ([scoreSet[0]] * len(scoreSet[1]))
  return [allScores, allLabels]

#
# WRITING
#

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

#
# MERGING / SPLITTING
#

def mergeScores(scores):
  """
  Takes multiple scores and concatenates their names and measures.

  @param scores {List<Dict>}
  @return {Dict}
  """
  emptyScore = {
    'name': '',
    'measures': []
  }

  def reduceScores(mergedScore, score):
    mergedScore['name'] += score['name'] + ' + '
    mergedScore['measures'] += score['measures']
    return mergedScore

  mergedScore = reduce(reduceScores, scores, emptyScore)
  if mergedScore['name'][-3:] == ' + ':
    mergedScore['name'] = mergedScore['name'][:-3]

  return mergedScore

def splitScore(mergedScore, n):
  """
  Splits a score's measures into n parts, returning n scores.

  @param mergedScore {Dict}
  @param n {int}
  @return {List<Dict>}
  """
  measureChunks = list(tday.util.chunk(mergedScore['measures'], n))
  scores = [None] * len(measureChunks)
  for idx, measures in enumerate(measureChunks):
    scores[idx] = {
      'name': mergedScore['name'] + ' (chunk ' + str(idx) + '/' + str(len(measureChunks) - 1) + ')',
      'measures': measures
    }
  return scores

#
# CONVERSION
#

def fromMxl(score, name='Unknown'):
  """
  Converts an MXL score to a plain score.

  @param score {music21.score.Score, music21.stream.Opus}
  @return {plainScore}
  """
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
      key = tday.mxlScores.getKeyFromMeasure(measure)
      plainMeasure['key'] = key.tonicPitchNameWithCase
      for generalNote in measure.flat.notes:
        if isinstance(generalNote, music21.chord.Chord):
          notes = music21.mxlScores.getNotesFromChord(generalNote)
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

def convertMxlCorpus(paths):
  """
  Converts a series of MXL corpus scores to plain scores.

  @param paths {List<str>}
  """
  for path in paths:
    score = tday.mxlScores.loadCorpusScores([path])[0]
    composer = basename(dirname(path))
    name = basename(path)
    plainScore = fromMxl(score, composer + '/' + name)
    writeCorpusScore(plainScore, composer, name)

def convertMxlComposer(paths):
  """
  Converts a series of MXL composer scores to plain scores.

  @param paths {List<str>}
  """
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
