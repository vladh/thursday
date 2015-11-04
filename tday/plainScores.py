import tday.music
import tday.paths

import music21
from os import mkdir
from os.path import dirname, exists

def fromMxl(score):
  plainScore = {
    'measures': []
  }

  for part in score.parts:
    for measure in part.getElementsByClass('Measure'):
      key = tday.music.keyFromKeySignature(measure.flat.getKeySignatures()[0])
      sig = measure.getTimeSignatures()[0]
      plainMeasure = {
        'key': key.tonicPitchNameWithCase,
        'timeSignature': sig.ratioString,
        'notes': []
      }
      for generalNote in measure.flat.notes:
        if isinstance(generalNote, music21.chord.Chord):
          notes = []
          for pitch in generalNote.pitches:
            note = music21.note.Note(pitch)
            note.offset = generalNote.offset
            note.duration = generalNote.duration
            notes.append(note)
        elif isinstance(generalNote, music21.note.Note):
          notes = [generalNote]
        for note in notes:
          offset = score.offset + part.offset + measure.offset + note.offset
          interval = music21.interval.Interval(note.pitch, key.getTonic())
          semitones = interval.cents / 100
          plainNote = {
            'start': offset,
            'duration': note.duration.quarterLength,
            'keyDegree': interval.intervalClass,
            'keySemitones': semitones
          }
          plainMeasure['notes'].append(plainNote)
      plainScore['measures'].append(plainMeasure)

  return plainScore

def write(plainScore, plainName):
  plainPath = tday.paths.paths['plainCorpusRoot'] + plainName
  plainDirName = dirname(plainPath)
  if not exists(plainDirName): mkdir(plainDirName)
  with open(plainPath, 'w') as fp:
    fp.write(str(plainScore))
