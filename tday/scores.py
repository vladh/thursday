"""
Source format:
  * file source
    {'filepath': '../bach/etc'}
  * corpus source
    {'corpusFilepath': 'bach/etc'}
"""

from music21 import converter, corpus, interval, note

sourceRoot = '../scores/'

def getTestSources():
  return [
    {'filepath': sourceRoot + 'bwv563.xml'},
    {'corpusFilepath': 'bach/bwv127.5.mxl'},
    {'corpusFilepath': 'haydn/opus74no1/movement1.mxl'},
    {'corpusFilepath': 'monteverdi/madrigal.3.1.xml'},
    {'corpusFilepath': 'schoenberg/opus19/movement2.mxl'},
    {'corpusFilepath': 'trecento/Fava_Dicant_nunc_iudei.xml'},
    {'corpusFilepath': 'verdi/laDonnaEMobile.mxl'}
  ]

def getComposerSources(composer, limit=None):
  sources = [{'corpusFilepath': path} for path in corpus.getComposer(composer)]
  if limit != None:
    if len(sources) < limit:
      return sources
    else:
      return sources[:limit]

def loadScore(source):
  """
  @param sourceId {str}
  @returns {music21.score}
  """
  if 'filepath' in source:
    print 'Loading score ' + source['filepath']
    return converter.parse(source['filepath'])
  elif 'corpusFilepath' in source:
    print 'Loading score ' + source['corpusFilepath']
    return corpus.parse(source['corpusFilepath'])

def loadScores(sources):
  return [loadScore(source) for source in sources]
