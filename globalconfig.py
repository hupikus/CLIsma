import os
import sys

from userglobals import userglobals

class Config:

    def __init__(self):

        d = userglobals.userpath + ".local/share/CLIsma/"
        if not os.path.exists(d):
             os.makedirs(d, mode = 0o777)

        #creating missing folders
        for p in ("config/system", "config/carmen", "config/apps/default", "config/apps/external", "custom", "custom/apps/external"):
            n = d + p
            if not os.path.exists(n):
                os.makedirs(n, mode = 0o777)
