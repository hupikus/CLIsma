import curses

from integration.loghandler import Loghandler

class Colors:

    colorMode = {}

    FXNormal = curses.A_NORMAL

    FXItalic = FXNormal
    FXPale = FXNormal
    FXHighlight = FXNormal
    FXUnderline = FXNormal
    FXReverse = FXNormal
    FXReversed = FXNormal
    FXAlt = FXNormal
    FXBlink = FXNormal
    FXInvisible = FXNormal


    #Thank you, but actually turns out some of this effects may be missing in specific linux distributions
    try:
        FXBold = curses.A_BOLD
    except:
        pass
    try:
        FXItalic = curses.A_ITALIC
    except:
        pass
    try:
        FXPale = curses.A_DIM
    except:
        pass
    try:
        FXHighlight = curses.A_STANDOUT
    except:
        pass
    try:
        FXUnderline = curses.A_UNDERLINE
    except:
        pass
    try:
        FXReverse = curses.A_REVERSE
        FXReversed = curses.A_REVERSE
    except:
        FXReverse = FXNormal
        FXReversed = FXNormal
    try:
        FXAlt = curses.A_ALTCHARSET
    except:
        pass
    try:
        FXBlink = curses.A_BLINK
    except:
        pass
    try:
        FXInvisible = curses.A_INVIS
    except:
        pass


    FXWhite = curses.COLOR_WHITE
    FXBlack = curses.COLOR_BLACK
    FXRed = curses.COLOR_RED
    FXGreen = curses.COLOR_GREEN
    FXYellow = curses.COLOR_YELLOW
    FXBlue = curses.COLOR_BLUE
    FXMagenta = curses.COLOR_MAGENTA
    FXCyan = curses.COLOR_CYAN

    FXTextBlack = FXNormal
    FXTextRed = FXNormal
    FXTextGreen = FXNormal
    FXTextYellow = FXNormal
    FXTextBlue = FXNormal
    FXTextMagenta = FXNormal
    FXTextCyan = FXNormal
    FXTextWhite = FXNormal

    FXHash = {
        "normal":curses.A_NORMAL,
        "norma":curses.A_NORMAL, # Please don't kill me this is temporary here
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
    def start_color(forceColor):
        curses.start_color()
        curses.use_default_colors()

        Colors.colorPosibility = True
        Colors.colorlen = curses.COLORS
        if forceColor and Colors.colorlen >= 2:
            Colors.colorlen = 8

        if curses.can_change_color():
            curses.init_color(0, 121, 121, 121)
            curses.init_color(1, 823, 239, 145)
            curses.init_color(2, 345, 722, 165)
            curses.init_color(3, 769, 678, 219)
            curses.init_color(4, 192, 392, 952)
            curses.init_color(5, 514, 282, 659)
            curses.init_color(6, 388, 812, 859)
            curses.init_color(7, 900, 900, 900)


        if Colors.colorlen >= 8:
            Colors.FXTextBlack = curses.color_pair(0)
            Colors.FXTextRed = curses.color_pair(1)
            Colors.FXTextGreen = curses.color_pair(2)
            Colors.FXTextYellow = curses.color_pair(3)
            Colors.FXTextBlue = curses.color_pair(4)
            Colors.FXTextMagenta = curses.color_pair(5)
            Colors.FXTextCyan = curses.color_pair(6)
            Colors.FXTextWhite = curses.color_pair(7)

    @staticmethod
    def define_pairs():
        Colors.pairlen = curses.COLOR_PAIRS

        Loghandler.Log(f"Color amount is {Colors.colorlen}, color pairs amount is {Colors.pairlen}")
        # if Colors.colorlen > 16:
        #     try:
        #         depth = round((Colors.colorlen - 8) ** 0.333 - 0.5)
        #         Colors.colorDepth = depth
        #         step = round(Colors.colorlen / depth - 0.5)
        #         rng = range(depth)
        #         i = 9
        #         for r in rng:
        #             for g in rng:
        #                 for b in rng:
        #                     curses.init_color(i, r, g, b)
        #                     i += 1
        #     except:
        #         print("Color error. try launching CLIsma with -l option or changing the environment.")
        #         exit()
        #if Colors.colorlen == 8 and curses.COLOR_PAIRS == 64:
        i = 0
        for fore in range(8):
            curses.init_pair(i, fore, -1)
            i += 1
        for back in range(1, 8):
            for fore in range(8):
                curses.init_pair(i, fore, back)
                i += 1
        if curses.COLOR_PAIRS >= 72:
            for fore in range(8):
                curses.init_pair(i, fore, 0)
                i += 1
        #curses.init_pair(63, 7, 0)
        # else:
        #     for i in range(Colors.colorlen):
        #         curses.init_pair(i, i, - 1)

    @staticmethod
    def newPair(forecolor, backcolor):
        curses.init_pair(Colors.colorlen, forecolor, backcolor)

    @staticmethod
    def colorPair(num):
        return curses.color_pair(num)

    @staticmethod
    def getColorPair(foreground, background = -1):
        if foreground == -1: foreground = 0
        if background == -1: return curses.color_pair(7 + foreground)
        return curses.color_pair(background * 8 + foreground)

    @staticmethod
    def getPairColors(num):
        fg = num % 8
        bg = num // 8
        return fg, bg

    @staticmethod
    def getPairNumber(attr):
        return curses.pair_number(attr)
