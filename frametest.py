import sys
import os
import curses
import time


width = 25
height = 25

#preparation
screen = curses.initscr()

curses.curs_set(0)


#ASCII screen
root = curses.newwin(height, width, 0, 0)
#srend = [[' ' for x in range(width)] for y in range(height)]

counter = 0

while True:
    root.move(2, 2)		
    root.addstr(str(counter))
    counter += 1
    root.refresh()
    time.sleep(0.016)

