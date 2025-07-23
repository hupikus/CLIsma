
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

def NoteName(n):
    return f"{NOTES[n % 12]}{n // 12 - 1}"
