from type.colors import Colors

from apps.apphabit import apphabit

from userglobals import userglobals
from integration.loghandler import Loghandler
class contextmenu(apphabit):

    def __init__(self, id, node, controller, height, width, params):
        #base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width


		#input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]



        self.wm = self.node.wm

    def draw(self, delta):
        self.node.appendStr(0, 0, "Open".center(self.width, ' '), Colors.FXReverse)
        self.node.appendStr(0, 0, "Rename".center(self.width, ' '), Colors.FXReverse)
        self.node.appendStr(0, 0, "Delete".center(self.width, ' '), Colors.FXReverse)




    def process(self, delta):
        if not self.node.isActive():
            self.wm.desktop.ismenu = False
            self.node.abort()
