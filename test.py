# -*- coding: utf-8 -*-

import tday.util
import tday.mxlScores
import tday.plainScores
import tday.learning
import tday.transform

import sys
import music21

def convert():
  composer = 'Hofstadter, Douglas'

  tday.plainScores.convertMxlComposer(
    tday.mxlScores.getComposerPaths(composer)
  )

def classify():
  nrSplits = 40
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

def transform():
  score = tday.mxlScores.loadScores(
    tday.mxlScores.getComposerPaths('Bach, Johann Sebastian', limit=1)
  )[0]
  score.show('text')

  score = tday.transform.transformPitches(score, 6, 14)
  score = tday.transform.transformPitches(score, 6, 18)

  score.show('text')
  print score.write('xml', '/Users/vladh/Desktop/bach-debussy.xml')

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
