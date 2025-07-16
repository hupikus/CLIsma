import curses

class Colors:

    colorMode = {}


    FXItalic = curses.A_NORMAL


    FXNormal = curses.A_NORMAL
    FXBold = curses.A_BOLD
    #There is no italic in bodhi linux e.g., ill figure it out
    try:
        FXItalic = curses.A_ITALIC
    except:
        FXItalic = curses.A_NORMAL
    FXPale = curses.A_DIM
    FXHighlight = curses.A_STANDOUT
    FXUnderline = curses.A_UNDERLINE
    FXReverse = curses.A_REVERSE

    FXAlt = curses.A_ALTCHARSET
    FXBlink = curses.A_BLINK
    FXInvisible = curses.A_INVIS


    FXWhite = curses.COLOR_WHITE
    FXBlack = curses.COLOR_BLACK
    FXRed = curses.COLOR_RED
    FXGreen = curses.COLOR_GREEN
    FXYellow = curses.COLOR_YELLOW
    FXBlue = curses.COLOR_BLUE
    FXMagenta = curses.COLOR_MAGENTA
    FXCyan = curses.COLOR_CYAN

    FXHash = {
        "normal":curses.A_NORMAL,
        "blink":curses.A_BLINK,
        "bold":curses.A_BOLD,
        "pale":curses.A_DIM,
        "highlight":curses.A_STANDOUT,
        "underline":curses.A_UNDERLINE,
        "reverse":curses.A_REVERSE,
        "invisible":curses.A_INVIS,
        "alt":curses.A_ALTCHARSET
    }

    FXColorHash = {
        "white":curses.COLOR_WHITE,
        "black":curses.COLOR_BLACK,
        "red":curses.COLOR_RED,
        "green":curses.COLOR_GREEN,
        "yellow":curses.COLOR_YELLOW,
        "blue":curses.COLOR_BLUE,
        "magenta":curses.COLOR_MAGENTA,
        "cyan":curses.COLOR_CYAN
    }

    RawColorHash = {
        "white":'\033[0m',
        "black":'\033[30m',
        "red":'\033[91m',
        "green":'\033[92m',
        "yellow":'\033[93m',
        "blue":'\033[94m',
        "magenta":'\033[95m',
        "cyan":'\033[96m',
        "darkcyan":'\033[36m'
    }
    RawColor = [ '\033[0m', '\033[30m', '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[36m' ]


    colorPosibility = False
    colorlen = 2

    @staticmethod
    def define_pairs(forceColor):
        Colors.colorPosibility = True
        Colors.colorlen = curses.COLORS
        if forceColor:
            Colors.colorlen = 8
        if Colors.colorlen > 16:
            try:
                depth = round((Colors.colorlen - 8) ** 0.333 - 0.5)
                Colors.colorDepth = depth
                step = round(Colors.colorlen / depth - 0.5)
                rng = range(0, depth)
                i = 9
                for r in rng:
                    for g in rng:
                        for b in rng:
                            curses.init_color(i, r, 0, b)
                            i += 1
            except:
                print("Color error. try launching CLIsma with -l option or changing the environment.")
                exit()
        for i in range(Colors.colorlen):
            curses.init_pair(i, i, - 1)

    @staticmethod
    def newPair(forecolor, backcolor):
        curses.init_pair(Colors.colorlen, forecolor, backcolor)
        Colors.colorlen += 1
        return Colors.colorlen

    @staticmethod
    def colorPair(num):
        return curses.color_pair(num)
