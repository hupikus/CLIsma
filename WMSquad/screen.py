import sys
import os
import curses
import shutil

from type.colors import Colors

class Screen():

	def __init__(self, forceColor):

		siz = shutil.get_terminal_size()

		self.height = siz[1]
		self.width = siz[0]

		self.resize_wm_signal = False


		#preparation
		self.screen = curses.initscr()


		#ASCII screen
		self.root = curses.newwin(self.height + 1, self.width, 0, 0)

		#set up the env
		self.root.nodelay(1)
		curses.cbreak()
		curses.noecho()
		curses.curs_set(0)

		#colors
		Colors.start_color(forceColor)
		if curses.has_colors():
			Colors.define_pairs()

		#curses.nonl()
		#curses.def_shell_mode()

	def draw(self):
		#sys.stdout.write("\033[0m")
		self.root.refresh()
		siz = shutil.get_terminal_size()
		if self.height != siz[1] or self.width != siz[0]:
			self.height = siz[1]
			self.width = siz[0]
			self.root.resize(self.height + 1, self.width)
			self.resize_wm_signal = True
		return 0

	def abort(self):
		self.root.addstr(0, 0, ' ' * self.width)
		curses.curs_set(2)
		curses.echo()
		curses.nocbreak()
		self.root.erase() # or clear(), it does not matter as it not work
		self.screen.refresh()
		self.root.refresh()
		#curses.reset_shell_mode()
		curses.endwin()

		self.srend = []
		os.system("clear")

	def getColorPair(self, y, x):
		return self.root.inch(y, x) & curses.A_ATTRIBUTES

	def getChar(self, y, x):
		ch = self.root.inch(y, x) & 0xFF
		if ch == 0: return ''
		return bytes([ch])
