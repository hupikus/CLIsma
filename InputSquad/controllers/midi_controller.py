from integration.loghandler import Loghandler


from .typecontroller import TypeController
class MidiController(TypeController):

    def __init__(self, parentController):
        self.listeners = parentController.midi_listen

    def keyPress(self, note, pressure):
        #Loghandler.Log(note_name(note))
        for node in self.listeners:
            node.midikeyPress(note, pressure)

    def keyRelease(self, note):
        for node in self.listeners:
            node.midikeyRelease(note)
