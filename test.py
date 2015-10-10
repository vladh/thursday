import thursday.music
import thursday.scores

def processScore(score):
  """
  Does various things with a score.
  """
  key = score.analyze('key')
  # NOTE: This (wrongly) always seems to get "4/4".
  sig = score.getTimeSignatures()[0]
  notes = score.flat.pitches
  intervals = thursday.music.makeNotesIntoTonicIntervals(notes, key.getTonic())
  freq = thursday.music.sortIntervalFrequencies(thursday.music.getIntervalFrequencies(intervals))

  print '# Score: ' + str(getattr(score, 'corpusFilepath', score.filePath))
  print '- Key of'
  print '  ' + str(key)
  print
  print '- Time signature'
  print '  ' + str(sig.ratioString)
  print
  print '- Interval frequencies'
  print '  ' + thursday.music.intervalFrequenciesToString(freq)
  print
  print

def main():
  bachScores = thursday.scores.loadScores(thursday.scores.getComposerSources('bach', limit=2))
  [processScore(score) for score in bachScores]
  beethovenScores = thursday.scores.loadScores(thursday.scores.getComposerSources('beethoven', limit=2))
  [processScore(score) for score in beethovenScores]

if __name__ == '__main__':
  main()
