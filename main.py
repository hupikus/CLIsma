#!/usr/bin/python3
import os
import sys
import threading
import time

debug = False
textmode = False
force = False
version = "1.3"
text_shutdown = False

if not os.path.exists("apps/.CLIsma_system_apps"):
	print("Critical: user is not in CLIsma folder or app folder is not mounted")
	print("cd to CLIsma folder before execution.")
	exit()

#argparse
for i in range(len(sys.argv)):
	arg = sys.argv[i]
	if arg == '-h' or arg == '--help':
		print(f"CLIsma v{version}")
		print("""-------------
Usage:
Insert flags before others to control order of execution
Use -# instead of - for opposite effect: supported commands marked with !
Example: main.py -f       -r testapp -#f              -i /path/to/archive testapp
                 ^force   ^remove    ^disable force   ^install                   : Re-install a package\n
!   -b  --brief                                      Quick common info
!   -d, --debug                                      Debug mode
!   -f, --force                                      Disable confirmation (Warning: force deletion with -r)
    -h, --help                                       Print help message
!   -i, --install {archive_path} {package_name}      Install a package
!   -r, --remove {package_name}                      Remove a package
!   -s, --shell                                      Shell mode (CLIsma shell only)""")
		
		text_shutdown = True
	elif arg in ('-i', '--install', '-#r', '--#remove'):
		text_shutdown = True

		file = ""
		packagename = ""
		if len(sys.argv) > i + 1:
			file = sys.argv[i + 1]
		if len(sys.argv) > i + 2:
			packagename = sys.argv[i + 2]

		import integration.shell.carmen as carmen
		carmen.install_CLI(file, packagename, force)

	elif arg in ('-r', '--remove', '-#i', '--#install'):
		text_shutdown = True

		packagename = ""
		if len(sys.argv) > i + 1:
			packagename = sys.argv[i + 1]

		#wrong or missing arguments
		if packagename == "" or packagename[0] == '-' or packagename[0] == '!':
			print("{package_name} was expected; got " + f"'{packagename}'")
			continue

		import integration.shell.carmen as carmen
		carmen.remove_CLI(packagename, force)

	elif arg == '-d' or arg == '--debug':
		debug = True
	elif arg == '-#d' or arg == '--#debug':
		debug = False

	elif arg == '-f' or arg == '--force':
		force = True
	elif arg == '-#f' or arg == '--#force':
		force = False

	elif arg == "-b" or arg == "--brief":
		print(f"CLIsma v{version}\n-------------")
		print(f"userID: {os.geteuid()}")
		from NodeSquad.appool import AppPool
		appool = AppPool()
		sysApps = 13
		print(f"Apps installed: {len(appool.apps) - sysApps}")
		print(f"System apps: {sysApps}")
		text_shutdown = True
	elif arg == "-#b" or arg == "--#brief":
		from NodeSquad.appool import AppPool
		appool = AppPool()
		import utils.stringmethods as strutils
		sysApps = 13
		print(strutils.getPoem(version, os.geteuid(), sysApps, appool.apps))
		text_shutdown = True
	elif arg == "-s" or arg == "--shell":
		text_shutdown = True
		import integration.shell.shell as shell
		shell.shell()

if text_shutdown:
	exit()

if os.geteuid() != 0:
	print("Critical: no root permissions")
	exit()


from worldglobals import worldglobals
from singletons import Singletons
Singletons.start()


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
	while work:
		error = 0
	
		error += wm.draw()

		error += display.draw()

		if error > 0:
			abort("Display exited with code 1.")

		time.sleep(worldglobals.framedelta)

#main loop
def main_loop():
		l = threading.Lock()
		l.acquire()
		while work:
			time.sleep(worldglobals.processdelta)

			error = 0

			wm.process()

			if error > 0:
				abort("Window Manager exited with code 1.")
				break

			if wm.shutdown_ready:
				abort("\nAborted.\n")
				break
		wm.shutdown()



#draw_thread = threading.Thread(target=draw_loop)
#draw_thread.start()
#main_loop()
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
		#abort("Unknown error.")

