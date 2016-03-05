# -*- coding: utf-8 -*-

import tday.util
import tday.mxlScores
import tday.plainScores
import tday.learning

def convert():
  tday.plainScores.convertMxlComposer(
    tday.mxlScores.getComposerPaths('Hofstadter, Douglas')
  )

def classify():
  nrSplits = 10
  nrSlices = 10
  maxDepth = 8

  composers = [
    # 'bach',
    # 'oneills1850',
    # 'trecento',

    'Bach, Johann Sebastian',
    # 'Beethoven, Ludwig van',
    # 'Brahms, Johannes',
    'Chopin, Frederic',
    'Debussy, Claude',
    # 'Fauré, Gabriel',

    # 'Alsen, Wulf Dieter',
    # 'Blindow, Karl-Gottfried',
    # 'Albeniz, Isaac',
  ]

  [allScores, allLabels] = tday.plainScores.getComposerData(composers, splits=nrSplits)
  print '[test#classify] ' + str(len(allScores)) + ' scores'
  tday.learning.testFeatures(
    allScores, allLabels, nrSlices=nrSlices, classNames=composers,
    maxDepth=maxDepth, verbose=False
  )

def transform():
  score.show('text')

def main():
  # convert()
  classify()
  # transform()

if __name__ == '__main__':
  main()
