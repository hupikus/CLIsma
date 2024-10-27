import os
from apps.apphabit import apphabit
class fileman(apphabit):

    def __init__(self, id, node, controller, height, width):
		#base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width


        self.preferred_height = 15
        self.preferred_width = 45

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]
        
        self.space = ' ' * self.width

        #file management
        #as fileman grows it will be moved to separate classes
        self.dir = "~/"

        filelist = self.scandir()


    def draw(self):
        self.node.appendStr(0, 0, scspaceape)
        self.node.appendStr(1, 0, scspaceape)
        self.node.appendStr(2, 0, scspaceape)
        #self.node.appendStr(2, 0, '\n'.join(filelistt))


    def scandir(path=self.dir):
        return os.listdir(path)