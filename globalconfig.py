import os
import sys

from userglobals import userglobals

class Config:

    def __init__(self):

        d = userglobals.userpath + ".local/share/CLIsma/"
        prep = os.path.exists(d)
        if not prep:
             os.makedirs(d, mode = 0o777)

        #creating missing folders
        for p in ("config/system", "config/carmen", "config/apps/default", "config/apps/external", "custom", "custom/apps/external"):
            n = d + p
            if not os.path.exists(n):
                os.makedirs(n, mode = 0o777)

                #custom
                if p == "custom/apps/external":
                    os.system(f"ln -s {d}custom/apps ./apps/external")

        if not prep:
            os.system("chmod 777 " + d + " -R")
