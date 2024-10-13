import os
import sys
import evdev
import time

#not an actual code









EV_MSC = 0x04
EV_KEY = 0x01
BTN_MOUSE = 0x100

fast_hexes = {'0':"0000", '1':"0001", '2':"0010", '3':"0011", '4':"0100", '5':"0101", '6':"0110", '7':"0111", '8':"1000", '9':"1001", 'a':"1010", 'b':"1011", 'c':"1100", 'd':"1101", 'e':"1110", 'f':"1111", }


def hex_to_bin(str_hex):
	num = ''
	i = 0
	for c in str_hex:
		if c == '\n':
			pass
		elif c == ' ':
			num = '0' * (16 - i) + num
			i = 0
		else:
			num = fast_hexes[c] + num
			i += 1
	return num


c = True
devnum = 0
mouses = []
while c:
	c = os.path.isfile("/sys/class/input/event" + str(devnum))
	devnum += 1
devnum -= 1
#define avaliable keyboard and mouse and use first two
devnum = 10
for i in range(devnum):
	is_mouse = False
	is_keyboard = False
	poss = open("/sys/class/input/event" + str(i) + "/device/capabilities/ev", 'r')
	capb = hex_to_bin(poss.read())
	if len(capb) >= EV_KEY:
		is_mouse = capb[EV_KEY] == '1'
	#poss = open("/sys/class/input/event" + str(i) + "/device/capabilities/ev", 'r')
	#capb = hex_to_bin(poss.read())
	#if len(capb) > EV_KEY:
	#	is_keyboard = capb[EV_KEY] == '1'
	if is_mouse:
		mouses.append("/dev/input/event" + str(i))
print(mouses)

#devices = map(evdev.InputDevice, mouses)
device = evdev.InputDevice(mouses[0])
#for event in device.read_loop():
#    if event.type == evdev.ecodes.EV_KEY:
#        print(device.active_keys())
while True:
    print(device.active_keys())
    time.sleep(0.7)