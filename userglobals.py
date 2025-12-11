import os
class userglobals:
	username = os.getenv('SUDO_USER', "!nosudo")
	if username == "!nosudo":
		username = os.getenv('LOGNAME', "unknownUser")

	userpath = os.getenv('SUDO_HOME', "!nosudohome")
	if userpath == "!nosudohome":
		userpath = os.getenv('HOME')
	userpath += '/'
