import integration.shell.clismautils as utils
from userglobals import userglobals
import subprocess
import importlib
import os

term = os.getenv('TERM', 'xterm')

modules = {"utils" : utils}
vars = { "PATH":["/bin/", os.path.join(userglobals.userpath, ".local/bin/"), "/usr/bin/", "/usr/local/bin/"] }
path = vars["PATH"]

aliases = {"ls" : "ls --color=always"}
vars["alias"] = aliases

echoing = True


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

            #parse vars and etc
            args = parse_shell_args(exe)

            if not args:
                continue

            #try:
            proc = execute(len(args), args)
            if isinstance(proc, subprocess.Popen):
                proc.wait()
                #for line in iter(proc.stdout.readline, b''):
                #    print(line.decode(), end='')
                #    print("\033[91m HHHH \033[0m")
                stdout, stderr = proc.communicate()
                print(stdout.decode())
            #except:
            #print("Execution failed.")
        #except:
        #    exit()

def run(args):
    shell(os.geteuid() == 0)


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
                    #return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"TERM":  term})
                    return os.system(' '.join(args))
    
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