from type.colors import Colors
from apps.apphabit import apphabit

import math

class pong(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width

		#self.node.resize(15, 65)

		self.ball_y = 7
		self.ball_x = 32
		
		self.ball_ry = 7.0
		self.ball_rx = 32.0
		

		self.ball_dir = 75.0
		self.ball_speed = 0.4

		self.player1_y = 0
		self.player2_y = 0
		self.p1score = 0
		self.p2score = 0

		self.platform_width = 5


	def draw(self):
		write = self.node.appendStr
		for y in range(16):
			if y >= self.player1_y and y < self.player1_y + self.platform_width:
				write(y, 0, '|')
			if y >= self.player1_y and y < self.player1_y + self.platform_width:
				write(y, 64, '|')
			write(self.ball_y, self.ball_x, ' ', Colors.colorPair(1) | Colors.FXReverse)

		#process the ball
		self.ball_rx += math.cos(self.ball_dir) * self.ball_speed
		self.ball_ry += math.sin(self.ball_dir) * self.ball_speed

		if self.ball_rx >= 63.5 and self.ball_ry >= self.player1_y and self.ball_ry < self.player1_y + self.platform_width:
			self.ball_dir += math.atan2(1, self.player1_y - self.ball_y - self.controller[0].mouse_dy)
			self.ball_dir = (-self.ball_dir + 180.0) % 360.0 - 180.0
			self.ball_rx = 63.0

		elif self.ball_rx <= 0.5 and self.ball_ry >= self.player2_y and self.ball_ry < self.player2_y + self.platform_width:
			self.ball_dir += math.atan2(1, self.player2_y - self.ball_ry - self.controller[0].mouse_dy)
			self.ball_dir = (-self.ball_dir + 180.0) % 360.0 - 180.0
			self.ball_rx = 1.0

		self.ball_dir = (self.ball_dir + 180.0) % 360.0 - 180.0

		if self.ball_ry <= 0.5:
			self.ball_dir = (-self.ball_dir + 180.0) % 360.0 - 180.0
			self.ball_ry = 1

		elif self.ball_ry >= 14.5:
			self.ball_dir = (-self.ball_dir + 180.0) % 360.0 - 180.0
			self.ball_ry = 14

		self.ball_dir = (self.ball_dir + 180.0) % 360.0 - 180.0

		if self.ball_rx < -0.5 or self.ball_rx > 64.5:
			if self.ball_rx > 0.0:
				self.p2score += 1
			else:
				self.p1score += 1
			self.ball_dir = -75.0 if self.ball_rx > 0.0 else 75.0
			self.ball_ry = 7.0
			self.ball_rx = 32.0

		self.ball_y = round(self.ball_ry)
		self.ball_x = round(self.ball_rx)

		self.player1_y = min(max(self.controller[0].mouse_y - self.node.from_y, 0), self.height) - (self.platform_width >> 1)
		self.player2_y = self.player1_y
		write(3, 31, f"{self.p1score}:{self.p2score}")

	def onresize(self, height, width):
		self.node.resize(15, 65)
