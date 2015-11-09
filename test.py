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

def getCorpusComposerData(composers):
  allScoreSets = []
  for composer in composers:
    allScoreSets.append([composer, tday.plainScores.getCorpusComposerPaths(composer)])
  allScores = []
  allLabels = []
  for scoreSet in allScoreSets:
    allScores += tday.plainScores.loadScores(scoreSet[1])
    allLabels += ([scoreSet[0]] * len(scoreSet[1]))
  return [allScores, allLabels]

def main():
  # tday.plainScores.convertMxlCorpus()

  composers = ['bach', 'trecento']
  nrSlices = 11

  [allScores, allLabels] = getCorpusComposerData(composers)
  allScores = np.array(allScores)
  allLabels = np.array(allLabels)
  [allScores, allLabels] = tday.util.unisonShuffle(allScores, allLabels)
  rawPredictions = []
  rawAccuracies = []

  for foldIdx in xrange(nrSlices):
    print '[test#main] Fold ' + str(foldIdx)
    [trainScores, testScores] = tday.util.crossfold(allScores, nrSlices, foldIdx)
    [trainLabels, testLabels] = tday.util.crossfold(allLabels, nrSlices, foldIdx)

    trainSamples = np.array([
      tday.plainFeatures.makeIntervalFrequencyFeature(score)
      for score in trainScores
    ])
    testSamples = np.array([
      tday.plainFeatures.makeIntervalFrequencyFeature(score)
      for score in testScores
    ])

    [pred, acc] = tday.learning.testTree(trainSamples, trainLabels,
                                         testSamples, testLabels,
                                         classNames=composers, maxDepth=1)
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
