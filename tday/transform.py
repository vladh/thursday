def transformPitches(score, srcSt, dstSt):
  """
  Transforms a score, converting degrees of `srcSt` semitones to `dstSt` semitones.

  @param score {music21.score.Score, music21.stream.Opus}
  @param srcSt {int}
  @param dstSt {int}
  @return {music21.score.Score}
  """
  print '[transformPitches] Transforming from ' + music21.interval.Interval(srcSt).name + ' to ' + music21.interval.Interval(dstSt).name

  if isinstance(score, music21.stream.Opus):
    print '[transformPitches] WARNING: Merging Opus'
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
            newNote = note.transpose(srcSt - (0 - dstSt))
            newInterval = music21.interval.Interval(newNote.pitch, key.getTonic())
            print '[transformPitches] ' + note.name + ' (' + interval.name + \
              ') -> ' + newNote.name + ' (' + newInterval.name + ')'
            note.pitch = newNote.pitch

  return score

