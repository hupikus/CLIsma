from userglobals import userglobals
import urllib.request
#from ftplib import FTP
import os

def install_CLI(packagename, file, force):
    mode = "Local"
    #wrong or missing arguments
    if packagename == "" or packagename[0] == '-' or packagename[0] == '-':
        print("{package_name} was expected; got " + f"'{packagename}'")
        return False
    if file == "" or file[0] == '-' or file[0] == '!':
        mode = "Remote"

    if packagename in os.listdir("apps/default/"):
        print(f"Package '{packagename}' already exist among system apps. Stop.")
        return False

    #LOCAL ARCHIVE MODE
    if mode == "Local":
        #file check
        if os.path.exists(file):
            print("Analysing containtment...")
            install_system(packagename, file, mode, force)
        else:
            print("Specified file does not exists.")
    #REMOTE PACKAGE MODE
    else:
        #results = search_host(packagename)
        result = search_host_strict(packagename)

        if not result:
            print(f"Error: {packagename}: package not found")
        else:
            packagename = result[0]
            url = result[3]

            print("Checking files...")
            cache_path = userglobals.userpath + ".cache/CLIsma/apps/"
            if not os.path.exists(cache_path): os.makedirs(cache_path, mode = 0o777)
            cache_path += packagename + '.zip'
            if os.path.exists(cache_path):
                os.remove(cache_path)

            try:
                print("Indexing...")
                urllib.request.urlretrieve(url, cache_path, reporthook = print_progress)
                print()
                print("Download completed.")
                install_system(packagename, cache_path, mode, force)
            except urllib.error.URLError as error:
                print("Error: Failed to download: Broken URL (" + error.reason + ')')
                return False
            except Exception as error:
                print("Error: Failed to download: " + str(error))
                return False

    return False

def remove_CLI(packagename, force):
    import shutil

    package_path = userglobals.userpath + ".local/share/CLIsma/custom/apps/external/" + packagename

    if os.path.exists(package_path):
        print("Package found")
        ans = 'y'
        if not force:
            ans = input("Proceed? (y/N)")
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

    config_path = userglobals.userpath + ".local/share/CLIsma/config/apps/external/" + packagename
    if os.path.exists(config_path):
        ans = 'y'
        if not force:
            ans = input("Remove config? (y/N)")
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
    except PermissionError:
        print("Removal failed. Permission denied.")
        return False
    except:
        print("Removal failed for unknown reason.")
        return False
    return False


host_root = "https://drive.google.com/uc?export=download&id="
database_path = userglobals.userpath + ".local/share/CLIsma/config/carmen/carmen_database"

def update_CLI():
    if os.path.exists(database_path):
        os.remove(database_path)
    file_id = "1UhGIBVVAlulUrhOqx4L5JEBFU6IMVMHA"
    print("Updating database...")
    urllib.request.urlretrieve(host_root + file_id, database_path, reporthook = print_progress)
    print()
    print("Download completed.")




def run(argc, args):
    force = False
    if args == ["carmen"]: args.append("-h")
    for i in range(1, len(args)):
        arg = args[i]
        if arg == '-h' or arg == '--help':
            print("Carmen Package Manager")
            print("Usage")
            print("carmen --flag {required} (optional)")
            print("    -h, --help                                       Print help message")
            print("    -i, --install {package_name} (archive_path)      Install a package")
            print("    -r, --remove {package_name}                      Remove a package")
            print("    -u, --update                                     Update the database")
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
                packagename = args[i + 1]
            if len(args) > i + 2:
                file = args[i + 2]
            install_CLI(packagename, file, force)
        elif arg == '-r' or arg == '--remove':
            packagename = ""
            if len(args) > i + 1:
                packagename = args[i + 1]
            remove_CLI(packagename, force)
        elif arg == '-u' or arg == '--update':
            update_CLI()


def search_host(name):
    if not os.path.exists(database_path):
        update_CLI()

    return tuple()

