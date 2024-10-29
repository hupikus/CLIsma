import sys
import os
import curses

from type.colors import Colors

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
		curses.cbreak()
		#curses.noecho()
		curses.curs_set(0)

		#colors
		curses.start_color()
		curses.use_default_colors()
		if curses.has_colors():
			Colors.define_pairs()

	def draw(self):
		self.root.refresh()
		return 0

	def abort(self):
		self.root.addstr(0, 0, ' ' * self.width)
		self.root.refresh()
		curses.curs_set(2)
		curses.echo()
		#curses.nocbreak()
		self.screen.clear()
		curses.endwin()
		self.srend = []
		os.system("clear")
