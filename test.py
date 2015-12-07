import tday.util
import tday.mxlScores
import tday.plainScores
import tday.plainFeatures
import tday.learning

import numpy as np

verbose = False

def getCorpusComposerData(composers):
  allScoreSets = []
  for composer in composers:
    composerScores = tday.plainScores.getCorpusComposerPaths(composer)[0:10]
    allScoreSets.append([composer, composerScores])
  allScores = []
  allLabels = []
  for scoreSet in allScoreSets:
    allScores += tday.plainScores.loadScores(scoreSet[1])
    allLabels += ([scoreSet[0]] * len(scoreSet[1]))
  return [allScores, allLabels]

def getComposerData(composers):
  allScoreSets = []
  for composer in composers:
    composerScores = tday.plainScores.getComposerPaths(composer)[0:10]
    allScoreSets.append([composer, composerScores])
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
      rawPredictions.append(pred)
      rawAccuracies.append(acc)
      print '[test#testTree] (fold ' + str(foldIdx) + ') ' + str(acc * 100) + '% accuracy'

    predictions = np.array(rawPredictions)
    accuracies = np.array(rawAccuracies)
    print '[test#testTree] ' + str(np.average(accuracies) * 100) + '% average accuracy'
    print '[test#testTree] ' + str(np.std(accuracies) * 100) + ' standard deviation'

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
  # [allScores, allLabels] = getComposerData(composers)
  [allScores, allLabels] = getCorpusComposerData(composers)
  print allLabels

  print '[main] ' + str(len(allScores)) + ' scores'
  testTree(allScores, allLabels, nrSlices=5, classNames=composers, maxDepth=1)

if __name__ == '__main__':
  main()
