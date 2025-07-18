class apphabit:

    preferred_height = 9
    preferred_width = 45

    #ABCS

    def draw(self, delta):
        pass

    def process(self, delta):
        pass

    #INPUT

    def click(self, device_id, button, y, x):
        pass

    def drag(self, id, button, stage, y, x):
        pass

    def scroll(self, id, delta):
        pass

    def keyboard(self, code):
        pass

    #NODE EVENTS

    def onresize(self, height, width):
        self.height = height
        self.width = width

    def oncollapse(self):
        pass

    def abort(self):
        pass
