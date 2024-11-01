import os
from type.colors import Colors

from apps.apphabit import apphabit
from userglobals import userglobals
class fileman(apphabit):

    def __init__(self, id, node, controller, height, width, params):
		#base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width


        self.preferred_height = 15
        self.preferred_width = 45

		#input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]
        
        self.space = ' ' * self.width

        #file management
        #as fileman grows it will be moved to separate classes
        self.dir = userglobals.userpath

        self.filelist = self.scandir()

        self.scrollpos = 0

        #colors
        self.colors = Colors.colorlen
            #                 file                 folder               hidden folder        hidden file
        if self.colors == 256:
            self.colormode = [Colors.colorPair(88), Colors.colorPair(229), Colors.colorPair(138), Colors.colorPair(40)]
        else:
            self.colormode = [Colors.colorPair(0), Colors.colorPair(4), Colors.colorPair(7), Colors.colorPair(3)]

        #temp
        self.resizelist()


    def draw(self):
        self.node.appendStr(0, 0, self.space)
        self.node.appendStr(1, 0, self.space)
        self.node.appendStr(2, 0, self.space)
        self.node.appendStr(3, 0, self.space)
        for y in range(self.oblen):
            file = self.filelist[y + self.scrollpos]

            if self.colors >= 2:
                ind = 0
                if os.path.isdir(file):
                    ind = 1
                if file[0] == '.':
                    ind = 3 - ind
                self.node.appendStr(3 + y, 0, self.filelist[y + self.scrollpos], self.colormode[ind])
    
    def onresize(self, height, width):
        self.height = height
        self.width = width
        self.resizelist()


    def scandir(self, path = ''):
        if path == '':
            path = self.dir
        return os.listdir(path)
    
    def resizelist(self):
        self.oblen = min(self.height - 4, len(self.filelist))
        self.arrows = self.oblen == self.height - 1

