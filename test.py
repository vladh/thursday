import tday.util
import tday.mxlScores
import tday.plainScores
import tday.plainFeatures
import tday.learning

import numpy as np

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

def testTree(allScores, allLabels, nrSlices=1, classNames=None, maxDepth=None):
  allScores = np.array(allScores)
  allLabels = np.array(allLabels)
  [allScores, allLabels] = tday.util.unisonShuffle(allScores, allLabels)
  rawPredictions = []
  rawAccuracies = []

  for foldIdx in xrange(nrSlices):
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

    [pred, acc] = tday.learning.testTree(trainSamples, trainLabels, testSamples, testLabels,
                                         classNames=classNames, maxDepth=maxDepth)
    rawPredictions.append(pred)
    rawAccuracies.append(acc)
    print '[test#testTree] (fold ' + str(foldIdx) + ') ' + str(acc * 100) + '% accuracy'

  predictions = np.array(rawPredictions)
  accuracies = np.array(rawAccuracies)
  print '[test#testTree] ' + str(np.average(accuracies) * 100) + '% average accuracy'
  print '[test#testTree] ' + str(np.std(accuracies) * 100) + ' standard deviation'

def main():
  # tday.plainScores.convertMxlCorpus(tday.mxlScores.getCorpusComposerPaths('oneills1850'))

  composers = ['bach', 'trecento']
  [allScores, allLabels] = getCorpusComposerData(composers)
  testTree(allScores, allLabels, nrSlices=11, classNames=composers, maxDepth=1)

if __name__ == '__main__':
  main()
