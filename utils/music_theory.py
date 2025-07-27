
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

def noteName(n):
    return f"{NOTES[n % 12]}{n // 12 - 1}"

def getOctave(n):
    return n // 12 - 1

def getNote(n):
    return NOTES[n % 12]
