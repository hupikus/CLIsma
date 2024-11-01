from type.inpevents import InputEvents

class Controller:

	def __init__(self, mouse):
		self.mouse = mouse
		self.mouse_dy, self.mouse_dx = (0, 0)
		self.raw_mouse_buttons = [0, 0, 0]
		self.mouse_ry, self.mouse_rx = (0.0, 0.0)
		self.mouse_rdy, self.mouse_rdx = (0, 0)
		self.mouse_y, self.mouse_x = (0, 0)
		self.mouse_last_y, self.mouse_last_x = (0, 0)
		self.mouse_buttons = [0, 0, 0]


		#input types generation
		self.KeyboardEvents = InputEvents("!x000")
		self.MouseEvents = InputEvents("!x001")
	
	def relMousePos(node):
		return self.mouse_y - node.from_y, self.mouse_x - node.from_x