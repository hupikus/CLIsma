import integration.shell.clismautils as utils
import os
import importlib

base = ("clear", "bash", "sh", "ls", "python", "mkdir", "rmdir", "rm", "touch", "cat",
        "mv", "head", "tail", "stat", "df", "kill", "uptime", "shutdown", "reboot",
        "wc", "ping", "ip", "ps", "dd", "uname", "who", "passwd", "tar", "man",
        "pwd", "ln", "du", "readlink", "basename", "dirname", "tac", "chmod", "chown", "chgrp",
        "yes", "cmp", "diff", "comm", "uniq", "whoami", "groups", "true", "false", "tee",
        "shuf", "stty", "tty", "sort", "cut", "tr", "nl", "wc", "split", "csplit")
modules = {"utils" : utils}

def shell(root):
    prefix = '#' if root else '$'
    while True:
        #try:
        command = input(f"{os.path.basename(os.getcwd())} {prefix}> ")
        commands = [command]
        if '&&' in command:
            commands = command.split("&&")
        for exe in commands:
            if exe == "exit": exit()
            args = exe.split()
    #        try:
            execute(len(args), args)
    #        except:
    #            print("Execution failed.")
        #except:
        #    exit()

def run(args):
    shell(os.geteuid() == 0)


def execute(argc, args):
    name = args[0]
    if name in base:
        return os.system(' '.join(args))
    if name == "shell":
        run(args)
    if name == "reload":
            if argc > 1:
                module = args[1]
                if module in modules:
                    importlib.reload(modules[module])
                else:
                    try:
                        modules[module] = importlib.import_module("integration.shell." + module)
                    except ModuleNotFoundError:
                        print(f"{module}: module not found")
                        return False
            else:
                print("Specify a module to reload.")
    else:
        try:
            modules[name] = importlib.import_module("integration.shell." + name)
            return modules[name].run(argc, args)
        except ModuleNotFoundError:
            found = True
            if hasattr(utils, name):
                function = getattr(utils, name)
                if callable(function):
                    return function(argc, args)
                else:
                    found = False
            else:
                
                found = False
            if not found:
                if os.path.exists(name):
                    found = True
                    return os.system(' '.join(args))
                else:
                    found = False
            if not found:
                print(f"Shell: {name}: command not found")
