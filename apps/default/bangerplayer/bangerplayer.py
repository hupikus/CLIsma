import os
import sys

import threading

extra = True

try:
    import soundfile as sf
    import sounddevice as sd
    import numpy as np
    from .audio import audio
except Exception as ex:
    extra = False



from type.colors import Colors
from integration.loghandler import Loghandler

from .layout import *

from NodeSquad.modules.window import Window
class bangerplayer(Window):

    def __init__(self, node):
        # Base
        self.node = node
        self.id = node.id
        self.controller = node.controller
        self.height = node.height
        self.width = node.width

        # Important-To-Abort targets
        self.opened = []
        self.thread = None

        # Player
        self.songs = {}
        self.song_id = 0
        self.current = 0
        self.current_instance = None

        self.playing = True
        self.sample_pos = 0
        self.prev_pos = 0
        self.stream = None

        # Input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

        if not extra: return

        if params:
            song = self.open(params)
            if song >= 0:
                self.play(song)


        # UI
        self.ui = node.neoui
        ui = self.ui

        self.file_list = ui.CreateCanvas(0, 0, self.height, 0)
        self.main_canvas = ui.CreateCanvas(0, 0, self.height, self.width)
        self.toggle_files = False



    def pause(self, pause):
        pass


    def open(self, file):
        song = len(self.songs)

        try:
            file = sf.SoundFile(file, "r")
            self.opened.append(file)

            audiofile = audio()
            audiofile.len = file.frames
            audiofile.samplerate = file.samplerate
            audiofile.channels = file.channels
            audiofile.init_data()

            name = os.path.basename(file.name)
            if name:
                audiofile.name = name

            self.songs[self.song_id] = audiofile
            self.song_id += 1

            if self.thread:
                self.thread.join()
            self.thread = threading.Thread(target = self.load, args = (file, audiofile))
            self.thread.start()

        except Exception as ex:
            Loghandler.Log(f"Bangerplayer: loading error: {ex}")
            return -1
        return song


    def load(self, soundfile, audiofile):
        block_size = audiofile.samplerate

        alen = audiofile.len
        ac = audiofile.channels
        data = audiofile.data

        ind = 0
        for chunk in soundfile.blocks(blocksize = block_size):
            if ac == 1:
                chunk = chunk.reshape(-1, 1)
            data[ind: ind + block_size] = chunk

            ind += block_size
            audiofile.len_read += block_size


        if soundfile in self.opened:
            self.opened.remove(soundfile)
        soundfile.close()
        audiofile.loaded = True


    def play(self, song):
        if song < 0: return
        self.current = song

        audiofile = self.songs.get(song, None)
        if not audiofile: return
        self.current_instance = audiofile

        self.sample_pos = 0

        first_stream = self.stream is None
        same_specs = False

        if not first_stream:
            same_specs = (
                self.stream.samplerate == audiofile.samplerate and
                self.stream.channels == audiofile.channels
            )

            if same_specs: return # Do nothing

            self.stream.stop()
            self.stream.close()

        self.stream = sd.OutputStream(
            samplerate = audiofile.samplerate,
            channels = audiofile.channels,
            dtype='float32',
            callback = self.stream_callback,
            blocksize = 1024
        )

        self.stream.start()


    def stream_callback(self, outdata, frames, time, status):
        if not self.playing: return

        audiofile = self.current_instance
        pos = self.sample_pos
        prev = self.prev_pos

        if pos + frames + audiofile.samplerate >= audiofile.len_read: return

        if abs(pos - prev) >= frames:

            ln = min(frames, audiofile.len - pos)
            if ln < frames:
                if ln > 0:
                    outdata[:ln] = audiofile.data[pos:pos + ln]
                outdata[ln:] = 0.0
            else:
                np.copyto(outdata, audiofile.data[pos:pos + frames])

        self.prev_pos = self.sample_pos
        self.sample_pos += frames



    def draw(self, delta):
        self.node.clear()
        if not extra:
            self.node.appendStr(0, 0, "Attention:".center(self.width, ' '), Colors.FXTextRed | Colors.FXBold)
            self.node.appendStr(1, 0, "You probably do not have CLIsma extras installed.")
            self.node.appendStr(2, 0, "BANGERPLAYER is the part of that.")
            self.node.appendStr(3, 0, "Just execute")
            self.node.appendStr(3, 14, "pip install -r requirements-extra.txt", Colors.FXTextBlue | Colors.FXReverse | Colors.FXBold)
            self.node.appendStr(4, 0, "in your CLIsma directory.".center(self.width, ' '))
            return
        
        current = None
        if self.current >= 0:
            current = self.current_instance

        if current and current.len_read < current.len and self.current == 0:
            self.node.appendStr(0, 0, f"{current.name} - {100 * current.len_read / current.len}%")
            return

        
        if current:
            self.node.appendStr(0, 0, current.name.center(self.width, ' '), Colors.FXBold)
        else:
            self.node.appendStr(0, 0, "No song playing".center(self.width, ' '))


    def resize(self, height, width):
        self.height = height
        self.width = width
        self.arrange_layout(self.toggle_files, height, width)


    def abort(self):
        # Exact order. Stream first. Load second. File last, if not closed.

        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except:
                pass

        if self.thread:
            self.thread.join()

        for file in self.opened:
            try:
                file.close()
            except:
                pass

