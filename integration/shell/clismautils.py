from userglobals import userglobals
import importlib
import os
#standard shell utils

NC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'

def cd(argc, argv):
    pathy = ' '.join(argv[1:])
    if os.path.exists(pathy):
        if os.path.isdir(pathy):
            os.chdir(pathy)
            return True
        else:
            print(f"{pathy}: is not a directory")
            return False
    else:
        print(f"{pathy}: no such file or directory")
        return False

def engrave(argc, argv):
    p = ' '.join(argv[1:])
    print(p)
    return p


def listdir(argc, argv):
    all = 0
    path = './'
    for arg in argv:
        if arg == '-A' or arg == '--almost-all':
            all = 1
        elif arg == '-a' or arg == '--all':
            all = 2
        else:
            if os.path.exists(arg):
                if os.path.isdir(arg):
                    path = arg
                else:
                    print(f"{arg}: is not a folder")

    files = os.listdir(path)
    if all == 2:
        print(BLUE + '.' + NC, end = ' ')
        if os.path.abspath(path) != '/':
            print(BLUE + '..' + NC, end = ' ')

    for file in files:
        if os.path.isdir(file):
            if file[0] == '.':
                if all > 0:
                    print(BLUE + file + NC, end = ' ')
            else:
                print(BLUE + file + NC, end = ' ')
        else:
            if file[0] == '.':
                if all > 0:
                    print(GREEN + file + NC, end = ' ')
            else:
                print(file, end = ' ')
    print()





def desktop(argc, argv):
    os.system(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "main.py"))