def search_host_strict(name):
    if not os.path.exists(database_path):
        update_CLI()

    print("Reading database...")
    file = open(database_path)
    order = file.readlines()
    file.close()
    print("Searching...")
    for line in order:
        content = line.split()
        package_name = content[0]
        if package_name == name:
            print("Package found")
            if len(content) != 4:
                print("Invalid package info. Consider telling CLIsma dev to fix database, then run 'carmen --update'.")
                return False
            return tuple([name, content[1], content[2].replace('_', ' '), host_root + content[3]])
            #            name  author      description                   url
    else:
        return False


def print_progress(block_num, block_size, total):
    dowd_size  = block_num * block_size
    bar_width = 50
    progress = round(bar_width * dowd_size / total + 0.5)
    if dowd_size == 0:
        print("Download started...")
        print(f"\r[{'-' * (bar_width)}] / {total / 1024:.2f} KB", end = '')
    elif dowd_size <= total:
        print(f"\r[{'=' * progress}{'-' * (bar_width - progress)}] {dowd_size / 1024:.2f} KB / {total / 1024:.2f} KB", end = '')



def install_system(packagename, file, mode, force):
    import zipfile
    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file, 'r') as archive:
            zip_files = [file for file in archive.namelist() if '/' not in file]
            if mode == "Local": print(f"{len(zip_files)} files in root folder.")
            if len(zip_files) > 0:

                #required files are missing
                if ".app" not in zip_files:
                    if mode == "Local": print("Required file missing: .app")
                    else: print("Error: Package is corrupted by author.")
                    return False
                elif "icon.asc" not in zip_files:
                    print("App icon may be missing.")

                #entry file not found
                if packagename + ".py" not in zip_files:
                    import utils.stringmethods as strutils
                    similarname = strutils.closest(packagename + ".py", (i for i in zip_files if len(i) >= 4 and i[-3:] == ".py"))
                    if mode == "Local": print(f'Entry file {packagename}.py is missing. Did you mean "{similarname[:-3]}"?')
                    else: print("Error: Package is corrupted by author.")
                    return False

                #package already exists
                if os.path.exists(userglobals.userpath + ".local/share/CLIsma/custom/apps/external/" + packagename):
                    ans = 'y'
                    if not force:
                        if mode == "Local":
                            ans = input("Package with that name already exist. Proceed? (y/N)")
                        else:
                            print("Package found, updating...")
                    if ans != 'y': return False

                #installing
                try:
                    p = userglobals.userpath + ".local/share/CLIsma/custom/apps/external/" + packagename
                    if not os.path.exists(p):
                        os.makedirs(p, mode = 0o764)
                    print("Unpacking...")
                    archive.extractall(p)
                    # print("Creating config...")
                    # p = userglobals.userpath + ".local/share/CLIsma/config/apps/external/" + packagename
                    # if not os.path.exists(p):
                    #     os.makedirs(p, mode = 0o777)
                    # config_path = p + '/main.conf'
                    # if os.path.exists(config_path):
                    #     if mode == "Local": print("Warning: config file for this app existed before.")
                    # else:
                    #     open(config_path, 'w').close()
                    if mode == "Remote":
                        print("Cleaning...")
                        try:
                            if os.path.exists(file):
                                os.remove(file)
                            print("Cleaning done.")
                        except:
                            print("Cleaning failed.")

                    print(f"Package {packagename} was succesfully installed.")
                    return True
                except Exception as error:
                    print(f"Unknown error has ocurred during the installation. ({str(error)})")
                    return False
            else:
                if mode == "Local": print("Maybe, archive is nested or empty.")
                else: print("Error: Package is corrupted by author.")
    else:
        if mode == "Local": print("Specified file is not a ZIP archive.")
        else: print("Error: File corrupted.")

    #Failed, but clean
    if mode == "Remote":
        print("Cleaning...")
        try:
            if os.path.exists(file):
                os.remove(file)
                print("Cleaning done.")
        except:
            print("Cleaning failed.")
    return False
