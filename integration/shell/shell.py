import integration.shell.clismautils as utils
from userglobals import userglobals
import utils.stringmethods as strutils
import subprocess
import importlib

import threading
import time

import os      #\
import sys     # \
import termios #  - - - -
import tty     # /
import io      #/

import pty
import select


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


#redefine print() to control stdout
import builtins

prev_print = builtins.print

#usual redirection
def raw_print(*args, **kwargs):
    if 'end' not in kwargs:
        kwargs['end'] = '\r\n'
    prev_print(*args, **kwargs)

#redirection, write to stdout
def stdout_print(*args, **kwargs):
    sys.stdout.write(' '.join(args))
    if 'end' not in kwargs:
        sys.stdout.write('\r\n')

#redirection, write to pty slave
def pty_print(*args, **kwargs):
    global master
    global slave
    os.write(slave,  bytes(' '.join(args), 'utf-8'))
    if 'end' not in kwargs:
        os.write(slave, b'\r\n')
    elif kwargs["end"] != '':
       os.write(slave, bytes(kwargs["end"], 'utf-8'))


def redirect_print(print_func):
    builtins.print = print_func

redirect_print(raw_print)

#PTY
def set_pty_raw(fd):
    attrs = termios.tcgetattr(fd)
    attrs[3] &= ~(termios.ICANON | termios.ECHO)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)


master, slave = pty.openpty()
set_pty_raw(master)


def ever_stdout():
    global echoing
    global chmod
    global master
    global slave
    global running

    while running:
        try:
            rlist, _, _ = select.select([master], [], [])
            if master in rlist:
                output = os.read(master, 1).decode()
                print(output, end='') 
        except:
            break

def ever_getch():
    global buffer
    global last_getch
    global echoing
    global chmod
    global master
    global running


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
            shell_exit()
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
        #try:
        #    os.write(master, bytes(last_getch, 'utf-8'))
        #except:
        #    shell_exit()
        #    exit()

def shell_exit():
    global running
    global master
    global slave
    running = False
    os.close(master)
    os.close(slave)
    print("\x1b[?25h\r")

def shell():
    global buffer
    global last_getch
    global echoing
    global history
    global master
    global slave
    global running

    history_pos = 0
    cursor = 0

    prefix = '#' if os.geteuid() == 0 else '$'
    print(f"{os.path.basename(os.getcwd())} {prefix}> ", end = '', flush = True)


    getch_thread = threading.Thread(target=ever_getch)
    getch_thread.start()
    setch_thread = threading.Thread(target=ever_stdout)
    #setch_thread.start()

    while running:
        try:
        #check for charactersc
            if last_getch == '':
                pass
            elif last_getch == '\t':
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
                            print('\r' + f"{lr} matches")

            elif last_getch == '\n' or last_getch == '\r':
                print('\r' + '\x1b[2K' + f"{os.path.basename(os.getcwd())} {prefix}> {buffer}" + '\r')
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
                        print("\rPress any key...\r")
                        running = False
                        #setch_thread.join()
                        shell_exit()
                        exit()

                    #parse vars and etc
                    args = parse_shell_args(exe)

                    if not args:
                        continue

                    #try:
                    proc = execute(len(args), args)
                    if isinstance(proc, subprocess.Popen):
                        proc.wait()
                    process = False


                    print('\r', end = '')
                    #print(f"{os.path.basename(os.getcwd())} {prefix}>", end = ' ', flush = True)
                    #except:
                    #print("Execution failed.")

            elif last_getch == '\x1b[A': #Up arrow
                history_pos = max(history_pos - 1, -len(history))
                history[-1] = history[history_pos][:]
                cursor = len(history[-1])
            elif last_getch == '\x1b[B': #Down arrow
                if history_pos == -2:
                    history[-1] = ""
                    history_pos = -1
                    cursor = 0
                else:
                    history_pos = min(history_pos + 1, -1)
                    history[-1] = history[history_pos][:]
                    cursor = len(history[-1])
            elif last_getch == '\x1b[D': #Left arrow
                history_pos = -1
                cursor = max(0, cursor - 1)
            elif last_getch == '\x1b[C': #Right arrow
                history_pos = -1
                cursor = min(len(buffer), cursor + 1)
            elif last_getch == '\x7f': #Backspace
                history_pos = -1
                if cursor > 0:
                    history[-1] = history[-1][:cursor - 1] + history[-1][cursor:]
                    cursor -= 1
            else:
                #any character
                if chmod:
                    history[-1] = last_getch
                else:
                    history[-1] = history[-1][:cursor] + last_getch + history[-1][cursor:]
                    cursor += 1
                #print(last_getch, end = '', flush = True)
                history_pos = -1
            buffer = history[-1]


            #clear
            last_getch = ''
            time.sleep(update_interval)

            #'cursor symbol is cursor - 1, but cursor should be drawn at cursor'
            if len(buffer) > cursor:
                print('\r' + '\x1b[2K' + f"{os.path.basename(os.getcwd())} {prefix}> {buffer[:cursor]}{INVERSE}{buffer[cursor]}{REVERT}{buffer[cursor + 1:]}", end = '', flush = True)
            else:
                print('\r' + '\x1b[2K' + f"{os.path.basename(os.getcwd())} {prefix}> {buffer}{INVERSE} {REVERT}", end = '', flush = True)

                    

        except:
            exit()
    shell_exit()
    exit()
        


def run(args):
    shell()


def execute(argc, args):
    global master
    global slave

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
        elif key == "PATH":
            print("'PATH' is set to read-only. Use 'bpath' instead.")
            return False

        val =  kvar(name[i + 1:] + ' ' + ' '.join(args[1:]))

        vars[key] = val
        return val

    try:

        if name == "shell":
            run(args)
        elif name == "alias":
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
        elif name == "bpath":
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
        elif name == "reload":
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
        elif name == "vars":
            print(vars)
            return True
        else:
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
                    #return subprocess.Popen(args, stdin = None, stdout = slave, stderr = slave, env={"TERM":  term})
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
    except:
        pass


def parse_shell_args(argt):
    args = []
    buffer = ''
    quote_depth = False
    bracket_depth = 0
    for i in argt:
        try:
            if i == ' ':
                if not quote_depth:
                    #vars
                    args.append(kvar(buffer))
                    buffer = ''
            elif i == '"':
                quote_depth = not quote_depth
            elif i == '(':
                if not quote_depth:
                    bracket_depth += 1
                buffer += i
            elif i == ')':
                if not quote_depth:
                    bracket_depth -= 1
                    if bracket_depth < 0:
                        print("')': wrong syntax")
                        return False
                buffer += i
            else:
                buffer += i
        except:
            pass

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
