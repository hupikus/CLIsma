from enum import Enum

from type.colors import Colors
from integration.loghandler import Loghandler

class DecorationStyle(Enum):
	classic = 0
	top_only = 1
	all_sides = 2
	top_and_thick_borders = 3
	modern = 4

class DecorationPreset():
	style = None
	func = None

	cornerThick = 1

	def SetStyle(self, style):
		if style in funcs:
			self.style = style
			self.func = funcs[style]

	def Draw(self, wm, node):
		if self.func is not None:
			self.func(self, wm, node)



class Decoration():

	@staticmethod
	def classic(preset, node, wm):
		mode = preset.style
		if node.windowed:

			fx = node.from_x
			tx = node.to_x + 1
			fy = node.from_y
			ty = node.to_y + 1
			width = node.width
			height = node.height
			scrwidth = wm.screen_width
			scrheight = wm.screen_height

			topchar = '─'

			if width > 8:
				text = node.name.center(width, topchar)[:-7] + " - m x "
			elif width > 4:
				text = (topchar * (width - 5)) + " m x "
			else:
				text = "x "

			x_offcut = fx
			mxln = min(scrwidth - x_offcut, width)
			if x_offcut < 0:
				x_offcut *= -1
				wm.display.root.addstr(max(fy - 1, 0), 0, text[x_offcut:mxln])
			else:
				wm.display.root.addnstr(max(fy - 1, 0), x_offcut, text, mxln)

			if mode != DecorationStyle.top_only:
				#bottom decoration
				t = True
				if t and ty < scrheight:
					text = '─' * width # '¯' was used, but not supported in tty somewhy?
					x_offcut = fx
					mxln = min(scrwidth - x_offcut, width)
					if x_offcut < 0:
						x_offcut *= -1
						wm.display.root.addstr(max(ty, 0), 0, text[x_offcut:mxln])
					else:
						wm.display.root.addnstr(max(ty, 0), x_offcut, text, mxln)

				# side decoration
				if mode == DecorationStyle.all_sides:
					left = True
					right = True

					if fx < 1:
						left = False
					if tx> scrwidth - 1:
						right = False

					maxy = scrheight - 1 if ty >= scrheight - 1 else ty

					if left:
						wm.display.root.addstr(fy - 1, fx - 1, '┌')
						if maxy == ty:
							wm.display.root.addstr(ty, fx - 1, '└')
					if right:
						wm.display.root.addstr(fy - 1, tx, '┐')
						if maxy == ty:
							wm.display.root.addstr(ty, tx, '┘')

					y = fy

					while y < maxy:
						if left:
							wm.display.root.addstr(y, fx - 1, '│')
						if right:
							wm.display.root.addstr(y, tx, '│')
						y += 1

funcs = {
		DecorationStyle.classic: Decoration.classic,
		DecorationStyle.top_only: Decoration.classic,
		DecorationStyle.all_sides: Decoration.classic
	}



