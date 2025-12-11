import numpy as np

class audio:

    def __init__(self, channels = 2, samplerate = 44100):
        self.name = "Unnamed"
        self.channels = channels
        self.samplerate = samplerate

        self.len = 0
        self.len_read = 0
        self.data = None

        self.loaded = False

    def init_data(self):
        self.data = np.empty((self.len, self.channels), dtype = np.float32)
