import os
import pydub

from type.colors import Colors

from apps.apphabit import apphabit
class bangerplayer(apphabit):

    def __init__(self, id, node, controller, height, width, params):
        #base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width

		#input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

        #os.system(f"play {params}")
        #self.sound = nava.play(params, async_mode=True, loop=False)
