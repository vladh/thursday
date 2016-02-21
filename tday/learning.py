import tday.util
import tday.config

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.externals.six import StringIO
import os.path
import time

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
    [pred, acc] = evaluateClassifier(classifier['clf'], trainSamples, trainLabels,
                                     testSamples, testLabels)
    return [classifier['name'], str(pred) + ' (' + str(acc * 100) + '% accuracy)']

  evaluations = map(prettyEvaluateClassifier, classifiers)
  tday.util.printTable('Predictions', evaluations)

def testTree(trainSamples, trainLabels, testSamples, testLabels, classNames=None, maxDepth=None, verbose=False):
  clf = tree.DecisionTreeClassifier(max_depth=maxDepth)
  clf.fit(trainSamples, trainLabels)
  pred = np.array(clf.predict(testSamples))

  if verbose:
    print testLabels
    print pred

  acc = (testLabels == pred).sum() / float(len(testLabels))

  graphvizPath = os.path.join(tday.config.paths['learning'], 'tree-' + str(time.time()) + '.dot')

  with open(graphvizPath, 'w') as fp:
    tree.export_graphviz(clf, out_file=fp, class_names=classNames, filled=True, rounded=True,
                         special_characters=True)

  return [pred, acc]
