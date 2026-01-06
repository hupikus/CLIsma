class TypeController:
    def __init__(self, parentController):
        self.controller = parentController
        self.listeners = []

    def abort(self):
        pass
