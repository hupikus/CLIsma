from type.inpevents import InputEvents

class Controller:

	def __init__(self, mouse):
		self.mouse = mouse
		self.mouse_x, self.mouse_y = (0, 0)
		self.mouse_buttons = [0, 0, 0]
		if self.mouse == 0:
			self.mode = "kbrd"
		else:
			self.mode = "full"


		#input types generation
		self.KeyboardEvents = InputEvents("!x000")
		self.MouseEvents = InputEvents("!x001")
