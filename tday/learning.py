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

def getTrainData():
  # bachSources = tday.scores.getFileComposerSources('Bach, Johann Sebastian')
  # bachLabels = ['bach' for _ in bachSources]

  # debussySources = tday.scores.getFileComposerSources('Debussy, Claude')
  # debussyLabels = ['bach' for _ in debussySources]

  # sources = np.array(bachSources + debussySources)
  # labels = np.array(bachLabels + debussyLabels)

  # [shufSources, shufLabels] = tday.util.unisonShuffle(sources, labels)

  # trainSources = shufSources[:-10]
  # trainLabels = shufLabels[:-10]
  # trainScores = tday.scores.loadScores(trainSources)

  trainScores = [] + \
                tday.scores.loadScores(tday.scores.getCorpusComposerSources('bach', limit=7)) + \
                tday.scores.loadScores(tday.scores.getCorpusComposerSources('schumann', limit=7))
  trainLabels = (['bach'] * 7) + (['schumann'] * 7)

  trainSamples = [tday.features.makeIntervalFrequencyFeature(score)[0] for score in trainScores]

  return [trainSamples, trainLabels]

def getTestData():
  # testSources = shufSources[-10:]
  # testLabels = shufLabels[-10:]
  # testScores = tday.scores.loadScores(testSources)

  testScores = [] + \
               tday.scores.loadScores(tday.scores.getCorpusComposerSources('bach', limit=40))[-6:-1]
  testLabels = np.array(['bach'] * 5)

  testSamples = [tday.features.makeIntervalFrequencyFeature(score)[0] for score in testScores]

  return [testSamples, testLabels]

def evaluateClassifiers():
  [trainSamples, trainLabels] = getTrainData()
  [testSamples, testLabels] = getTestData()

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
