import sys
import os
import curses
import shutil
import tty
import termios
import threading

from integration.loghandler import Loghandler
from type.colors import Colors

class Screen():

	def __init__(self, forceColor):

		self.lock = threading.Lock()

		siz = shutil.get_terminal_size()

		self.height = siz[1]
		self.width = siz[0]

		self.resize_wm_signal = False


		# Handle special terminals before starting curses, because curses relies solely on the environment variable rather than on the actual capabilities

		colorterm = os.environ.get("COLORTERM")

		if colorterm == "kmscon":
			os.environ["TERM"] = "xterm"

		# Preparation
		self.screen = curses.initscr()


		# ASCII screen
		self.root = curses.newwin(self.height + 1, self.width, 0, 0)

		# Save props
		self.fd = sys.stdin.fileno()
		self.old_config = termios.tcgetattr(self.fd)

		# Set up the env
		tty.setraw(self.fd)
		self.root.nodelay(1)
		curses.cbreak()
		curses.noecho()
		try:
			curses.curs_set(0)
		except:
			pass

		# Colors
		Colors.start_color(forceColor)
		if Colors.colorPosibility: #curses.has_colors():
			Colors.define_pairs()

		#curses.nonl()
		#curses.def_shell_mode()

		self.record = False
		self.record_y = 0
		self.record_x = 0
		self.record_h = 0
		self.record_w = 0
		self.record_data = [[0, 0]] * self.height * self.width

		self.record_listener = None

	def RecordFrame(self, listener, y, x, height, width):
		self.record_listener = listener
		self.record_y = y
		self.record_x = x
		self.record_h = height
		self.record_w = width

		self.record = True

	def draw(self):
		#sys.stdout.write("\033[0m")
		self.root.refresh()
		siz = shutil.get_terminal_size()
		if self.height != siz[1] or self.width != siz[0]:
			self.height = siz[1]
			self.width = siz[0]
			self.root.resize(self.height + 1, self.width)
			self.resize_wm_signal = True

		if self.record:
			self.record_listener(self)
			self.record = False
		return 0

	def abort(self):
		self.root.addstr(0, 0, ' ' * self.width)
		#curses.curs_set(2)
		#curses.echo()
		#curses.nocbreak()
		self.root.erase() # Or clear(), it does not matter as it does not work

		# Restore
		termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_config)


		self.screen.refresh()
		self.root.refresh()
		#curses.reset_shell_mode()
		curses.flushinp()
		curses.endwin()

		self.srend = []
		os.system("clear")

	def getColorPair(self, y, x):
		return self.root.inch(y, x) & curses.A_ATTRIBUTES

	def getChar(self, y, x):
		ch = self.root.inch(y, x) & 0xFF
		if ch == 0: return ''
		return bytes([ch])
