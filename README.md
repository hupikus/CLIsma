# CLISMA

**CLISMA** is an console-based desktop enviroment. Made mostly for fun using python.

> Stands for 'Command-Line-Interface System Manager Accompanier'

![](./assets/readme_images/screenshot1.png)

## Cool Features

- poorly documented

- dependency-free (there is exceptions, see requirements)

- external apps support; package manager

- all input and windowing job are done for you; just append strings to the window

- premade ui elements: sliders, buttons, text fields

- multitasking window system

- many mouse cursors support

- runs smooth on old pcs



This app is currently unfinished and requies testing.



## Requirements

- curses for python
- alsa
- python 3.10 or newer

  additional: (unneccesary)
- pympler (pip)
- psutil (pip)
## Use

Just execute **main.py**, while in the folder. *You must* have access to /dev/input.
This could be arranged by adding your user into input group or running python with sudo or root.

> all input is received from from /dev/input.
> root privilegies isn't required for CLIsma shell.

```
sudo usermod -aG input $USER
```
then reboot.

```
cd ./CLIsma
pip install -r ./requirements-extra.txt
python main.py
```

###

### CLIsma have shell arguiments:

```
Usage: main.py --flag1 {required1} (optional2) --flag2 ...
Manipulate flag order to control order of execution
Use -# instead of - for opposite effect: supported commands marked with !
!   -b  --brief                                      Quick common info
!   -d, --debug                                      Debug mode
!   -f, --force                                      Disable confirmation (Warning: force deletion with -r)
!   -h, --help                                       Print this message
!   -i, --install {package_name} (archive_path)      Install a package
!   -r, --remove {package_name}                      Remove a package
!   -s, --shell                                      Shell mode (start CLIsma Shell)
    -l, --low-color                                  Force low color mode (compatibility)
```
