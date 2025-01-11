import integration.shell.clismautils as utils
from userglobals import userglobals
import utils.stringmethods as strutils
import subprocess
import importlib

import threading
import time

import os
import sys
import termios
import tty

running = True
update_interval = 1.0 / 120.0

INVERSE = '\x1b[7m'
REVERT = '\x1b[0m'

term = os.getenv('TERM', 'xterm')

modules = {"utils" : utils}
vars = {
    "PATH" : ["/bin/", os.path.join(userglobals.userpath, ".local/bin/"), "/usr/bin/", "/usr/local/bin/"],
    "HISTORY_LEN" : 1000
    }

path = vars["PATH"]

aliases = {"ls" : "ls --color=always"}
vars["alias"] = aliases

echoing = True
chmod = False

buffer = ""
last_getch = ''



history = [""]


#redefine 'print' to include returning caret
import builtins

prev_print = builtins.print

def raw_print(*args, **kwargs):
    if 'end' not in kwargs:
        kwargs['end'] = '\r\n'
    prev_print(*args, **kwargs)

builtins.print = raw_print


def ever_getch():
    global buffer
    global last_getch
    global echoing
    global chmod


    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    #prefs
    tty.setraw(fd)
    print('\x1b[?25l', end = '', flush = True) #hide cursor
    #fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)

    while running:
        is_escape = False
        try:
            r = sys.stdin.read(1)
        except:
            print("\x1b[?25h\r") #show cursor
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            exit()
 
        if r != '':
            last_getch = r
            if last_getch == '\x1b':  # Escape character
                is_escape = True
                n = sys.stdin.read(1)
                if n == '[':
                    last_getch += n + sys.stdin.read(1)
                else:
                    last_getch += n
            else:
                od = ord(last_getch)
                if od > 0x7F:                       #multi-byte character
                    if 0xC0 <= od <= 0xDF:              #2-byte character
                        last_getch += sys.stdin.read(1)
                    elif 0xE0 <= od <= 0xEF:            #3-byte character
                        last_getch += sys.stdin.read(2)
                    elif 0xF0 <= od <= 0xF7:            #4-byte character
                        last_getch += sys.stdin.read(3)
        r = ''
                


def shell():
    global buffer
    global last_getch
    global echoing
    global history

    history_pos = 0
    cursor = 0

    prefix = '#' if os.geteuid() == 0 else '$'
    print(f"{os.path.basename(os.getcwd())} {prefix}> ", end = '', flush = True)


    getch_thread = threading.Thread(target=ever_getch)
    getch_thread.start()
    while True:
        #try:
        #check for charactersc
        match (last_getch):
            case '':
                pass
            case '\t':
                #autocomplete
                if cursor > 0:
                    sea = strutils.extract_word(buffer, cursor - 1)
                    if sea != '':
                        res = search(sea)
                        lr = len(res)
                        if lr == 0: pass
                        elif lr == 1:
                            history[-1] = history[-1][:cursor] + res[0] + history[-1][cursor:]
                            cursor += len(res[0])
                        elif lr < 21:
                            print('\r' + ' '.join(res), end = '\n\r', flush = True)
                        else:
                            print(f"\r{lr} matches")
                    
            case '\n' | '\r':
                print(f"\r{'\x1b[2K'}{os.path.basename(os.getcwd())} {prefix}> {buffer}\r")
                #command = input(f"{os.path.basename(os.getcwd())} {prefix}> ")
                buffer = buffer.strip()
                if buffer == "":
                    last_getch = ''
                    continue
                commands = [buffer[:]]
                buffer = ""

                #history
                history.append("")
                history_pos = -1
                cursor = 0


                while len(history) > vars["HISTORY_LEN"]:
                    history.pop(0)


                if '&&' in commands[0]:
                    commands = command.split("&&")
                for exe in commands:
                    #emergency
                    if exe == "exit":
                        running = False
                        print("\rPress any key...\r")
                        exit()

                    #parse vars and etc
                    args = parse_shell_args(exe)

                    if not args:
                        continue

                    #try:
                    proc = execute(len(args), args)
                    if isinstance(proc, subprocess.Popen):
                        proc.wait()
                        #while True:

                        #for line in iter(proc.stdout.readline, b''):
                        #    print(line.decode(), end = '\n\r', flush = True)
                        #stdout, stderr = proc.communicate()
                        #print(stdout.decode(), end = '\n\r')
                    process = False


                    print('\r', end = '')
                    #print(f"{os.path.basename(os.getcwd())} {prefix}>", end = ' ', flush = True)
                    #except:
                    #print("Execution failed.")

            case '\x1b[A': #Up arrow
                history_pos = max(history_pos - 1, -len(history))
                history[-1] = history[history_pos][:]
                cursor = len(history[-1])
            case '\x1b[B': #Down arrow
                if history_pos == -2:
                    history[-1] = ""
                    history_pos = -1
                    cursor = 0
                else:
                    history_pos = min(history_pos + 1, -1)
                    history[-1] = history[history_pos][:]
                    cursor = len(history[-1])
            case '\x1b[D': #Left arrow
                history_pos = -1
                cursor = max(0, cursor - 1)
            case '\x1b[C': #Right arrow
                history_pos = -1
                cursor = min(len(buffer), cursor + 1)
            case '\x7f': #Backspace
                history_pos = -1
                if cursor > 0:
                    history[-1] = history[-1][:cursor - 1] + history[-1][cursor:]
                    cursor -= 1
            case _:
                #any character
                if chmod:
                    history[-1] = last_getch
                else:
                    history[-1] = history[-1][:cursor] + last_getch + history[-1][cursor:]
                    cursor += 1
                #print(last_getch, end = '', flush = True)
                history_pos = -1
        buffer = history[-1]

        #'cursor symbol is cursor - 1, but cursor should be drawn at cursor'
        if len(buffer) > cursor:
            print(f"\r{'\x1b[2K'}{os.path.basename(os.getcwd())} {prefix}> {buffer[:cursor]}{INVERSE}{buffer[cursor]}{REVERT}{buffer[cursor + 1:]}", end = '', flush = True)
        else:
            print(f"\r{'\x1b[2K'}{os.path.basename(os.getcwd())} {prefix}> {buffer}{INVERSE} {REVERT}", end = '', flush = True)

                    
        #clear
        last_getch = ''
        time.sleep(update_interval)

        #except:
        #    exit()
        


