import os
from type.colors import Colors
from apps.apps import App

from apps.apphabit import apphabit

from userglobals import userglobals
from integration.loghandler import Loghandler

from integration.filehandler import Filehandler
class fileman(apphabit):

    def __init__(self, id, node, controller, height, width, params):
		#base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width


		#input
        self.input_subscriptions = [controller.MouseEvents, controller.MouseWheelEvents, controller.KeyboardEvents]

        self.space = ' ' * self.width

        #file management
        #as fileman grows it will be moved to separate classes
        self.dir = userglobals.userpath
        self.childfolder = userglobals.username

        self.filelen = 0
        self.filelist = self.scandir()

        self.scrollpos = 0
        self.cached_scrollposes = {}
        self.is_slider = 0
        self.error_messages = ['', "Folder is empty", "Permission denied"]
        self.errorno = 0

        #colors
        self.colors = Colors.colorlen
        #                    file                   folder              hidden folder       hidden file
        if self.colors == 256:
            self.colormode = [Colors.colorPair(88), Colors.colorPair(229), Colors.colorPair(138), Colors.colorPair(40)]
        elif self.colors >= 8:
            self.colormode = [Colors.colorPair(6), Colors.colorPair(5), Colors.colorPair(7), Colors.colorPair(3)]
        else:
            self.colormode = [Colors.colorPair(0) for i in range(4)]

        #uis
        self.ui = self.node.ui
        self.ui.clickableArt("upb", self.moveup, 1, 0, ["Up "], width = 3)


        #temp
        self.resizelist()
        self.space = ' ' * self.width


        #menu
        self.menuapp = App("default/fileman/contextmenu")
        self.menu = 0
        self.menuclass = None

    def draw(self, delta):
        self.node.appendStr(self.height - 1, 0, self.space)
        if self.childfolder == '':
            self.node.appendStr(0, 0, '/'.center(self.width, ' '), Colors.FXBold)
        else:
            self.node.appendStr(0, 0, self.childfolder.center(self.width, ' '), Colors.FXBold)
        self.node.appendStr(1, 0, self.space)
        self.node.appendStr(2, 0, '_' * self.width)
        if self.filelen == 0:
            self.node.appendStr(3, 0, self.error_messages[self.errorno].center(self.width, ' '), Colors.FXPale)
            return 0
        for y in range(self.oblen):
            self.node.appendStr(3 + y, 0, self.space)
            if y + self.scrollpos < self.filelen:
                file = self.filelist[y + self.scrollpos]
                ind = 0

                m = Colors.FXNormal
                for i in range(self.controller.getPlayerNumber()):
                    if self.menu == 0 and self.controller[i].mouse_x >= self.node.from_x and self.controller[i].mouse_x < self.node.to_x:
                        if y + 3 == self.controller[i].mouse_y - self.node.from_y:
                            m = Colors.FXReverse
                            break

                if self.colors >= 2:
                    if os.path.isdir(self.dir + file):
                        ind = 1
                    if file[0] == '.':
                        ind = 3 - ind

                    #try:
                    #self.node.appendStr(3 + y, 0, self.filelist[y + self.scrollpos], self.colormode[ind] | m)
                    self.node.appendStr(3 + y, 0, self.filelist[y + self.scrollpos].ljust(self.width - self.is_slider, ' '), self.colormode[ind] | m)
                    #except:
                        #Loghandler.Log(str(self.filelist))
                        #self.node.abort()

    def onresize(self, height, width):
        self.height = height
        self.width = width
        self.space = ' ' * width
        self.resizelist()

    def click(self, device_id, button, y, x):
        if self.menu == 1:
            self.closemenu()
        if y >= 3 and y <= self.height - 1 and x >= 0 and x < self.width - 1:
            ytap = y - 3 + self.scrollpos
            if ytap < self.filelen and self.menu == 0:
                filename = self.filelist[ytap]
                if button == 0:
                    appath = ''.join((self.dir, filename))
                    if os.path.isdir(appath):
                        Loghandler.Log(f"cd to ./{filename}")

                        self.cached_scrollposes[self.dir] = self.scrollpos
                        self.scrollpos = 0

                        self.dir = appath + '/'
                        self.childfolder = filename

                        self.filelist = self.scandir()
                        self.resizelist()
                    else:

                        app = Filehandler.appToUse(appath)
                        if app != None:
                            self.node.wm.newNodeByApp(app, y - 2, x - 10, 0, 0, appath)
                elif button == 1:
                    Loghandler.Log(f"options for {filename}")
                    self.menu = 1
                    self.menuclass = self.node.newNodeByApp(self.menuapp, y, x, 6, 15, '')
            elif button == 1:
                self.moveup('', 0, 0)


    def scroll(self, id, delta):
        if self.filelen > 0:
            self.scrollpos = min(max(0, self.scrollpos + delta), self.filelen - 2)
            self.ui.setSliderPos("fileSlider", round(self.scrollpos / self.filelen * self.height), type = "verticalSliders")


    def scandir(self, path = ''):
        isSet = False
        if path == '':
            path = self.dir
            isSet = True
        if os.access(path, os.R_OK):
            c = os.listdir(path)
            if path != '' and isSet:
                self.filelen = len(c)
                self.errorno = 1
            return c
        else:
            self.filelen = 0
            self.errorno = 2
            return []

    def resizelist(self):
        self.oblen = min(self.height - 4, self.filelen)
        self.is_slider = 0
        self.ui.remove("fileSlider")
        if self.oblen == self.height - 4 and self.filelen > 0:
            self.slider = 1
            self.ui.verticalSlider("fileSlider", self.scrollfileviaslider, 0, self.width - 1, self.height, round(self.scrollpos / self.filelen * self.height), railChar = '|', buttonChar = '*', buttonHeight = max(1, round(self.height / self.filelen)), railAttr = Colors.FXPale, buttonAttr = Colors.FXBold)


    #buttons and buttofs
    def moveup(self, name, button, device_id):
        if self.dir != '/':
            if self.dir in self.cached_scrollposes:
                del self.cached_scrollposes[self.dir]

            self.dir = self.dir[:-len(self.childfolder) - 1]
            self.childfolder = self.dir.split('/')[-2]
            self.filelist = self.scandir()

            if self.dir in self.cached_scrollposes:
                self.scrollpos = self.cached_scrollposes[self.dir]
            else:
                self.scrollpos = 0
            self.resizelist()
            Loghandler.Log("cd to ../")



    def closemenu(self):
        self.menu = 0
        self.menuclass.node.abort()
        self.menuclass = None


    def scrollfileviaslider(self, name, y):
        self.scrollpos = round(y / self.height * self.filelen)


