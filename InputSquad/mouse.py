import evdev

EV_KEY = 0x01
EV_REL = 0x02

BTN_LEFT = 0x110
BTN_RIGHT = 0x111
BTN_MIDDLE = 0x112

REL_X = 0x00
REL_Y = 0x01

REL_WHEEL = 0x08

class Mice():

	def readevent(self):
		for id in self.devicerange:
			try:
				events = self.devices[id].read()
				self.y[id] = 0
				self.x[id] = 0
				self.wheel[id] = 0
				if events:
					for event in events:
						if event.type == EV_REL:
							if event.code == REL_Y:
			 					self.y[id] = event.value * 0.67
							elif event.code == REL_X:
			 					self.x[id] = event.value
							elif event.code == REL_WHEEL:
			 					self.wheel[id] -= event.value
						elif event.type == EV_KEY:
							if event.code >= BTN_LEFT and event.code <= BTN_MIDDLE:
								self.state[id][event.code - BTN_LEFT] = event.value
			except:
				continue

	def abort(self):
		for dev in self.devices:
			dev.close()

	def __init__(self, devices):
		self.devices = [evdev.InputDevice(device) for device in devices]
		devicelen = len(devices)
		self.devicelen = devicelen

		#cache
		self.devicerange = range(devicelen)
		nir = [0 for i in self.devicerange]

		self.y, self.x = nir[:], nir[:]
		self.wheel = nir[:]
		self.state = [[0, 0, 0] for i in self.devicerange]

		

