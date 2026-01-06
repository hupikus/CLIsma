#!/usr/bin/python3
import os
import sys
import threading
import time

debug = False
desktop = "default"
textmode = False
force = False
forceColor = False
version = "1.9"
skip_desktop = False

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)
if not os.path.exists("apps/default"):
	if not os.path.exists("empty"):
		print("Critical: default apps are deleted. Proceed if you want an empty WM or fix the installation.")
		resp = input("Proceed? (y/n) ").lower()
		if resp != 'y': exit()
		with open('empty', 'w') as f:
			pass

#argparse
for i in range(len(sys.argv)):
	arg = sys.argv[i]
	if arg == '-h' or arg == '--help':
		print(f"CLIsma v{version}")
		print("""-------------
Usage: main.py --flag1 {required1} (optional2) --flag2 ...
Run main.py without parameters to run desktop
Сontrol order of execution by rearranging flags order
Use -# instead of - for the opposite effect: supported commands marked with !
Example: main.py -f       -r testapp -#f              -i /path/to/archive testapp
                 ^force   ^remove    ^disable force   ^install                   : Re-install a package\n
!   -b  --brief                                      Quick common info
!   -d, --debug                                      Debug mode
    -D, --desktop {package_name}                     Launch CLIsma with custom desktop app
!   -f, --force                                      Disable confirmation (Warning: force deletion with -r)
    -h, --help                                       Print help message
!   -i, --install {package_name} (archive_path)      Install a package
!   -r, --remove {package_name}                      Remove a package
!   -s, --shell                                      Shell mode (CLIsma shell only)
    -l, --low-color                                  Low color mode""")

		skip_desktop = True
	elif arg in ('-i', '--install', '-#r', '--#remove'):
		skip_desktop = True

		packagename = ""
		file = ""
		if len(sys.argv) > i + 1:
			packagename = sys.argv[i + 1]
		if len(sys.argv) > i + 2:
			file = sys.argv[i + 2]

		import integration.shell.carmen as carmen
		carmen.install_CLI(packagename, file, force)

	elif arg in ('-r', '--remove', '-#i', '--#install'):
		skip_desktop = True

		packagename = ""
		if len(sys.argv) > i + 1:
			packagename = sys.argv[i + 1]

		#wrong or missing arguments
		if packagename == "" or packagename[0] == '-' or packagename[0] == '!':
			print("{package_name} was expected; got " + f"'{packagename}'")
			continue

		import integration.shell.carmen as carmen
		from globalconfig import Config
		Cfg = Config()
		carmen.remove_CLI(packagename, force)

	elif arg == '-d' or arg == '--debug':
		debug = True
	elif arg == '-#d' or arg == '--#debug':
		debug = False

	elif arg == '-f' or arg == '--force':
		force = True
	elif arg == '-#f' or arg == '--#force':
		force = False

	elif arg == '-l' or arg == '--low-color':
		forceColor = True

	elif arg == "-b" or arg == "--brief":
		print(f"CLIsma v{version}\n-------------")
		print(f"userID: {os.geteuid()}")
		from NodeSquad.appool import AppPool
		appool = AppPool()
		sysApps = 12
		print(f"Apps installed: {len(appool.apps) - sysApps}")
		print(f"System apps: {sysApps}")
		skip_desktop = True
	elif arg == "-#b" or arg == "--#brief":
		from NodeSquad.appool import AppPool
		appool = AppPool()
		import utils.stringmethods as strutils
		sysApps = 12
		print(strutils.getPoem(version, os.geteuid(), sysApps, appool.apps))
		skip_desktop = True
	elif arg == "-s" or arg == "--shell":
		skip_desktop = True
		import integration.shell.shell as shell
		from globalconfig import Config
		Cfg = Config()
		shell.shell()
	elif arg == "-D" or arg == "--desktop":
		if len(sys.argv) > i + 1:
			v = sys.argv[i + 1]
			desktop = sys.argv[i + 1]

if skip_desktop:
	exit()

if not os.access("/dev/input/event0", os.R_OK):
	print("Critical: don't have access to /dev/input")
	time.sleep(0.5)
	


from worldglobals import worldglobals
from singletons import Singletons
Singletons.start(forceColor, desktop)


work = True


import apps.apphabit

def abort(msg):
	global work
	work = False
	draw_thread.join()
	Singletons.Inpd.abort()
	display.abort()
	print(msg)
	exit()

wm = Singletons.Wm

display = Singletons.Screenman


def draw_loop():
	timestamp = time.time()
	deltaTime = 0
	while work:
		error = 0

		error += wm.draw(deltaTime)

		error += display.draw()

		if error > 0:
			abort(f"Display exited with code {error}.")

		deltaTime = time.time() - timestamp
		timestamp += deltaTime

		t = worldglobals.framedelta
		if deltaTime > t:
			t = t * 2 - deltaTime
			if t < 0:
				t = 0
		time.sleep(t)


#main loop
def main_loop():

	timestamp = time.time()
	deltaTime = 0
	while work:
		error = 0

		wm.process(deltaTime)

		if error > 0:
			abort(f"Window Manager exited with code {error}.")
			break

		if wm.shutdown_ready:
			abort("\nAborted.\n")
			break

		deltaTime = time.time() - timestamp
		timestamp += deltaTime


		t = worldglobals.processdelta
		if deltaTime > t:
			t = t * 2 - deltaTime
			if t < 0:
				t = 0
		time.sleep(t)

	wm.shutdown()



# draw_thread = threading.Thread(target=draw_loop)
# draw_thread.start()
# main_loop()
try:
	#draw
	draw_thread = threading.Thread(target=draw_loop)
	draw_thread.start()
	#process
	main_loop()
except KeyboardInterrupt:
	work = False
	abort("\nAborted.\n")
except:
	work = False
	error = True
	abort("Unknown error.")

