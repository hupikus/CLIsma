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
							wm.display.root.addch(fy - 1, fx - 1, '┌')
						if bottom:
							wm.display.root.addch(ty + 1, fx - 1, '└')
					if right:
						if top:
							wm.display.root.addch(fy - 1, tx + 1, '┐')
						if bottom:
							wm.display.root.addch(ty + 1, tx + 1, '┘')

					y = fy if fy >= 0 else 0
					maxy = scrheight if ty + 1 > scrheight else ty + 1

					while y < maxy:
						if left:
							wm.display.root.addch(y, fx - 1, '│')
						if right:
							wm.display.root.addch(y, tx + 1, '│')
						y += 1

	@staticmethod
	def thick(preset, node, wm):
		for y in range(node.from_y, node.to_y):
			wm.display.root.addch(y, node.from_x - 1, ' ', Colors.FXReverse)
			wm.display.root.addch(y, node.to_x, ' ', Colors.FXReverse)
		wm.display.root.addstr(node.from_y - 1, node.from_x - 1, ' ' * (node.width + 2), Colors.FXReverse)
		wm.display.root.addstr(node.to_y, node.from_x - 1, ' ' * (node.width + 2), Colors.FXReverse)



funcs = {
		DecorationStyle.classic: Decoration.classic,
		DecorationStyle.top_only: Decoration.classic,
		DecorationStyle.all_sides: Decoration.classic,
		DecorationStyle.thick: Decoration.thick
	}



