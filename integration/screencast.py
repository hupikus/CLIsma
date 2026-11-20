import curses

from integration.loghandler import Loghandler

MAX_CHAR_SIZE = 4

class Screencast:

	@staticmethod
	def RenderFrame(display):
		Loghandler.Log("I BEGEG")
		for func_id, listeners in enumerate(Screencast.listeners):
			for listener in listeners:
				listener(str(display.record_data))

	@staticmethod
	def CaptureScreen(listener, display, y = 0, x = 0, height = 0, width = 0, color = True):
		if not callable(listener): return
		scr_height = display.height
		scr_width = display.width

		if (height == 0 and width == 0):
			y = 0
			x = 0
			height = scr_height
			width = scr_width
		else:
			y = max(0, min(scr_height - 1, y))
			x = max(0, min(scr_width - 1, x))

			scr_height = max(1, min(scr_height - y, scr_height))
			scr_height = max(1, min(scr_width - x, scr_width))
		
		func_id = 0
		if color:
			func_id = 1
		Screencast.listeners[func_id].append(listener)

		display.RecordFrame(Screencast.funcs[func_id], y, x, height, width)

	@staticmethod
	def CaptureScreenPlain(display):
		with display.lock:
			y = display.record_y
			x = display.record_x
			height = display.record_h
			width = display.record_w
			

	@staticmethod
	def CaptureScreenAttr(display):
		return CaptureScreenPlain(display, y, x, height, width)

	funcs = [CaptureScreenPlain, CaptureScreenAttr]
	listeners = [[], []]
