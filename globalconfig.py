import os
import sys

from userglobals import userglobals

class Config:

    def __init__(self):

        prep = os.path.exists(userglobals.userpath + ".local/share/CLIsma")

        if not prep:
            os.makedirs(userglobals.userpath + ".local/share/CLIsma/config/default/desktop", mode = 0o747)
            os.mkdir(userglobals.userpath + ".local/share/CLIsma/config/system", mode = 0o747)


            os.makedirs(userglobals.userpath + ".local/share/CLIsma/custom/apps", mode = 0o747)
            
            sys.path.append(userglobals.userpath + ".local/share/CLIsma/custom")