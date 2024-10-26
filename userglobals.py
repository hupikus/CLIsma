import os
class userglobals:
    username = os.getenv('SUDO_USER', "!nosudo")
    if username == "!nosudo":
        username = os.getenv('LOGNAME')