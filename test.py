import tday.music
import tday.scores

def processScore(score):
  """
  Does various things with a score.
  """
  key = score.analyze('key')
  # NOTE: This (wrongly) always seems to get "4/4".
  sig = score.getTimeSignatures()[0]
  notes = score.flat.pitches
  intervals = tday.music.makeNotesIntoTonicIntervals(notes, key.getTonic())
  freq = tday.music.sortIntervalFrequencies(tday.music.getIntervalFrequencies(intervals))

  print '# Score: ' + str(getattr(score, 'corpusFilepath', score.filePath))
  print '- Key of'
  print '  ' + str(key)
  print
  print '- Time signature'
  print '  ' + str(sig.ratioString)
  print
  print '- Interval frequencies'
  print '  ' + tday.music.intervalFrequenciesToString(freq)
  print
  print

def main():
  bachScores = tday.scores.loadScores(tday.scores.getComposerSources('bach', limit=2))
  [processScore(score) for score in bachScores]
  beethovenScores = tday.scores.loadScores(tday.scores.getComposerSources('beethoven', limit=2))
  [processScore(score) for score in beethovenScores]

if __name__ == '__main__':
  main()
