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

#argparse
for i in range(len(sys.argv)):
	arg = sys.argv[i]
	if arg == '-h' or arg == '--help':
		print()
		print(f"CLIsma v{version}\n-------------")
		print()
		print("Usage:")
		print("Insert flags before others to control order of execution")
		print("Use -# instead of - for opposite effect: supported commands marked with !")
		print("Example: main.py -f       -r testapp -#f              -i /path/to/archive testapp")
		print("                 ^force   ^remove    ^disable force   ^install                   : Re-install a package")
		print()
		print("!   -b  --brief                                      Quick common info")
		print("!   -d, --debug                                      Debug mode")
		print("!   -f, --force                                      Disable confirmation (Warning: force deletion with -r)")
		print("!   -h, --help                                       Print help message")
		print("!   -i, --install {archive_path} {package_name}      Install a package")
		print("!   -r, --remove {package_name}                      Remove a package")
		print("!   -s, --shell                                      Text mode (CLIsma shell only) !TODO")
		
		text_shutdown = True
	elif arg in ('-i', '--install', '-#r', '--#remove'):
		text_shutdown = true
		from userglobals import userglobals
		import zipfile
		from globalconfig import Config
		cfg = Config()


		file = ""
		packagename = ""
		if len(sys.argv) > i + 1:
			file = sys.argv[i + 1]
		if len(sys.argv) > i + 2:
			packagename = sys.argv[i + 2]

		#wrong or missing arguments
		if file == "" or file[0] == '-' or file[0] == '!':
			print("{archive_path} was expected; got " + f"'{file}'")
			continue
		if packagename == "" or packagename[0] == '-' or packagename[0] == '-':
			print("{package_name} was expected; got " + f"'{packagename}'")
			continue

		#file check
		if os.path.exists(file):
			print("Analysing containtment...")
			if zipfile.is_zipfile(file):
				with zipfile.ZipFile(file, 'r') as archive:
					zip_files = [file for file in archive.namelist() if '/' not in file]
					print(f"{len(zip_files)} files in root folder.")
					if len(zip_files) > 0:

						#required files are missing
						if ".app" not in zip_files:
							print("Required file missing: .app")
							continue
						elif "icon.asc" not in zip_files:
							print("App icon may be missing.")

						#entry file not found
						if packagename + ".py" not in zip_files:
							import utils.stringmethods as strutils
							similarname = strutils.closest(packagename + ".py", (i for i in zip_files if len(i) >= 4 and i[-3:] == ".py"))
							print(f'Entry file {packagename}.py is missing. Did you mean "{similarname[:-3]}"?')
							continue

						#package already exists
						if os.path.exists(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename):
							ans = 'y'
							if not force:
								ans = input("Package with that name already exist. Proceed? (y/n)")
							if ans != 'y': continue

						#installing
						try:
							os.makedirs(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename, mode = 0o764)
							print("Unpacking...")
							archive.extractall(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename)
							print("Creating config...")
							os.makedirs(userglobals.userpath + ".local/share/CLIsma/config/apps/" + packagename, mode = 0o777)
							config_path = userglobals.userpath + ".local/share/CLIsma/config/apps/" + packagename + '/main.conf'
							if os.path.exists(config_path):
								print("Warning: config file for this app existed before.")
							else:
								open(config_path, 'w').close()
							print(f"Package {packagename} was succesfully installed.")
						except:
							print("Unknown error has ocurred during the installation.")
							continue
					else:
						print("Maybe, archive is nested or empty.")
			else:
				print("Specified file is not a ZIP archive.")
		else:
			print("Specified file does not exists.")
	elif arg in ('-r', '--remove', '-#i', '--#install'):
		text_shutdown = true
		from userglobals import userglobals
		packagename = ""
		if len(sys.argv) > i + 1:
			packagename = sys.argv[i + 1]

		#wrong or missing arguments
		if packagename == "" or packagename[0] == '-' or packagename[0] == '!':
			print("{package_name} was expected; got " + f"'{packagename}'")
			continue
		
		import shutil

		package_path = userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename

		if os.path.exists(package_path):
			print("Package found")
			ans = 'y'
			if not force:
				ans = input("Proceed? (y/n)")
			if ans != 'y':
				print("Cancelled.")
				continue
		else:
			from NodeSquad.appool import AppPool
			appool = AppPool()
			packagelist = appool.apps
			if len(appool.apps) > 0:
				import utils.stringmethods as strutils
				similarname = strutils.closest(packagename + ".py", packagelist)
				print(f"Error: package not found. Did you mean '{similarname}'?")
			else:
				print(f"Error: package not found.")
			continue

		config_path = userglobals.userpath + ".local/share/CLIsma/config/apps/" + packagename
		if os.path.exists(config_path):
			ans = 'y'
			if not force:
				ans = input("Remove config? (y/n)")
			if ans == 'y':
				try:
					shutil.rmtree(config_path)
					print("Config removed")
				except:
					print("Failed.")
		
		
		print("Removing package...")
		try:
			shutil.rmtree(package_path)
			print(f"Done removing '{packagename}'")
		except:
			print("Removal failed. Did you granted root permissions?")

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
		sysApps = 12
		print(f"Apps installed: {len(appool.apps) - sysApps}")
		print(f"System apps: {sysApps}")
		text_shutdown = True
	elif arg == "-#b" or arg == "--brief":
		from NodeSquad.appool import AppPool
		appool = AppPool()
		import utils.stringmethods as strutils
		sysApps = 12
		print(strutils.getPoem(version, os.geteuid(), sysApps, appool.apps))
		text_shutdown = True

if text_shutdown:
	exit()

if not os.path.exists("apps/.CLIsma_system_apps"):
	print("Critical: user is not in CLIsma folder or app folder is not mounted")
	print("cd to CLIsma folder before execution.")
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

