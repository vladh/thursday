#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tday.util
import tday.music
import tday.scores
import tday.features
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def processScore(score):
  [sample, key, freq] = tday.features.makeIntervalFrequencyFeature(score)
  tday.util.printTable('Score: ' + str(getattr(score, 'corpusFilepath', score.filePath)), [
    ['Key of', str(key)],
    ['Interval frequencies', tday.music.intervalFrequenciesToString(tday.music.sortIntervalFrequencies(freq))],
    ['Interval frequency feature', str(sample)]
  ])

def evaluateClassifier(clf, trainSamples, trainLabels, testSamples, testLabels):
  """
  @param clf {sklearn classifier}
  @param trainSamples {List}
  @param trainLabels {List}
  @param testSamples {List}
  @param testLabels {List}
  @returns {List[pred, acc]}
  """
  clf.fit(trainSamples, trainLabels)
  pred = np.array(clf.predict(testSamples))
  acc = (testLabels == pred).sum() / float(len(testLabels))
  return [pred, acc]

def main():
  trainScores = [] + \
                tday.scores.loadScores(tday.scores.getComposerSources('bach', limit=7)) + \
                tday.scores.loadScores(tday.scores.getComposerSources('schumann', limit=7))
  trainSamples = [tday.features.makeIntervalFrequencyFeature(score)[0] for score in trainScores]
  trainLabels = (['bach'] * 7) + (['schumann'] * 7)

  testScores = [] + \
               tday.scores.loadScores(tday.scores.getComposerSources('bach', limit=40))[-6:-1]
  testSamples = [tday.features.makeIntervalFrequencyFeature(score)[0] for score in testScores]
  testLabels = np.array(['bach'] * 5)

  tday.util.printTable('Samples', [
    ['Train samples', trainSamples],
    ['Train labels', trainLabels],
    ['Test samples', testSamples],
    ['Test labels', testLabels]
  ])

  classifiers = [
    {'name': 'Random forests', 'clf': RandomForestClassifier(n_estimators=10)},
    {'name': 'SVM', 'clf': svm.SVC()},
    {'name': 'K-nearest neighbors', 'clf': KNeighborsClassifier(n_neighbors=3)},
    {'name': 'Gaussian naive Bayes', 'clf': GaussianNB()}
  ]

  def wrapEvaluateClassifier(classifier):
    [pred, acc] = evaluateClassifier(classifier['clf'], trainSamples, trainLabels, testSamples, testLabels)
    return [classifier['name'], str(pred) + ' (' + str(acc * 100) + '% accuracy)']

  evaluations = map(wrapEvaluateClassifier, classifiers)
  tday.util.printTable('Predictions', evaluations)

if __name__ == '__main__':
  main()
