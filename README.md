#  CLISMA
**CLISMA** is an console-based desktop enviroment. Mostly for fun.
> Stands for 'Command-Line-Interface System Manager Accompanier'

## Requirements
- curses
- evdev
- pydoc
- python 3.6 or newer

## Use
Just execute **main.py** with sudo or root, while in the folder.
> sudo is required because of reading device input from /dev/input. 
```
cd ./CLIsma
sudo python main.py
```

### Recently, CLIsma had got an arguments:

```
Insert flags before others to control order of execution
Use -# instead of - for opposite effect: supported commands marked with !

!   -b  --brief                                      Quick common info
!   -d, --debug                                      Debug mode
!   -f, --force                                      Disable confirmation (Warning: force deletion with -r)
!   -h, --help                                       Print help message
!   -i, --install {archive_path} {package_name}      Install a package
!   -r, --remove {package_name}                      Remove a package
```