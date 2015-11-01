#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tday.learning

import numpy as np

def main():
  trainScores = np.array(
    tday.scores.loadScores(tday.scores.getCorpusComposerSources('bach', limit=7)) + \
    tday.scores.loadScores(tday.scores.getCorpusComposerSources('trecento', limit=7))
  )
  trainNames = np.array((['bach'] * 7) + (['trecento'] * 7))
  [trainSamples, trainLabels] = tday.learning.getTrainData(trainScores, trainNames)

  testScores = np.array(
    tday.scores.loadScores(tday.scores.getCorpusComposerSources('bach', limit=20))[-5:-1] + \
    tday.scores.loadScores(tday.scores.getCorpusComposerSources('trecento', limit=20))[-5:-1]
  )
  testNames = np.array((['bach'] * 4) + (['trecento'] * 4))
  [testSamples, testLabels] = tday.learning.getTestData(testScores, testNames)

  tday.learning.evaluateClassifiers(trainSamples, trainLabels, testSamples, testLabels)

if __name__ == '__main__':
  main()
