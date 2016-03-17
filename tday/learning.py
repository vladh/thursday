import tday.util
import tday.config
import tday.plainFeatures

import numpy as np
import sklearn.metrics as metrics

from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.externals.six import StringIO
import os.path
import time

def treeClassify(
  trainSamples, trainLabels, testSamples, testLabels, classNames=None,
  maxDepth=None, verbose=False
):
  """
  Runs a decision tree classifier on a given data set.

  @param trainSamples {np.array}
  @param trainLabels {np.array}
  @param testSamples {np.array}
  @param testLabels {np.array}
  @param classNames {List<str>}
  @param maxDepth {int}
  @param verbose {bool}
  """
  clf = tree.DecisionTreeClassifier(max_depth=maxDepth)
  clf.fit(trainSamples, trainLabels)
  pred = np.array(clf.predict(testSamples))

  if verbose:
    print testLabels
    print pred

  acc = (testLabels == pred).sum() / float(len(testLabels))

  graphvizPath = os.path.join(
    tday.config.paths['learning-dot'], 'tree-' + str(time.time()) + '.dot'
  )

  with open(graphvizPath, 'w') as fp:
    tree.export_graphviz(
      clf, out_file=fp, class_names=classNames, filled=True, rounded=True,
      special_characters=True
    )

  return [pred, acc]

def testFeatures(
  allScores, allLabels, featureExtractors,
  nrSlices=1, classNames=None, maxDepth=None, verbose=False
):
  """
  Runs a decision tree classifier with various feature extractors on folds
  of the given data. Prints the results.

  @param allScores {np.array}
  @param allLabels {np.array}
  @param featureExtractors {List<List<str, function>>} A list of pairs of
    extractor name and extractor function (e.g. from tday.plainFeatures).
  @param nrSlices {np.array} The number of split/merge slices
  @param classNames {List<str>}
  @param maxDepth {int}
  @param verbose {bool}
  """
  allScores = np.array(allScores)
  allLabels = np.array(allLabels)
  [allScores, allLabels] = tday.util.unisonShuffle(allScores, allLabels)

  for featureExtractor in featureExtractors:
    print '[learning#testFeatures] Using feature extractor: ' + featureExtractor[0]

    rawPredictions = []
    rawAccuracies = []

    for foldIdx in xrange(nrSlices):
      [trainScores, testScores] = tday.util.crossfold(allScores, nrSlices, foldIdx)
      [trainLabels, testLabels] = tday.util.crossfold(allLabels, nrSlices, foldIdx)

      trainSamples = np.array([featureExtractor[1](score) for score in trainScores])
      testSamples = np.array([featureExtractor[1](score) for score in testScores])

      [pred, acc] = treeClassify(
        trainSamples, trainLabels, testSamples, testLabels,
        classNames=classNames, maxDepth=maxDepth, verbose=verbose
      )
      rawPredictions.extend(pred)
      rawAccuracies.append(acc)

      print '[learning#testFeatures] (fold ' + str(foldIdx) + ') ' + str(acc * 100) + '% accuracy'

    predictions = np.array(rawPredictions)
    accuracies = np.array(rawAccuracies)

    metricsAccuracy = metrics.accuracy_score(allLabels, predictions)
    metricsStd = np.std(accuracies)
    metricsReport = metrics.classification_report(allLabels, predictions).rstrip()
    metricsConfusion = metrics.confusion_matrix(allLabels, predictions)

    metricsString = ''
    metricsString += '# average accuracy: ' + str(metricsAccuracy) + '\n'
    metricsString += '# fold accuracy standard deviation: ' + str(metricsStd) + '\n'
    metricsString += '# confusion matrix\n'
    metricsString += str(metricsConfusion) + '\n'
    metricsString += '# classification report\n'
    metricsString += str(metricsReport) + '\n'

    print '[learning#testFeatures] classification metrics'
    print '  ' + '  '.join(metricsString.splitlines(True))

def averageFeatures(allScores, allLabels, featureExtractors):
  """
  Prints some information on the distribution of samples.

  @param allScores {np.array}
  @param allLabels {np.array}
  @param featureExtractors {List<List<str, function>>} A list of pairs of
    extractor name and extractor function (e.g. from tday.plainFeatures).
  """
  allScores = np.array(allScores)
  allLabels = np.array(allLabels)
  labels = list(set(allLabels))

  for featureExtractor in featureExtractors:
    print '[learning#averageFeatures] Using feature extractor: ' + featureExtractor[0]

    allSamples = np.array([featureExtractor[1](score) for score in allScores])

    labelMeans = {}
    for label in labels:
      samples = allSamples[np.where(allLabels == label)[0]]
      labelMeans[label] = np.mean(samples, axis=0)

    meansDiff = labelMeans[labels[0]] - labelMeans[labels[1]]
    meansDiffSorted = sorted(list(enumerate(meansDiff)), key=lambda d: d[1])

    for label in labels:
      print '[learning#averageFeatures] ' + label
      print "\n".join(map(str, list(enumerate(labelMeans[label]))))
    print '[learning#averageFeatures] ' + labels[0] + ' - ' + labels[1]
    print "\n".join(map(str, meansDiffSorted))

