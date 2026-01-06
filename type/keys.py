#"all keys", actuially. see: https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
class Keys:
    KEY_RESERVED                           = 0
    KEY_ESC                                = 1
    KEY_1                                  = 2
    KEY_2                                  = 3
    KEY_3                                  = 4
    KEY_4                                  = 5
    KEY_5                                  = 6
    KEY_6                                  = 7
    KEY_7                                  = 8
    KEY_8                                  = 9
    KEY_9                                  = 10
    KEY_0                                  = 11
    KEY_MINUS                              = 12
    KEY_EQUAL                              = 13
    KEY_BACKSPACE                          = 14
    KEY_TAB                                = 15
    KEY_Q                                  = 16
    KEY_W                                  = 17
    KEY_E                                  = 18
    KEY_R                                  = 19
    KEY_T                                  = 20
    KEY_Y                                  = 21
    KEY_U                                  = 22
    KEY_I                                  = 23
    KEY_O                                  = 24
    KEY_P                                  = 25
    KEY_LEFTBRACE                          = 26
    KEY_RIGHTBRACE                         = 27
    KEY_ENTER                              = 28
    KEY_LEFTCTRL                           = 29
    KEY_A                                  = 30
    KEY_S                                  = 31
    KEY_D                                  = 32
    KEY_F                                  = 33
    KEY_G                                  = 34
    KEY_H                                  = 35
    KEY_J                                  = 36
    KEY_K                                  = 37
    KEY_L                                  = 38
    KEY_SEMICOLON                          = 39
    KEY_APOSTROPHE                         = 40
    KEY_GRAVE                              = 41
    KEY_LEFTSHIFT                          = 42
    KEY_BACKSLASH                          = 43
    KEY_Z                                  = 44
    KEY_X                                  = 45
    KEY_C                                  = 46
    KEY_V                                  = 47
    KEY_B                                  = 48
    KEY_N                                  = 49
    KEY_M                                  = 50
    KEY_COMMA                              = 51
    KEY_DOT                                = 52
    KEY_SLASH                              = 53
    KEY_RIGHTSHIFT                         = 54
    KEY_KPASTERISK                         = 55
    KEY_LEFTALT                            = 56
    KEY_SPACE                              = 57
    KEY_CAPSLOCK                           = 58
    KEY_F1                                 = 59
    KEY_F2                                 = 60
    KEY_F3                                 = 61
    KEY_F4                                 = 62
    KEY_F5                                 = 63
    KEY_F6                                 = 64
    KEY_F7                                 = 65
    KEY_F8                                 = 66
    KEY_F9                                 = 67
    KEY_F10                                = 68
    KEY_NUMLOCK                            = 69
    KEY_SCROLLLOCK                         = 70
    KEY_KP7                                = 71
    KEY_KP8                                = 72
    KEY_KP9                                = 73
    KEY_KPMINUS                            = 74
    KEY_KP4                                = 75
    KEY_KP5                                = 76
    KEY_KP6                                = 77
    KEY_KPPLUS                             = 78
    KEY_KP1                                = 79
    KEY_KP2                                = 80
    KEY_KP3                                = 81
    KEY_KP0                                = 82
    KEY_KPDOT                              = 83

    KEY_ZENKAKUHANKAKU                     = 85
    KEY_102ND                              = 86
    KEY_F11                                = 87
    KEY_F12                                = 88
    KEY_RO                                 = 89
    KEY_KATAKANA                           = 90
    KEY_HIRAGANA                           = 91
    KEY_HENKAN                             = 92
    KEY_KATAKANAHIRAGANA                   = 93
    KEY_MUHENKAN                           = 94
    KEY_KPJPCOMMA                          = 95
    KEY_KPENTER                            = 96
    KEY_RIGHTCTRL                          = 97
    KEY_KPSLASH                            = 98
    KEY_SYSRQ                              = 99
    KEY_RIGHTALT                           = 100
    KEY_LINEFEED                           = 101
    KEY_HOME                               = 102
    KEY_UP                                 = 103
    KEY_PAGEUP                             = 104
    KEY_LEFT                               = 105
    KEY_RIGHT                              = 106
    KEY_END                                = 107
    KEY_DOWN                               = 108
    KEY_PAGEDOWN                           = 109
    KEY_INSERT                             = 110
    KEY_DELETE                             = 111
    KEY_MACRO                              = 112
    KEY_MUTE                               = 113
    KEY_VOLUMEDOWN                         = 114
    KEY_VOLUMEUP                           = 115
    KEY_POWER                              = 116           #SC System Power Down
    KEY_KPEQUAL                            = 117
    KEY_KPPLUSMINUS                        = 118
    KEY_PAUSE                              = 119
    KEY_SCALE                              = 120           #AL Compiz Scale (Expose)

    KEY_KPCOMMA                            = 121
    KEY_HANGEUL                            = 122
    KEY_HANGUEL                    = KEY_HANGEUL
    KEY_HANJA                              = 123
    KEY_YEN                                = 124
    KEY_LEFTMETA                           = 125
    KEY_RIGHTMETA                          = 126
    KEY_COMPOSE                            = 127

    KEY_STOP                               = 128           #AC Stop
    KEY_AGAIN                              = 129
    KEY_PROPS                              = 130           #AC Properties
    KEY_UNDO                               = 131           #AC Undo
    KEY_FRONT                              = 132
    KEY_COPY                               = 133           #AC Copy
    KEY_OPEN                               = 134           #AC Open
    KEY_PASTE                              = 135           #AC Paste
    KEY_FIND                               = 136           #AC Search
    KEY_CUT                                = 137           #AC Cut
    KEY_HELP                               = 138           #AL Integrated Help Center
    KEY_MENU                               = 139           #Menu (show menu)
    KEY_CALC                               = 140           #AL Calculator
    KEY_SETUP                              = 141
    KEY_SLEEP                              = 142           #SC System Sleep
    KEY_WAKEUP                             = 143           #System Wake Up
    KEY_FILE                               = 144           #AL Local Machine Browser
    KEY_SENDFILE                           = 145
    KEY_DELETEFILE                         = 146
    KEY_XFER                               = 147
    KEY_PROG1                              = 148
    KEY_PROG2                              = 149
    KEY_WWW                                = 150           #AL Internet Browser
    KEY_MSDOS                              = 151
    KEY_COFFEE                             = 152           #AL Terminal Lock/Screensaver
    KEY_SCREENLOCK                  = KEY_COFFEE
    KEY_ROTATE_DISPLAY                     = 153           #Display orientation for e.g. tablets
    KEY_DIRECTION           = KEY_ROTATE_DISPLAY
    KEY_CYCLEWINDOWS                       = 154
    KEY_MAIL                               = 155
    KEY_BOOKMARKS                          = 156           #AC Bookmarks
    KEY_COMPUTER                           = 157
    KEY_BACK                               = 158           #AC Back
    KEY_FORWARD                            = 159           #AC Forward
    KEY_CLOSECD                            = 160
    KEY_EJECTCD                            = 161
    KEY_EJECTCLOSECD                       = 162
    KEY_NEXTSONG                           = 163
    KEY_PLAYPAUSE                          = 164
    KEY_PREVIOUSSONG                       = 165
    KEY_STOPCD                             = 166
    KEY_RECORD                             = 167
    KEY_REWIND                             = 168
    KEY_PHONE                              = 169           #Media Select Telephone
    KEY_ISO                                = 170
    KEY_CONFIG                             = 171           #AL Consumer Control Configuration
    KEY_HOMEPAGE                           = 172           #AC Home
    KEY_REFRESH                            = 173           #AC Refresh
    KEY_EXIT                               = 174           #AC Exit
    KEY_MOVE                               = 175
    KEY_EDIT                               = 176
    KEY_SCROLLUP                           = 177
    KEY_SCROLLDOWN                         = 178
    KEY_KPLEFTPAREN                        = 179
    KEY_KPRIGHTPAREN                       = 180
    KEY_NEW                                = 181           #AC New
    KEY_REDO                               = 182           #AC Redo/Repeat

    KEY_F13                                = 183
    KEY_F14                                = 184
    KEY_F15                                = 185
    KEY_F16                                = 186
    KEY_F17                                = 187
    KEY_F18                                = 188
    KEY_F19                                = 189
    KEY_F20                                = 190
    KEY_F21                                = 191
    KEY_F22                                = 192
    KEY_F23                                = 193
    KEY_F24                                = 194

    KEY_PLAYCD                             = 200
    KEY_PAUSECD                            = 201
    KEY_PROG3                              = 202
    KEY_PROG4                              = 203
    KEY_ALL_APPLICATIONS                   = 204           #AC Desktop Show All Applications
    KEY_DASHBOARD         = KEY_ALL_APPLICATIONS
    KEY_SUSPEND                            = 205
    KEY_CLOSE                              = 206           #AC Close
    KEY_PLAY                               = 207
    KEY_FASTFORWARD                        = 208
    KEY_BASSBOOST                          = 209
    KEY_PRINT                              = 210           #AC Print
    KEY_HP                                 = 211
    KEY_CAMERA                             = 212
    KEY_SOUND                              = 213
    KEY_QUESTION                           = 214
    KEY_EMAIL                              = 215
    KEY_CHAT                               = 216
    KEY_SEARCH                             = 217
    KEY_CONNECT                            = 218
    KEY_FINANCE                            = 219           #AL Checkbook/Finance
    KEY_SPORT                              = 220
    KEY_SHOP                               = 221
    KEY_ALTERASE                           = 222
    KEY_CANCEL                             = 223           #AC Cancel
    KEY_BRIGHTNESSDOWN                     = 224
    KEY_BRIGHTNESSUP                       = 225
    KEY_MEDIA                              = 226

    KEY_SWITCHVIDEOMODE                    = 227           #Cycle between available video outputs (Monitor/LCD/TV-out/etc)

    KEY_KBDILLUMTOGGLE                     = 228
    KEY_KBDILLUMDOWN                       = 229
    KEY_KBDILLUMUP                         = 230

    KEY_SEND                               = 231           #AC Send
    KEY_REPLY                              = 232           #AC Reply
    KEY_FORWARDMAIL                        = 233           #AC Forward Msg
    KEY_SAVE                               = 234           #AC Save
    KEY_DOCUMENTS                          = 235

    KEY_BATTERY                            = 236

    KEY_BLUETOOTH                          = 237
    KEY_WLAN                               = 238
    KEY_UWB                                = 239

    KEY_UNKNOWN                            = 240

    KEY_VIDEO_NEXT                         = 241           #drive next video source
    KEY_VIDEO_PREV                         = 242           #drive previous video source
    KEY_BRIGHTNESS_CYCLE                   = 243           #brightness up", after max is min
    KEY_BRIGHTNESS_AUTO                    = 244           #Set Auto Brightness: manual brightness control is off", rely on ambient

    KEY_BRIGHTNESS_ZERO    = KEY_BRIGHTNESS_AUTO
    KEY_DISPLAY_OFF                        = 245           #display device to off state

    KEY_WWAN                               = 246           #Wireless WAN (LTE", UMTS", GSM", etc.)
    KEY_WIMAX                         = KEY_WWAN
    KEY_RFKILL                             = 247           #Key that controls all radios

    KEY_MICMUTE                            = 248           #Mute / unmute the microphone

            #Code 255 is reserved for special needs of AT keyboard driver

    KEY_NAMES = [
        "KEY_RESERVED",
        "KEY_ESC",
        "KEY_1",
        "KEY_2",
        "KEY_3",
        "KEY_4",
        "KEY_5",
        "KEY_6",
        "KEY_7",
        "KEY_8",
        "KEY_9",
        "KEY_0",
        "KEY_MINUS",
        "KEY_EQUAL",
        "KEY_BACKSPACE",
        "KEY_TAB",
        "KEY_Q",
        "KEY_W",
        "KEY_E",
        "KEY_R",
        "KEY_T",
        "KEY_Y",
        "KEY_U",
        "KEY_I",
        "KEY_O",
        "KEY_P",
        "KEY_LEFTBRACE",
        "KEY_RIGHTBRACE",
        "KEY_ENTER",
        "KEY_LEFTCTRL",
        "KEY_A",
        "KEY_S",
        "KEY_D",
        "KEY_F",
        "KEY_G",
        "KEY_H",
        "KEY_J",
        "KEY_K",
        "KEY_L",
        "KEY_SEMICOLON",
        "KEY_APOSTROPHE",
        "KEY_GRAVE",
        "KEY_LEFTSHIFT",
        "KEY_BACKSLASH",
        "KEY_Z",
        "KEY_X",
        "KEY_C",
        "KEY_V",
        "KEY_B",
        "KEY_N",
        "KEY_M",
        "KEY_COMMA",
        "KEY_DOT",
        "KEY_SLASH",
        "KEY_RIGHTSHIFT",
        "KEY_KPASTERISK",
        "KEY_LEFTALT",
        "KEY_SPACE",
        "KEY_CAPSLOCK",
        "KEY_F1",
        "KEY_F2",
        "KEY_F3",
        "KEY_F4",
        "KEY_F5",
        "KEY_F6",
        "KEY_F7",
        "KEY_F8",
        "KEY_F9",
        "KEY_F10",
        "KEY_NUMLOCK",
        "KEY_SCROLLLOCK",
        "KEY_KP7",
        "KEY_KP8",
        "KEY_KP9",
        "KEY_KPMINUS",
        "KEY_KP4",
        "KEY_KP5",
        "KEY_KP6",
        "KEY_KPPLUS",
        "KEY_KP1",
        "KEY_KP2",
        "KEY_KP3",
        "KEY_KP0",
        "KEY_KPDOT",

        "KEY_ZENKAKUHANKAKU",
        "KEY_102ND",
        "KEY_F11",
        "KEY_F12",
        "KEY_RO",
        "KEY_KATAKANA",
        "KEY_HIRAGANA",
        "KEY_HENKAN",
        "KEY_KATAKANAHIRAGANA",
        "KEY_MUHENKAN",
        "KEY_KPJPCOMMA",
        "KEY_KPENTER",
        "KEY_RIGHTCTRL",
        "KEY_KPSLASH",
        "KEY_SYSRQ",
        "KEY_RIGHTALT",
        "KEY_LINEFEED",
        "KEY_HOME",
        "KEY_UP",
        "KEY_PAGEUP",
        "KEY_LEFT",
        "KEY_RIGHT",
        "KEY_END",
        "KEY_DOWN",
        "KEY_PAGEDOWN",
        "KEY_INSERT",
        "KEY_DELETE",
        "KEY_MACRO",
        "KEY_MUTE",
        "KEY_VOLUMEDOWN",
        "KEY_VOLUMEUP",
        "KEY_POWER",
        "KEY_KPEQUAL",
        "KEY_KPPLUSMINUS",
        "KEY_PAUSE",
        "KEY_SCALE",

        "KEY_KPCOMMA",
        "KEY_HANGEUL",
        "KEY_HANGUEL",
        "KEY_HANJA",
        "KEY_YEN",
        "KEY_LEFTMETA",
        "KEY_RIGHTMETA",
        "KEY_COMPOSE",

        "KEY_STOP",
        "KEY_AGAIN",
        "KEY_PROPS",
        "KEY_UNDO",
        "KEY_FRONT",
        "KEY_COPY",
        "KEY_OPEN",
        "KEY_PASTE",
        "KEY_FIND",
        "KEY_CUT",
        "KEY_HELP",
        "KEY_MENU",
        "KEY_CALC",
        "KEY_SETUP",
        "KEY_SLEEP",
        "KEY_WAKEUP",
        "KEY_FILE",
        "KEY_SENDFILE",
        "KEY_DELETEFILE",
        "KEY_XFER",
        "KEY_PROG1",
        "KEY_PROG2",
        "KEY_WWW",
        "KEY_MSDOS",
        "KEY_COFFEE",
        "KEY_SCREENLOCK",
        "KEY_ROTATE_DISPLAY",
        "KEY_DIRECTION",
        "KEY_CYCLEWINDOWS",
        "KEY_MAIL",
        "KEY_BOOKMARKS",
        "KEY_COMPUTER",
        "KEY_BACK",
        "KEY_FORWARD",
        "KEY_CLOSECD",
        "KEY_EJECTCD",
        "KEY_EJECTCLOSECD",
        "KEY_NEXTSONG",
        "KEY_PLAYPAUSE",
        "KEY_PREVIOUSSONG",
        "KEY_STOPCD",
        "KEY_RECORD",
        "KEY_REWIND",
        "KEY_PHONE",
        "KEY_ISO",
        "KEY_CONFIG",
        "KEY_HOMEPAGE",
        "KEY_REFRESH",
        "KEY_EXIT",
        "KEY_MOVE",
        "KEY_EDIT",
        "KEY_SCROLLUP",
        "KEY_SCROLLDOWN",
        "KEY_KPLEFTPAREN",
        "KEY_KPRIGHTPAREN",
        "KEY_NEW",
        "KEY_REDO",

        "KEY_F13",
        "KEY_F14",
        "KEY_F15",
        "KEY_F16",
        "KEY_F17",
        "KEY_F18",
        "KEY_F19",
        "KEY_F20",
        "KEY_F21",
        "KEY_F22",
        "KEY_F23",
        "KEY_F24",

        "KEY_PLAYCD",
        "KEY_PAUSECD",
        "KEY_PROG3",
        "KEY_PROG4",
        "KEY_ALL_APPLICATIONS",
        "KEY_DASHBOARD",
        "KEY_SUSPEND",
        "KEY_CLOSE",
        "KEY_PLAY",
        "KEY_FASTFORWARD",
        "KEY_BASSBOOST",
        "KEY_PRINT",
        "KEY_HP",
        "KEY_CAMERA",
        "KEY_SOUND",
        "KEY_QUESTION",
        "KEY_EMAIL",
        "KEY_CHAT",
        "KEY_SEARCH",
        "KEY_CONNECT",
        "KEY_FINANCE",
        "KEY_SPORT",
        "KEY_SHOP",
        "KEY_ALTERASE",
        "KEY_CANCEL",
        "KEY_BRIGHTNESSDOWN",
        "KEY_BRIGHTNESSUP",
        "KEY_MEDIA",

        "KEY_SWITCHVIDEOMODE",

        "KEY_KBDILLUMTOGGLE",
        "KEY_KBDILLUMDOWN",
        "KEY_KBDILLUMUP",

        "KEY_SEND",
        "KEY_REPLY",
        "KEY_FORWARDMAIL",
        "KEY_SAVE",
        "KEY_DOCUMENTS",

        "KEY_BATTERY",

        "KEY_BLUETOOTH",
        "KEY_WLAN",
        "KEY_UWB",

        "KEY_UNKNOWN",

        "KEY_VIDEO_NEXT",
        "KEY_VIDEO_PREV",
        "KEY_BRIGHTNESS_CYCLE",
        "KEY_BRIGHTNESS_AUTO",

        "KEY_BRIGHTNESS_ZERO",
        "KEY_DISPLAY_OFF",

        "KEY_WWAN",
        "KEY_WIMAX",
        "KEY_RFKILL",

        "KEY_MICMUTE",
        ]

    KEY_SYMBOLS = {
        KEY_1:              '1' ,
        KEY_2:              '2' ,
        KEY_3:              '3' ,
        KEY_4:              '4' ,
        KEY_5:              '5' ,
        KEY_6:              '6' ,
        KEY_7:              '7' ,
        KEY_8:              '8' ,
        KEY_9:              '9' ,
        KEY_0:              '0' ,
        KEY_MINUS:          '-' ,
        KEY_EQUAL:          '=' ,
        KEY_BACKSPACE:      '+' ,
        KEY_TAB:            '\t',
        KEY_Q:              'q' ,
        KEY_W:              'w' ,
        KEY_E:              'e' ,
        KEY_R:              'r' ,
        KEY_T:              't' ,
        KEY_Y:              'y' ,
        KEY_U:              'u' ,
        KEY_I:              'i' ,
        KEY_O:              'o' ,
        KEY_P:              'p' ,
        KEY_LEFTBRACE:      '[' ,
        KEY_RIGHTBRACE:     ']' ,
        KEY_ENTER:          '\n',
        KEY_A:              'a' ,
        KEY_S:              's' ,
        KEY_D:              'd' ,
        KEY_F:              'f' ,
        KEY_G:              'g' ,
        KEY_H:              'h' ,
        KEY_J:              'j' ,
        KEY_K:              'k' ,
        KEY_L:              'l' ,
        KEY_SEMICOLON:      ';' ,
        KEY_APOSTROPHE:     '\'',
        KEY_GRAVE:          '`' ,
        KEY_BACKSLASH:      '\\',
        KEY_Z:              'z' ,
        KEY_X:              'x' ,
        KEY_C:              'c' ,
        KEY_V:              'v' ,
        KEY_B:              'b' ,
        KEY_N:              'n' ,
        KEY_M:              'm' ,
        KEY_COMMA:          ',' ,
        KEY_DOT:            '.' ,
        KEY_SLASH:          '/' ,
        KEY_SPACE:          ' ' ,
    }

    def KeyName(key):
        if key < 0 or key > 248: return "KEY_UNKNOWN"
        return Keys.KEY_NAMES[key]

    def isLetter(key):
        return (
            (key >= Keys.KEY_Q and key <= Keys.KEY_P) or
            (key >= Keys.KEY_A and key <= Keys.KEY_L) or
            (key >= Keys.KEY_Z and key <= Keys.KEY_M)
        )

    def isDigit(key):
        return (key >= Keys.KEY_1 and key <= Keys.KEY_0)

    def isSymbol(key):
        return ( 
            (key >= Keys.KEY_SEMICOLON and key <= Keys.KEY_BACKSLASH) or
            (key >= Keys.KEY_COMMA and key <= Keys.KEY_SLASH) or
            (key == Keys.KEY_MINUS or key == Keys.KEY_EQUAL) or
            (key == Keys.KEY_LEFTBRACE or key == Keys.KEY_RIGHTBRACE) or
            key == Keys.KEY_SPACE or
            Keys.isLetter(key) or
            Keys.isDigit(key)
        )

    def GetSymbol(key):
        if key in Keys.KEY_SYMBOLS:
            return Keys.KEY_SYMBOLS[key]
        return ''


    CAPITALS = {'[': '{', ']': '}', ';': ':', '\'': '"', '\\': '|', ',': '<', '.': '>', '/': '?', '-': '_', '=': '+'}

    def GetInput(key, shift, allow_escape = True):
        if key in Keys.KEY_SYMBOLS:
            char = Keys.KEY_SYMBOLS[key]
            if shift:

                if Keys.isDigit(key):
                    return "!@#$%^&*()"[key - Keys.KEY_1]
                elif Keys.isLetter(key):
                    return chr(ord(char) - 32)
                elif allow_escape == False and (key == Keys.KEY_ENTER or key == Keys.KEY_TAB):
                    return ''
                elif char in Keys.CAPITALS:
                    return Keys.CAPITALS[char]
                else:
                    return char

            else:
                return char
        return ''


class KeyState:
    keys = [False for i in range(248)]

    def KeyPress(self, key):
        self.keys[key] = True

    def KeyRelease(self, key):
        self.keys[key] = False

    def GetKey(self, key):
        if key < 0 or key > 248: return False
        return self.keys[key]
