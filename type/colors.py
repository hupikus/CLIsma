import curses

class Colors:

    colorMode = {}

    FXNormal = curses.A_NORMAL
    FXBlink = curses.A_BLINK
    FXBold = curses.A_BOLD
    FXItalic = curses.A_ITALIC
    FXPale = curses.A_DIM
    FXHighlight = curses.A_STANDOUT
    FXUnderline = curses.A_UNDERLINE
    FXReverse = curses.A_REVERSE

    colorPosibility = False
    colorlen = 0

    @staticmethod
    def define_pairs():
        Colors.colorPosibility = True
        Colors.colorlen = curses.COLORS
        for i in range(0, Colors.colorlen):
            curses.init_pair(i + 1, i, -1)
    
    @staticmethod
    def newPair(forecolor, backcolor):
        curses.init_pair(Colors.colorlen, forecolor, backcolor)
        Colors.colorlen += 1
        return Colors.colorlen
