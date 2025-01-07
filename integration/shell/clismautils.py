import importlib
import os
#standard shell utils

def cd(argc, argv):
    pathy = ' '.join(args[1:])
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

def echo(argc, argv):
    p = ' '.join(args[1:])
    print(p)
    return p 


def desktop(argc, argv):
    os.system(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "main.py"))