def run(args):
    shell()


def execute(argc, args):
    name = args[0]

    #search order
        #first: emergency commands (e.g. exit)
        #second: clismautils
        #third: PATH
        #fourth: modules
        #fifth: ./
    

    #assign
    if "=" in name:
        i = name.index('=')
        key = name[:i]
        if key == "alias":
            print("'alias' is set to read-only. Use 'alias cmd=some cool command' instead.")
            return False
        if key == "PATH":
            print("'PATH' is set to read-only. Use 'bpath' instead.")
            return False

        val =  kvar(name[i + 1:] + ' ' + ' '.join(args[1:]))

        vars[key] = val
        return val

    match name:

        case "shell":
            run(args)
        case "alias":
            if argc < 2:
                print("Specify an alias.")
                return False
            n = ' '.join(args[1:])

            if "=" in n:
                i = n.index('=')
                val = n[i + 1:]

                aliases[n[:i]] = val
                if n[:i] == val:
                    del aliases[n[:i]]
                return val
        case "bpath":
            if argc == 1:
                print("Help\n  -a, --add           Add to the PATH\n  -r, --remove        Remove from the PATH\n  -h, --help          Print Help message")
            elif argc == 2:
                if args[1] == '-h' or args[1] == '--help':
                    print("Help\n  -a, --add           Add to the PATH\n  -r, --remove        Remove from the PATH\n  -h, --help          Print Help message")
                else:
                    path.append(args[1])
            elif argc == 3:
                if args[1] == '-a' or args[1] == '--add':
                    path.append(args[2])
                elif args[1] == '-r' or args[1] == '--remove':
                    path.append(args[2])
            else:
                print("Wrong arguments.")
        case "reload":
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
        case "vars":
            print(vars)
            return True
        case _:
            #alias
            alias_replace(args)
            name = args[0]
            #clismautils
            if hasattr(utils, name):
                function = getattr(utils, name)
                if callable(function):
                    return function(argc, args)

            #PATH
            for bin in path:
                if os.path.exists(bin + name):
                    args[0] = bin + args[0]
                    return subprocess.Popen(args, stdin = None, stdout = None, stderr = None, env={"TERM":  term})
                    #return os.system(' '.join(args))
    
            try:
                #modules
                modules[name] = importlib.import_module("integration.shell." + name)
                return modules[name].run(argc, args)
            except ModuleNotFoundError:
                #./
                if os.path.exists(name):
                    return os.system(' '.join(args))
                else:
                    print(f"Shell: {name}: command not found")



def parse_shell_args(argt):
    args = []
    buffer = ''
    quote_depth = False
    bracket_depth = 0
    for i in argt:
        match i:
            case ' ':
                if not quote_depth:
                    #vars
                    args.append(kvar(buffer))
                    buffer = ''
            case '"':
                quote_depth = not quote_depth
            case '(':
                if not quote_depth:
                    bracket_depth += 1
                buffer += i
            case ')':
                if not quote_depth:
                    bracket_depth -= 1
                    if bracket_depth < 0:
                        print("')': wrong syntax")
                        return False
                buffer += i
            case _:
                buffer += i

    if buffer != '' and buffer != ' ':
        args.append(kvar(buffer.strip()))
    return args


def kvar(key):
    c = len(key)
    if key[0] == '%' and key[-1] == '%':
        n = key[1:-1]
        if n in vars:
            key = vars[n]
    elif c > 3 and key[1] == '(' and key[-1] == ')' and key[0] == ':':
        n = key[2:-1]
        args = parse_shell_args(n)
        key = execute(len(args), args)
    return key

def alias_replace(args):
    name = args[0]
    for i in aliases:
        if name == i:
            repl = parse_shell_args(aliases[i])
            args.pop(0)
            for el in repl[::-1]:
                args.insert(0, el)
            break


def search(prefix):
    #check list
    check = os.listdir()
    lp = len(prefix)
    result = []
    
    for matcha in check:
        if matcha.startswith(prefix):
            mp = matcha[lp:]
            if os.path.isdir(prefix + mp):
                result.append(mp + '/')
            else:
                result.append(mp)

    if os.path.isdir(prefix):
        for matcha in os.listdir(prefix):
            if os.path.isdir(os.path.join(prefix, matcha)):
                result.append(matcha + '/')
            else:
                result.append(matcha)

    else:
        ri = prefix.rfind('/')
        if ri != -1:
            try_topath = prefix[:ri + 1]
            prefix = prefix[ri + 1:]
            if os.path.isdir(try_topath):
                for matcha in os.listdir(try_topath):
                    if matcha.startswith(prefix):
                        mp = matcha[len(prefix):]
                        if os.path.isdir(os.path.join(try_topath, matcha)):
                            result.append(mp + '/')
                        else:
                            result.append(mp)

    
    return result