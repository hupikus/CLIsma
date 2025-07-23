from integration.loghandler import Loghandler


class KeyboardController:

    def __init__(self, parentController):
        self.listeners = parentController.keyboard_listen

    def keyPress(self, key):
        for node in self.listeners:
            node.keyPress(key)

    def keyRelease(self, key):
        for node in self.listeners:
            node.keyRelease(key)
