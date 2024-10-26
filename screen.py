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
		self.root.refresh()

	def abort(self):
		self.root.move(0, 0)
		self.root.addstr(0, 0, ' ' * self.width)
		curses.curs_set(1)
		self.screen.clear()
		curses.echo()
		curses.endwin()
		self.srend = []
		os.system("clear")
