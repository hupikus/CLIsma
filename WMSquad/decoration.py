from type.colors import Colors
from integration.loghandler import Loghandler

class DecorationStyle():
	classic = 0
	top_only = 1
	all_sides = 2
	top_and_thick_borders = 3
	modern = 4
	thick = 5

class DecorationPreset():
	style = None
	func = None

	edgeThick = (1, 1)
	headThick = 1
	boldTitle = True

	borderAttr = Colors.FXNormal

	topCornerRadius = 2
	bottomCornerRadius = 3

	def SetStyle(self, style): # set standard style
		if style in funcs:
			#styleclass = style.__class__

			#if styleclass is DecorationStyle:
			self.style = style
			self.func = funcs[style]


	def Draw(self, wm, node):
		if self.func is not None:
			self.func(self, wm, node)


class Decoration():

	@staticmethod
	def classic(preset, node, wm):
		mode = preset.style
		attr = preset.borderAttr
		if node.windowed:

			fx = node.from_x
			tx = node.to_x
			fy = node.from_y
			ty = node.to_y
			width = node.width
			height = node.height
			scrwidth = wm.screen_width
			scrheight = wm.screen_height

			addch = wm.display.root.addch


			top = (fy - 1 >= 0)

			bold_title = True

			x_offcut = fx
			mxln = min(scrwidth - x_offcut, width)
			if top:


				if width > 8:
					text = node.name.center(width, '─')[:-7] + " - m x "
				else:
					bold_title = False
					if width > 4:
						text = ('─' * (width - 5)) + " m x "
					else:
						text = "x "

				if x_offcut < 0:
					x_offcut *= -1
					wm.display.root.addstr(max(fy - 1, 0), 0, text[x_offcut:mxln], attr)
				else:
					y = max(fy - 1, 0)
					wm.display.root.addnstr(y, x_offcut, text, mxln, attr)
					if preset.boldTitle and bold_title:
						ln = len(node.name)
						x = x_offcut + (abs(width - ln) >> 1)
						if not ln & 1:
							x += (width & 1)
						if x < scrwidth: #Name attr
							wm.display.root.chgat(y, x, min(ln, width, scrwidth - x), Colors.FXBold)

			if mode != DecorationStyle.top_only:
				bottom = (ty + 1 < scrheight)
				#bottom decoration
				if bottom:
					text = '─' * width
					x_offcut = fx
					if x_offcut < 0:
						x_offcut *= -1
						wm.display.root.addstr(max(ty + 1, 0), 0, text[x_offcut:mxln], attr)
					else:
						wm.display.root.addnstr(max(ty + 1, 0), x_offcut, text, mxln, attr)

				# side decoration
				if mode == DecorationStyle.all_sides:
					left = (fx - 1 >= 0)
					right = (tx + 1 < scrwidth)

					if left:
						if top:
							addch(fy - 1, fx - 1, '┌')
						if bottom:
							addch(ty + 1, fx - 1, '└')
					if right:
						if top:
							addch(fy - 1, tx + 1, '┐')
						if bottom:
							addch(ty + 1, tx + 1, '┘')

					y = fy if fy >= 0 else 0
					maxy = scrheight if ty + 1 > scrheight else ty + 1

					while y < maxy:
						if left:
							addch(y, fx - 1, '│')
						if right:
							addch(y, tx + 1, '│')
						y += 1

	@staticmethod
	def thick(preset, node, wm):
		display = wm.display
		addch = display.root.addch
		addstr = display.root.addstr
		left = node.from_x - 2
		right = display.width - 1 - (node.to_x + 2)
		for y in range(max(0, node.from_y - 1), min(display.height, node.to_y + 2)):
			if left >= -1:
				addch(y, node.from_x - 1, ' ', Colors.FXReverse)
			if right >= -1:
				addch(y, node.to_x + 1, ' ', Colors.FXReverse)
			if left >= 0:
				addch(y, node.from_x - 2, ' ', Colors.FXReverse)
			if right >= 0:
				addch(y, node.to_x + 2, ' ', Colors.FXReverse)

		startx = max(0, node.from_x - 1)
		endx = min(display.width, node.from_x - 1 + node.width + 2)
		if node.from_y - 1 >= 0:
			addstr(node.from_y - 1, startx, ' ' * (endx - startx), Colors.FXReverse)
		if node.to_y + 1 < display.height:
			addstr(node.to_y + 1, startx, node.name.center(endx - startx, ' '), Colors.FXReverse)
			if (endx - startx) > 5:
				addstr(node.to_y + 1, node.to_x - 7, '- m x')



funcs = {
		DecorationStyle.classic: Decoration.classic,
		DecorationStyle.top_only: Decoration.classic,
		DecorationStyle.all_sides: Decoration.classic,
		DecorationStyle.thick: Decoration.thick
	}



