from userglobals import userglobals
from ftplib import FTP
import os

def install_CLI(file, packagename, force):

    #wrong or missing arguments
    if file == "" or file[0] == '-' or file[0] == '!':
        print("{archive_path} was expected; got " + f"'{file}'")
        return False
    if packagename == "" or packagename[0] == '-' or packagename[0] == '-':
        print("{package_name} was expected; got " + f"'{packagename}'")
        return False

    import zipfile
    from globalconfig import Config
    cfg = Config()

    if packagename in os.listdir("apps/default/"):
        print(f"Package '{packagename}' already exist among system apps. Stop.")
        return False

    #file check
    if os.path.exists(file):
        print("Analysing containtment...")
        if zipfile.is_zipfile(file):
            with zipfile.ZipFile(file, 'r') as archive:
                zip_files = [file for file in archive.namelist() if '/' not in file]
                print(f"{len(zip_files)} files in root folder.")
                if len(zip_files) > 0:

                    #required files are missing
                    if ".app" not in zip_files:
                        print("Required file missing: .app")
                        return False
                    elif "icon.asc" not in zip_files:
                        print("App icon may be missing.")

                    #entry file not found
                    if packagename + ".py" not in zip_files:
                        import utils.stringmethods as strutils
                        similarname = strutils.closest(packagename + ".py", (i for i in zip_files if len(i) >= 4 and i[-3:] == ".py"))
                        print(f'Entry file {packagename}.py is missing. Did you mean "{similarname[:-3]}"?')
                        return False

                    #package already exists
                    if os.path.exists(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename):
                        ans = 'y'
                        if not force:
                            ans = input("Package with that name already exist. Proceed? (y/n)")
                        if ans != 'y': return False

                    #installing
                    try:
                        os.makedirs(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename, mode = 0o764)
                        print("Unpacking...")
                        archive.extractall(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename)
                        print("Creating config...")
                        os.makedirs(userglobals.userpath + ".local/share/CLIsma/config/apps/" + packagename, mode = 0o777)
                        config_path = userglobals.userpath + ".local/share/CLIsma/config/apps/" + packagename + '/main.conf'
                        if os.path.exists(config_path):
                            print("Warning: config file for this app existed before.")
                        else:
                            open(config_path, 'w').close()
                        print(f"Package {packagename} was succesfully installed.")
                        return True
                    except:
                        print("Unknown error has ocurred during the installation.")
                        return False
                else:
                    print("Maybe, archive is nested or empty.")
        else:
            print("Specified file is not a ZIP archive.")
    else:
        print("Specified file does not exists.")
    return False

def remove_CLI(packagename, force):
    import shutil

    package_path = userglobals.userpath + ".local/share/CLIsma/custom/apps/" + packagename

    if os.path.exists(package_path):
        print("Package found")
        ans = 'y'
        if not force:
            ans = input("Proceed? (y/n)")
        if ans != 'y':
            print("Cancelled.")
            return False
    else:
        from NodeSquad.appool import AppPool
        appool = AppPool()
        packagelist = appool.apps
        if len(appool.apps) > 0:
            import utils.stringmethods as strutils
            similarname = strutils.closest(packagename + ".py", packagelist)
            print(f"Error: package not found. Did you mean '{similarname}'?")
        else:
            print(f"Error: package not found.")
        return False

    config_path = userglobals.userpath + ".local/share/CLIsma/config/apps/" + packagename
    if os.path.exists(config_path):
        ans = 'y'
        if not force:
            ans = input("Remove config? (y/n)")
        if ans == 'y':
            try:
                shutil.rmtree(config_path)
                print("Config removed")
            except:
                print("Failed.")
    
    
    print("Removing package...")
    try:
        shutil.rmtree(package_path)
        print(f"Done removing '{packagename}'")
        return True
    except:
        print("Removal failed. Did you granted root permissions?")
        return False
    return False


def run(argc, args):
    force = False
    if args == ["carmen"]: args.append("-h")
    for i in range(1, len(args)):
        arg = args[i]
        if arg == '-h' or arg == '--help':
            print("Carmen Package Manager")
            print("Usage")
            print("    -h, --help                                       Print help message")
            print("    -i, --install {archive_path} {package_name}      Install a package")
            print("    -r, --remove {package_name}                      Remove a package")
            print("    --refresh                                        Refresh package list from repository")
            return True
        elif arg == '-f' or arg == '--force':
            force = True
        elif arg == '-#f' or arg == '--#force':
            force = False
        elif arg == '-i' or arg == '--install':
            file = ""
            packagename = ""
            if len(args) > i + 1:
                file = args[i + 1]
            if len(args) > i + 2:
                packagename = args[i + 2]
            install_CLI(file, packagename, force)
        elif arg == '-r' or arg == '--remove':
            packagename = ""
            if len(args) > i + 1:
                packagename = args[i + 1]
            install_CLI(file, packagename, force)