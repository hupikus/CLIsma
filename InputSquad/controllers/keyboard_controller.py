import time
import threading

from integration.loghandler import Loghandler

from .typecontroller import TypeController
class KeyboardController(TypeController):

    def __init__(self, parentController):
        self.controller = parentController
        self.listeners = parentController.keyboard_listen

        self.key_repeat = []
        self.key_stage = {}
        self.work = True

        self.rate = 25
        self.treshold = 10


        t = threading.Thread(target = self.keyHold)
        t.start()


    def keyPress(self, key):
        self.controller.keys.KeyPress(key)
        self.holdQueue(key)
        for node in self.listeners:
            node.keyPress(key)
            node.keyType(key)

    def keyRelease(self, key):
        self.controller.keys.KeyRelease(key)
        self.holdQueueFree(key)
        for node in self.listeners:
            node.keyRelease(key)


    def keyHold(self):
        lock = threading.Lock()

        pause = 1.0 / self.rate

        kr = self.key_repeat
        ks = self.key_stage
        while self.work:
            with lock:
                for key in kr:
                    if ks[key] < self.treshold:
                        ks[key] += 1
                        continue

                    for node in self.listeners:
                        node.keyType(key)

            time.sleep(pause)

    def holdQueue(self, key):
        if key not in self.key_repeat:
            self.key_repeat.append(key)
            self.key_stage[key] = 0
        else:
            self.key_stage[key] = self.treshold

    def holdQueueFree(self, key):
        if key in self.key_repeat:
            self.key_repeat.remove(key)
            del self.key_stage[key]
        
    def holdQueueClear(self):
        self.key_repeat.clear()
        self.key_stage.clear()


    def abort(self):
        self.work = False
        self.holdQueueClear()
