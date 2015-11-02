import music21
from os import listdir
from os.path import isfile, join

paths = {
  'mxlComposerRoot': '../data/mxl/composers/',
  'mxlVariousRoot': '../data/mxl/various/',
  'plainCorpusRoot': '../data/plain/corpus/'
}

def getMxlComposerPaths(composer):
  directory = paths['mxlComposerRoot'] + composer + '/'
  paths = [join(directory, path) for path in listdir(directory)]
  paths = [path for path in paths if isfile(path)]
  return paths

def loadMxlPaths(paths):
  scores = [music21.converter.parse(path) for path in paths]
  return scores

def getCorpusComposerPaths(composer, limit=None):
  paths = music21.corpus.getComposer(composer)
  if limit != None and len(paths) > limit:
    paths = paths[:limit]
  return paths

def loadCorpusPaths(paths):
  scores = [music21.corpus.parse(path) for path in paths]
  return scores
