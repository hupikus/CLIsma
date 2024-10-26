import sys
import os
import curses


class Screen():

	def __init__(self, width, height):
		self.width = width
		self.height = height

		#preparation
		self.screen = curses.initscr()


		#ASCII screen
		self.root = curses.newwin(self.height, self.width, 0, 0)
		#self.srend = [[' ' for x in range(self.width)] for y in range(self.height)]

		#set up the env
		self.root.nodelay(1)
		curses.curs_set(0)


	def draw(self):
#		for y in range(self.height - 1):
#			self.root.move(y, 0)
#
#			try:
#				self.root.addstr(''.join(self.srend[y]))
#			except curses.error:
#				pass

		self.root.refresh()
		return 0


	def abort(self):
		self.root.move(0, 0)
		self.root.addstr(0, 0, ' ' * self.width)
		curses.curs_set(1)
		self.screen.clear()
		curses.echo()
		curses.endwin()
		self.srend = []
		os.system("clear")
