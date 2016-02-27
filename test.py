import tday.util
import tday.mxlScores
import tday.plainScores
import tday.learning

def convert():
  tday.plainScores.convertMxlComposer(
    tday.mxlScores.getComposerPaths('Hofstadter, Douglas')
  )

def classify():
  composers = [
    # 'bach',
    # 'oneills1850',
    # 'trecento',

    'Bach, Johann Sebastian',
    # 'Beethoven, Ludwig van',
    # 'Brahms, Johannes',
    # 'Chopin, Frederic',
    'Debussy, Claude',

    # 'Alsen, Wulf Dieter',
    # 'Blindow, Karl-Gottfried',
    # 'Albeniz, Isaac',
  ]

  [allScores, allLabels] = tday.plainScores.getComposerData(composers, splits=10)

  tday.learning.testFeatures(
    allScores, allLabels, nrSlices=10, classNames=composers, maxDepth=1, verbose=False
  )

  print '[test#classify] ' + str(len(allScores)) + ' scores'

def transform():
  score.show('text')

def main():
  # convert()
  classify()
  # transform()

if __name__ == '__main__':
  main()
