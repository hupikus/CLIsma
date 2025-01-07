import os
import sys

from userglobals import userglobals

class Config:

    def __init__(self):

        prep = os.path.exists(userglobals.userpath + ".local/share/CLIsma")

        if not prep:
            os.makedirs(userglobals.userpath + ".local/share/CLIsma/config/default/desktop", mode = 0o777)
            os.mkdir(userglobals.userpath + ".local/share/CLIsma/config/system", mode = 0o777)


            os.makedirs(userglobals.userpath + ".local/share/CLIsma/custom/apps", mode = 0o777)
            
            sys.path.append(userglobals.userpath + ".local/share/CLIsma/custom")
            os.system("chmod 777 " + userglobals.userpath +".local/share/CLIsma/ -R")