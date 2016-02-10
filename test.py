import tday.util
import tday.mxlScores
import tday.plainScores
import tday.plainFeatures
import tday.learning

import numpy as np
import sklearn.metrics as metrics

verbose = False

def testTree(allScores, allLabels, nrSlices=1, classNames=None, maxDepth=None):
  allScores = np.array(allScores)
  allLabels = np.array(allLabels)
  [allScores, allLabels] = tday.util.unisonShuffle(allScores, allLabels)

  featureExtractors = [
    ['interval frequency', tday.plainFeatures.makeIntervalFrequencyFeature],
    ['duration frequency', tday.plainFeatures.makeDurationFrequencyFeature],
    ['random', tday.plainFeatures.makeRandomFeature],
  ]

  for featureExtractor in featureExtractors:
    rawPredictions = []
    rawAccuracies = []
    print '[test#testTree] Using feature extractor: ' + featureExtractor[0]
    for foldIdx in xrange(nrSlices):
      [trainScores, testScores] = tday.util.crossfold(allScores, nrSlices, foldIdx)
      [trainLabels, testLabels] = tday.util.crossfold(allLabels, nrSlices, foldIdx)

      trainSamples = np.array([featureExtractor[1](score) for score in trainScores])
      testSamples = np.array([featureExtractor[1](score) for score in testScores])

      [pred, acc] = tday.learning.testTree(
        trainSamples, trainLabels, testSamples, testLabels,
        classNames=classNames, maxDepth=maxDepth, verbose=verbose
      )
      rawPredictions.extend(pred)
      rawAccuracies.append(acc)
      print '[test#testTree] (fold ' + str(foldIdx) + ') ' + str(acc * 100) + '% accuracy'

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

    print '[test#testTree] classification metrics'
    print '  ' + '  '.join(metricsString.splitlines(True))

def main():
  # tday.plainScores.convertMxlComposer(
  #   tday.mxlScores.getComposerPaths('Albeniz, Isaac')
  # )
  # return

  composers = [
    'bach',
    # 'oneills1850',
    'trecento',

    # 'Bach, Johann Sebastian',
    # 'Beethoven, Ludwig van',
    # 'Brahms, Johannes',
    # 'Alsen, Wulf Dieter',
    # 'Blindow, Karl-Gottfried',
    # 'Albeniz, Isaac',
  ]
  [allScores, allLabels] = tday.plainScores.getCorpusComposerData(composers, limit=5)
  # [allScores, allLabels] = tday.plainScores.getComposerData(composers)
  print '[main] ' + str(len(allScores)) + ' scores'

  mergedScore = tday.plainScores.mergeScores(allScores)
  print len(mergedScore['measures'])
  # testTree(allScores, allLabels, nrSlices=22, classNames=composers, maxDepth=1)

if __name__ == '__main__':
  main()
