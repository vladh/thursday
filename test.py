#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tday.util
import tday.mxlScores
import tday.plainScores
import tday.plainFeatures
import tday.learning

import music21
import numpy as np
import pprint
from os.path import basename, dirname

def getAllData():
  allScoreSets = [
    ['bach', tday.plainScores.getCorpusComposerPaths('bach')],
    ['trecento', tday.plainScores.getCorpusComposerPaths('trecento')]
  ]
  allScores = []
  allLabels = []
  for scoreSet in allScoreSets:
    allScores += tday.plainScores.loadScores(scoreSet[1])
    allLabels += ([scoreSet[0]] * len(scoreSet[1]))
  return [allScores, allLabels]

def convertBachTrecentoCorpusToPlain():
  paths = tday.mxlScores.getCorpusComposerPaths('bach') + \
          tday.mxlScores.getCorpusComposerPaths('trecento')
  for path in paths:
    score = tday.mxlScores.loadCorpusScores([path])[0]
    composer = basename(dirname(path))
    name = basename(path)
    plainScore = tday.plainScores.fromMxl(score, composer + '/' + name)
    tday.plainScores.writeCorpusScore(plainScore, composer, name)

def testPlainFeatures():
  paths = tday.plainScores.getCorpusComposerPaths('bach')[0:2]
  for score in tday.plainScores.loadScores(paths):
    freq = tday.plainScores.getKeyIntervalFrequencies(score)
    freq = tday.util.sortDict(freq)
    print '[test#testPlainFeatures] ' + tday.util.setToString(freq)

def main():
  # convertBachTrecentoCorpusToPlain()
  [allScores, allLabels] = getAllData()
  allScores = np.array(allScores)
  allLabels = np.array(allLabels)
  [allScores, allLabels] = tday.util.unisonShuffle(allScores, allLabels)
  nrSlices = 11
  rawPredictions = []
  rawAccuracies = []

  for foldIdx in xrange(nrSlices):
    print '[test#main] Fold ' + str(foldIdx)
    [trainScores, testScores] = tday.util.crossfold(allScores, nrSlices, foldIdx)
    [trainLabels, testLabels] = tday.util.crossfold(allLabels, nrSlices, foldIdx)

    print '[test#main] Training scores:'
    pprint.pprint(zip([score['name'] for score in trainScores], trainLabels))
    print '[test#main] Test scores:'
    pprint.pprint(zip([score['name'] for score in testScores], testLabels))

    trainSamples = np.array([
      tday.plainFeatures.makeIntervalFrequencyFeature(score)
      for score in trainScores
    ])
    testSamples = np.array([
      tday.plainFeatures.makeIntervalFrequencyFeature(score)
      for score in testScores
    ])

    [pred, acc] = tday.learning.testTree(trainSamples, trainLabels, testSamples, testLabels)
    rawPredictions.append(pred)
    rawAccuracies.append(acc)

    print '[test#main] Prediction: ' + str(pred)
    print '[test#main] Accuracy: ' + str(acc * 100)
    print '[test#main] End of fold ' + str(foldIdx)
    print

  predictions = np.array(rawPredictions)
  accuracies = np.array(rawAccuracies)
  print '[test#main] ' + str(np.average(accuracies) * 100) + '% average accuracy'
  print '[test#main] ' + str(np.std(accuracies) * 100) + ' standard deviation'

if __name__ == '__main__':
  main()
