import os
import sys

from userglobals import userglobals

class Config:

    def __init__(self):

        prep = os.path.exists(userglobals.userpath + ".local/share/CLIsma")
        d = userglobals.userpath + ".local/share/CLIsma/"

        #creating missing folders
        for p in ("config/system", "config/carmen", "config/default/desktop", "custom", "custom/apps"):
            n = d + p
            if not os.path.exists(n):
                os.makedirs(n, mode = 0o777)
                
                #custom
                if p == "custom/apps":
                    os.system(f"ln -s {d + "custom/apps"} ./apps/external")
                elif p == "custom":
                    sys.path.append(d + "custom")

        if not prep:
            os.system("chmod 777 " + d + " -R")