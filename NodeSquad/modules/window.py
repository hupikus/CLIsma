from .module import Module
class Window(Module):

    preferred_height = 9
    preferred_width = 45

    def __init__(self, node, args = ''):
        self.node = node.node
        self.height = node.height
        self.width = node.width
        self.controller = node.controller
        self.ui = self.node.ui

    def draw(self, delta):
        self.node.clear()

    def resize(self, height, width):
        self.height = height
        self.width = width
