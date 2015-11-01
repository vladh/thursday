import tday.util
import tday.music
import tday.scores
import tday.features

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

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

def getTrainData(scores, labels):
  samples = np.array([tday.features.makeIntervalFrequencyFeature(score)[0] for score in scores])
  [shufSamples, shufLabels] = tday.util.unisonShuffle(samples, labels)
  return [shufSamples, shufLabels]

def getTestData(scores, labels):
  samples = np.array([tday.features.makeIntervalFrequencyFeature(score)[0] for score in scores])
  [shufSamples, shufLabels] = tday.util.unisonShuffle(samples, labels)
  return [shufSamples, shufLabels]

def evaluateClassifiers(trainSamples, trainLabels, testSamples, testLabels):
  tday.util.printTable('Samples', [
    ['Train samples', trainSamples], ['Train labels', trainLabels],
    ['Test samples', testSamples], ['Test labels', testLabels]
  ])

  classifiers = [
    {'name': 'Random forests', 'clf': RandomForestClassifier(n_estimators=10)},
    {'name': 'SVM', 'clf': svm.SVC()},
    {'name': 'K-nearest neighbors', 'clf': KNeighborsClassifier(n_neighbors=3)},
    {'name': 'Gaussian naive Bayes', 'clf': GaussianNB()}
  ]

  def prettyEvaluateClassifier(classifier):
    [pred, acc] = evaluateClassifier(classifier['clf'], trainSamples, trainLabels, testSamples, testLabels)
    return [classifier['name'], str(pred) + ' (' + str(acc * 100) + '% accuracy)']

  evaluations = map(prettyEvaluateClassifier, classifiers)
  tday.util.printTable('Predictions', evaluations)
