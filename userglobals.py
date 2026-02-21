import os
import pathlib

class userglobals:
	username = os.getenv('SUDO_USER', "!nosudo")
	if username == "!nosudo":
		username = os.getenv('LOGNAME', "UnknownUser")

	# Should i switch to Path objects????
	userpath = str(pathlib.Path.home()) + '/'
	configfolder = os.getenv("XDG_DATA_HOME", userpath + ".local/share/CLIsma/")
