import os
import threading
import time

from wm import Wm
from screen import Screen
from inpdevices import DeviceHandler
work = True

def abort(msg):
	global work
	work = False
	draw_thread.join()
	wm.abort()
	display.abort()
	print(msg)
	os.system("exit")

#system
home = os.getenv('HOME')

#screen
screen_height, screen_width = map(int, os.popen('stty size', 'r').read().split())
display = Screen(screen_width, screen_height)

inpd = DeviceHandler()

wm = Wm(display, inpd)


def draw_loop():
	while work:
		error = 0
	
		error += wm.draw()

		error += display.draw()

		if error > 0:
			abort("Display exited with code 1.")

		time.sleep(0.0166)

#main loop
def main_loop():
		l = threading.Lock()
		l.acquire()
		while work:
			time.sleep(0.01)

			error = 0

			wm.process()

			if error > 0:
				abort("Window Manager exited with code 1.")
				break

			if wm.shutdown_ready:
				abort("\nAborted.\n")
				break




try:
	#draw
	draw_thread = threading.Thread(target=draw_loop)
	draw_thread.start()
	#process
	main_loop()
except KeyboardInterrupt:
	abort("\nAborted.\n")
except:
	error_logging = False
	if error_logging:
		#log = open("./error.log", "rw")
		#error = wm.newNode("apps.default", "error", 7, 15, 15, 65)
		#error.text = "Unknown Error"
		#wm.draw()
		abort("Unknown error.")
	else:
		work = False
		error = True
		abort("Unknown error.")
		
