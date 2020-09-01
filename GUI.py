from ctypes import windll
from time import sleep

class KEY:
    CANCEL = 0X03
    BACKSPACE = 0X08
    TAB = 0X09
    ENTER = 0X0D
    SHIFT = 0X10
    CTRL = 0X11
    ALT = 0X12
    CAPSLOCK = 0X14
    ESC = 0X1B
    SPACE = 0X20
    PGUP = 0X21
    PGDOWN = 0X22
    END = 0X23
    HOME = 0X24
    LEFTARROW = 0X26
    UPARROW = 0X26
    RIGHTARROW = 0X27
    DOWNARROW = 0X28
    SELECT = 0X29
    PRINT = 0X2A
    EXECUTE = 0X2B
    PRINTSCREEN = 0X2C
    INSERT = 0X2D
    DELETE = 0X2E
    HELP = 0X2F
    NUM0 = 0X30
    NUM1 = 0X31
    NUM2 = 0X32
    NUM3 = 0X33
    NUM4 = 0X34
    NUM5 = 0X35
    NUM6 = 0X36
    NUM7 = 0X37
    NUM8 = 0X38
    NUM9 = 0X39
    A = 0X41
    B = 0X42
    C = 0X43
    D = 0X44
    E = 0X45
    F = 0X46
    G = 0X47
    H = 0X48
    I = 0X49
    J = 0X4A
    K = 0X4B
    L = 0X4C
    M = 0X4D
    N = 0X4E
    O = 0X4F
    P = 0X50
    Q = 0X51
    R = 0X52
    S = 0X53
    T = 0X54
    U = 0X55
    V = 0X56
    W = 0X57
    X = 0X58
    Y = 0X59
    Z = 0X5A
    LEFTWIN = 0X5B
    RIGHTWIN = 0X5C
    APPS = 0X5D
    SLEEP = 0X5F
    NUMPAD0 = 0X60
    NUMPAD1 = 0X61
    NUMPAD3 = 0X63
    NUMPAD4 = 0X64
    NUMPAD5 = 0X65
    NUMPAD6 = 0X66
    NUMPAD7 = 0X67
    NUMPAD8 = 0X68
    NUMPAD9 = 0X69
    MULTIPLY = 0X6A
    ADD = 0X6B
    SEPERATOR = 0X6C
    SUBTRACT = 0X6D
    DECIMAL = 0X6E
    DIVIDE = 0X6F
    F1 = 0X70
    F2 = 0X71
    F3 = 0X72
    F4 = 0X73
    F5 = 0X74
    F6 = 0X75
    F7 = 0X76
    F8 = 0X77
    F9 = 0X78
    F10 = 0X79
    F11 = 0X7A
    F12 = 0X7B
    F13 = 0X7C
    F14 = 0X7D
    F15 = 0X7E
    F16 = 0X7F
    F17 = 0X80
    F19 = 0X82
    F20 = 0X83
    F21 = 0X84
    F22 = 0X85
    F23 = 0X86
    F24 = 0X87
    NUMLOCK = 0X90
    SCROLLLOCK = 0X91
    LEFTSHIFT = 0XA0
    RIGHTSHIFT = 0XA1
    LEFTCTRL = 0XA2
    RIGHTCTRL = 0XA3
    LEFTMENU = 0XA4
    RIGHTMENU = 0XA5
    BROWSERBACK = 0XA6
    BROWSERFORWARD = 0XA7
    BROWSERREFRESH = 0XA8
    BROWSERSTOP = 0XA9
    BROWSERFAVORIES = 0XAB
    BROWSERHOME = 0XAC
    VOLUMEMUTE = 0XAD
    VOLUMEDOWN = 0XAE
    VOLUMEUP = 0XAF
    NEXTTRACK = 0XB0
    PREVOUSTRACK = 0XB1
    STOPMEDIA = 0XB2
    PLAYPAUSE = 0XB3
    LAUNCHMAIL = 0XB4
    SELECTMEDIA = 0XB5
    LAUNCHAPP1 = 0XB6
    LAUNCHAPP2 = 0XB7
    SEMICOLON = 0XBA
    EQUALS = 0XBB
    COMMA = 0XBC
    DASH = 0XBD
    PERIOD = 0XBE
    SLASH = 0XBF
    ACCENT = 0XC0
    OPENINGSQUAREBRACKET = 0XDB
    BACKSLASH = 0XDC
    CLOSINGSQUAREBRACKET = 0XDD
    QUOTE = 0XDE
    PLAY = 0XFA
    ZOOM = 0XFB
    PA1 = 0XFD
    CLEAR = 0XFE

    LEFT = [0x0002, 0x0004]
    RIGHT = [0x0008, 0x00010]
    MIDDLE = [0x00020, 0x00040]

class Keyboard:
    def __init__(self):
        self.user32 = windll.user32
        self.kernel32 = windll.user32
        self.letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        self.shiftsymbols = "~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"
        self.delay = 0.01

    def press(self, key):
        self.user32.keybd_event(key, 0, 0, 0)
        sleep(self.delay)
        self.user32.keybd_event(key, 0, 2, 0)
        sleep(self.delay)

    def hold(self, key):
        self.user32.keybd_event(key, 0, 0, 0)
        sleep(self.delay)

    def release(self, key):
        self.user32.keybd_event(key, 0, 2, 0)
        sleep(self.delay)

class Mouse:
    def __init__(self):
        self.user32 = windll.user32
        self.kernel32 = windll.user32
        self.delay = 0.01

    def move(self, x, y):
        self.user32.SetCursorPos(x, y)

    def click(self, button):
        self.user32.mouse_event(button[0], 0, 0, 0, 0)
        sleep(self.delay)
        self.user32.mouse_event(button[1], 0, 0, 0, 0)
        sleep(self.delay)

    def holdclick(self, button):
        self.user32.mouse_event(button[0], 0, 0, 0, 0)
        sleep(self.delay)

    def releaseclick(self, button):
        self.user32.mouse_event(button[1])
        sleep(self.delay)
