#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tday.mxlScores
import tday.plainScores

import music21
import numpy as np
import yaml
from os.path import basename, dirname

def testLearning():
  """
  Uses deprecated API.
  """
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

def convertBachTrecentoCorpusToPlain():
  paths = tday.mxlScores.getCorpusComposerPaths('bach') + \
          tday.mxlScores.getCorpusComposerPaths('trecento')
  for path in paths:
    score = tday.mxlScores.loadCorpusScores([path])[0]
    plainScore = tday.plainScores.fromMxl(score)
    composer = basename(dirname(path))
    name = basename(path)
    print 'Writing simple score for ' + composer + '/' + name
    tday.plainScores.writeCorpusScore(plainScore, composer, name)

def main():
  paths = tday.plainScores.getCorpusComposerPaths('bach')[0:2]
  for score in tday.plainScores.loadScores(paths):
    print score

if __name__ == '__main__':
  main()
