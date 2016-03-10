# -*- coding: utf-8 -*-

import tday.util
import tday.mxlScores
import tday.plainScores
import tday.learning
import tday.transform
import tday.config

import sys
import os.path
import time

def convert():
  composer = 'Hofstadter, Douglas'

  tday.plainScores.convertMxlComposer(
    tday.mxlScores.getComposerPaths(composer)
  )

def classify():
  nrSplits = 60
  nrSlices = 10
  maxDepth = 50
  composers = [
    # 'bach',
    # 'oneills1850',
    # 'trecento',

    'Bach, Johann Sebastian',
    # 'Beethoven, Ludwig van',
    # 'Brahms, Johannes',
    # 'Chopin, Frederic',
    'Debussy, Claude',
    # 'Fauré, Gabriel',

    # 'Alsen, Wulf Dieter',
    # 'Blindow, Karl-Gottfried',
    # 'Albeniz, Isaac',
  ]
  featureExtractors = [
    ['interval frequency', tday.plainFeatures.makeIntervalFrequencyFeature],
    # ['duration frequency', tday.plainFeatures.makeDurationFrequencyFeature],
    # ['random', tday.plainFeatures.makeRandomFeature],
  ]

  [allScores, allLabels] = tday.plainScores.getComposerData(
    composers, splits=nrSplits
  )
  print '[test#classify] ' + str(len(allScores)) + ' scores'
  tday.learning.testFeatures(
    allScores, allLabels, featureExtractors,
    nrSlices=nrSlices, classNames=composers, maxDepth=maxDepth, verbose=False
  )
  tday.learning.averageFeatures(allScores, allLabels, featureExtractors)

def transform():
  path = '../data/mxl/composers/Bach, Johann Sebastian/200-English Suite I in A major: Nr. 1 Prelude.mxl'
  name = os.path.basename(path)
  score = tday.mxlScores.loadScores([path])[0]

  """
  Bach
  [x] m6  8  -1.0000000000000
  [x] P12  19  -1.0000000000000
  [x] m2  1  -0.8181818181818
  [x] P15  24  -0.5000000000000
  [x] d5  6  -0.3333333333333
  [ ] P4  5  0.0000000000000
  [ ] M6  9  0.0000000000000
  [ ] M7  11  0.0000000000000
  [ ] P8  12  0.0000000000000
  [ ] m9  13  0.0000000000000
  [ ] m10  15  0.0000000000000
  [ ] m13  20  0.0000000000000
  [ ] m16  25  0.0000000000000
  [ ] M16  26  0.0000000000000
  [ ] m17  27  0.0000000000000
  [ ] M18  28  0.0000000000000
  [ ] P19  29  0.0000000000000
  [ ] P1  0  0.2000000000000
  [ ] d12  18  0.2258064516129
  [ ] m7  10  0.3333333333333
  [ ] M10  16  0.6000000000000
  [ ] M3  4  0.6666666666667
  [ ] P11  17  1.0000000000000
  [ ] M13  21  1.0000000000000
  [x] M2  2  1.0000000000000
  [x] M14  23  1.0000000000000
  [x] m14  22  1.0000000000000
  [ ] m3  3  1.0000000000000
  [x] P5  7  1.0000000000000
  [x] M9  14  1.0000000000000
  Debussy

  m6 (8) -> M9 (14)
  P12 (19) -> M14 (23)
  m2 (1) -> M2 (2)
  P15 (24) -> m14(22)
  d5 (6) -> P5 (7)
  """
  score = tday.transform.transformPitches(score, 8, 14)
  score = tday.transform.transformPitches(score, 19, 23)
  score = tday.transform.transformPitches(score, 1, 2)
  score = tday.transform.transformPitches(score, 6, 7)

  scorePath = os.path.join(
    tday.config.paths['transformed'],
    str(time.time()) + '-bach-debussy-' + name + '.xml'
  )
  print score.write('xml', scorePath)

def main():
  if len(sys.argv) < 2:
    print 'Usage: python test.py [convert|classify|transform]'
    sys.exit(1)

  action = sys.argv[1]

  if action == 'convert':
    convert()
  elif action == 'classify':
    classify()
  elif action == 'transform':
    transform()

if __name__ == '__main__':
  main()
