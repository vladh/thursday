import tday.config

import music21
from collections import Counter
from os import listdir
from os.path import isfile, join

def getComposerPaths(composer):
  """
  Returns the paths of scores for a certain composer from the composers
  directory.

  @param composer {str}
  @return {List<str>}
  """
  directory = join(tday.config.paths['mxlComposerRoot'], composer)
  paths = [
    join(directory, path)
    for path in listdir(directory)
    if isfile(join(directory, path))
  ]
  return paths

def loadScores(paths):
  """
  Loads an array of paths and returns their associated scores.
  May return fewer scores than paths if there are errors.

  @param paths {List<str>}
  @return {List<music21.score.Score}>
  """
  scores = []
  for path in paths:
    try:
      score = music21.converter.parse(path)
      scores.append(score)
    except Exception as e:
      print '[mxlScores#loadScores] Could not parse score ' + path
      print '[mxlScores#loadScores] ' + str(e)
      pass
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
  # HACK: This always outputs the major key. Figure out how to get major/minor.
  key = music21.key.Key(music21.key.sharpsToPitch(keySignature.sharps))
  return key
