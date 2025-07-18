import os
import sys
import gi

from type.colors import Colors
from integration.loghandler import Loghandler

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


        self.player = Gst.ElementFactory.make("playbin", "player")
        if player:
            path = params
            if path[] != "file://":
                path = "file://" + path

            player.set_property("uri", path)
            player.set_state(Gst.State.PLAYING)


def pause(self, pause):
    if pause:
        self.player.set_state(Gst.State.PAUSED)
    else:
        self.player.set_state(Gst.State.PLAYING)


def draw(self, delta):
    self.node.addstr()

def process(self, delta):
    state = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS | Gst.MessageType.ERROR)


def abort(self):
    self.player.set_state(Gst.State.NULL)
