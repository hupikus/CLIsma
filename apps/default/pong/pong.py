from type.colors import Colors
from integration.loghandler import Loghandler

import math
import random

from NodeSquad.modules.window import Window
class pong(apphabit):
    def __init__(self, node, args = ''):
        self.node = node
        self.controller = node.controller
        self.height = node.height
        self.width = node.width

        self.mouselen = self.controller.mouselen
        Loghandler.Log(f"pong init, {self.mouselen} mouses detected")

        self.ball_y = 7
        self.ball_x = 32
        self.ball_ry = 7.0
        self.ball_rx = 32.0
        self.ball_dir = 0.0
        self.ball_speed = 0.4
        self.ball_speedboost = 0.0

        self.player1_y = 0
        self.player2_y = 0
        self.player1_speed = 0
        self.player2_speed = 0
        self.p1score = 0
        self.p2score = 0
        self.platform_width = 5

    def draw(self, delta):
        write = self.node.appendStr
        w = self.platform_width
        p1 = self.player1_y
        p2 = self.player2_y
        speedangle = 60
        frameboost = delta * 60

        p1speed = self.player1_speed / frameboost
        p2speed = self.player2_speed / frameboost

        self.clear()

        for y in range(self.height + 1):
            if y >= p1 and y < p1 + w:
                write(y, 0, '|')
            if y >= p2 and y < p2 + w:
                write(y, 64, '|')
            write(self.ball_y, self.ball_x, ' ', Colors.colorPair(1) | Colors.FXReverse)

        self.ball_rx += math.cos(math.radians(self.ball_dir)) * (self.ball_speed + self.ball_speedboost) * frameboost
        self.ball_ry += math.sin(math.radians(self.ball_dir)) * (self.ball_speed + self.ball_speedboost) * frameboost

        if self.ball_rx <= 0.5 and self.ball_ry >= p1 and self.ball_ry < p1 + w:
            self.ball_dir = 180 - self.ball_dir
            self.ball_dir += speedangle * p1speed
            self.ball_dir %= 360
            self.ball_rx = 1.0
            if self.ball_speedboost < 0.3: self.ball_speedboost += 0.022

        elif self.ball_rx >= 63.5 and self.ball_ry >= p2 and self.ball_ry < p2 + w:
            self.ball_dir = 180 - self.ball_dir
            self.ball_dir -= speedangle * p2speed
            self.ball_dir %= 360
            self.ball_rx = 63.0
            if self.ball_speedboost < 0.3: self.ball_speedboost += 0.022

        if self.ball_ry <= 0.5:
            self.ball_dir = -self.ball_dir
            self.ball_ry = 1.0

        elif self.ball_ry >= 14.5:
            self.ball_dir = -self.ball_dir
            self.ball_ry = 14.0

        #reset
        if self.ball_rx < -0.5:
            self.p2score += 1
            self.ball_dir = 180.0
            self.ball_ry = 7.0
            self.ball_rx = 32.0
            self.ball_speedboost = 0.0
        elif self.ball_rx > 64.5:
            self.p1score += 1
            self.ball_dir = 0.0
            self.ball_ry = 7.0
            self.ball_rx = 32.0
            self.ball_speedboost = 0.0


        self.ball_y = round(self.ball_ry)
        self.ball_x = round(self.ball_rx)


        p1 = min(max(self.controller[0].mouse_y - self.node.from_y, 0), self.height) - (w >> 1)
        if self.mouselen > 1:
            p2 = min(max(self.controller[1].mouse_y - self.node.from_y, 0), self.height) - (w >> 1)
        else:
            p2 = self.player1_y

        self.player1_speed += (p1 - self.player1_y - self.player1_speed) / 5
        self.player2_speed += (p2 - self.player2_y - self.player2_speed) / 5
        self.player1_y = p1
        self.player2_y = p2

        write(3, 31, f"{self.p1score}:{self.p2score}")

    def onresize(self, height, width):
        self.node.resize(14, 64)

    def clear(self):
        write = self.node.appendStr
        space = ' ' * self.width
        for y in range(self.height):
            write(y, 0, space)
