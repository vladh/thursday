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

#
# > Options
#

def _transformScore(score):
  newScore = score
  newScore = tday.transform.transformPitches(newScore, 8, 14)
  newScore = tday.transform.transformPitches(newScore, 19, 23)
  newScore = tday.transform.transformPitches(newScore, 1, 2)
  newScore = tday.transform.transformPitches(newScore, 6, 7)
  return newScore

options = {
  'convert': {
    'composer': 'Hofstadter, Douglas'
  },
  'classify': {
    'nrSplits': 60,
    'nrSlices': 10,
    'maxDepth': 50,
    'composers': [
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
    ],
    'featureExtractors': [
      ['interval frequency', tday.plainFeatures.makeIntervalFrequencyFeature],
      # ['duration frequency', tday.plainFeatures.makeDurationFrequencyFeature],
      # ['random', tday.plainFeatures.makeRandomFeature],
    ]
  },
  'transform': {
    'path': '../data/mxl/composers/Bach, Johann Sebastian/200-English Suite I in A major: Nr. 1 Prelude.mxl',
    'name': 'bach-debussy',
    'transformScore': _transformScore
  }
}

#
# <
#

def convert():
  tday.plainScores.convertMxlComposer(
    tday.mxlScores.getComposerPaths(options['convert']['composer'])
  )

def classify():
  [allScores, allLabels] = tday.plainScores.getComposerData(
    options['classify']['composers'], splits=options['classify']['nrSplits']
  )
  print '[test#classify] ' + str(len(allScores)) + ' scores'
  tday.learning.testFeatures(
    allScores, allLabels, options['classify']['featureExtractors'],
    nrSlices=options['classify']['nrSlices'],
    classNames=options['classify']['composers'],
    maxDepth=options['classify']['maxDepth'], verbose=False
  )
  tday.learning.averageFeatures(
    allScores, allLabels, options['classify']['featureExtractors']
  )

def transform():
  scoreName = os.path.basename(options['transform']['path'])
  score = tday.mxlScores.loadScores([options['transform']['path']])[0]
  transformedScore = options['transform']['transformScore'](score)
  scorePath = os.path.join(
    tday.config.paths['transformed'],
    str(time.time()) + '-' + options['transform']['name'] + '-' + scoreName + '.xml'
  )
  print transformedScore.write('xml', scorePath)

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
