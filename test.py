# -*- coding: utf-8 -*-

import tday.util
import tday.mxlScores
import tday.plainScores
import tday.learning

import music21

def convert():
  tday.plainScores.convertMxlComposer(
    tday.mxlScores.getComposerPaths('Hofstadter, Douglas')
  )

def classify():
  nrSplits = 10
  nrSlices = 10
  maxDepth = 8

  composers = [
    # 'bach',
    # 'oneills1850',
    # 'trecento',

    'Bach, Johann Sebastian',
    # 'Beethoven, Ludwig van',
    # 'Brahms, Johannes',
    'Chopin, Frederic',
    'Debussy, Claude',
    # 'Fauré, Gabriel',

    # 'Alsen, Wulf Dieter',
    # 'Blindow, Karl-Gottfried',
    # 'Albeniz, Isaac',
  ]

  [allScores, allLabels] = tday.plainScores.getComposerData(composers, splits=nrSplits)
  print '[test#classify] ' + str(len(allScores)) + ' scores'
  tday.learning.testFeatures(
    allScores, allLabels, nrSlices=nrSlices, classNames=composers,
    maxDepth=maxDepth, verbose=False
  )

def doTransform(score, srcSt, dstSt):
  """
  Transforms a score, converting intervals of `srcSt` semitones to `dstSt` semitones.

  @param score {music21.score.Score, music21.stream.Opus}
  @param srcSt {int}
  @param dstSt {int}
  @return {music21.score.Score}
  """
  print '[doTransform] Transforming from ' + music21.interval.Interval(srcSt).name + ' to ' + music21.interval.Interval(dstSt).name

  if isinstance(score, music21.stream.Opus):
    print '[doTransform] WARNING: Merging Opus'
    score = score.mergeScores()

  for part in score.parts:
    for measure in part.getElementsByClass('Measure'):
      timeSig = measure.getTimeSignatures()[0]
      key = tday.mxlScores.getKeyFromMeasure(measure)
      for generalNote in measure.flat.notes:
        if isinstance(generalNote, music21.chord.Chord):
          notes = tday.mxlScores.getNotesFromChord(generalNote)
        elif isinstance(generalNote, music21.note.Note):
          notes = [generalNote]
        for note in notes:
          interval = music21.interval.Interval(note.pitch, key.getTonic())
          if (interval.cents / 100) == srcSt:
            newNote = note.transpose(srcSt - dstSt)
            newInterval = music21.interval.Interval(newNote.pitch, key.getTonic())
            print '[doTransform] ' + note.name + ' (' + interval.name + ') -> ' + newNote.name + ' (' + newInterval.name + ')'
            note = newNote

  return score

def transform():
  score = tday.mxlScores.loadScores(
    tday.mxlScores.getComposerPaths('Bach, Johann Sebastian', limit=1)
  )[0]
  score = doTransform(score, 7, 1)
  score.show('text')

def main():
  # convert()
  # classify()
  transform()

if __name__ == '__main__':
  main()
