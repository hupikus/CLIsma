from apps.apphabit import apphabit
class settings(apphabit):

    def start(self):
        #self.node.ui.art("icon1", ["----", "---", "--", "-"], 1, 0)
        self.ui.clickableArt("icon1", self.submenu, 1, 0, ["-----  ", " --- ", "  -- ", "  -  "])

    def __init__(self, id, node, controller, height, width, params):
        #base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width


        self.preferred_height = 20
        self.preferred_width = 60

		#input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


        self.ui = self.node.ui

        self.start()


    def draw(self):
        self.node.appendStr(0, 0, "Settings")
        

    def submenu(self, name):
        self.ui.move(name, 0, 1)
