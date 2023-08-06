_SHELL = True

import sys
import msvcrt
import cursor
from ctypes import windll

_CLEAR = '\033[2J'
_MOVE_DOWN = '\033[B'
_MOVE_LEFT = '\033[D'
_MOVE_TO = '\033[%(y)d;%(x)dH'
_FG_24 = '\033[38;2;%d;%d;%dm'
_BG_24 = '\033[48;2;%d;%d;%dm'
_RESET_FORMAT = '\033[0m'

UP = '🡡'
DOWN = '🡣'
LEFT = '🡠'
RIGHT = '🡢'

class Window:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def writeText(self, text, *, fg: tuple[int]=None, bg: tuple[int]=None, pos=(0, 0)):
        print(_MOVE_TO % {'x':self.x + pos[0] + 1, 'y':self.y + pos[1] + 1}, end='', file=sys.__stdout__)
        text = text.splitlines()
        text = ''.join(x + len(x) * _MOVE_LEFT + _MOVE_DOWN for x in text)
        print(('' if fg is None else _FG_24 % fg), ('' if bg is None else _BG_24 % bg),
              text, _RESET_FORMAT, end=_MOVE_TO % {'x':1, 'y':1}, sep='', file=sys.__stdout__)
        if _SHELL:
            showAll()

def showAll():
    sys.__stdout__.flush()

def getKey():
    k = msvcrt.getch()
    if k == b'\xe0':
        match k := msvcrt.getch():
            case b'H':
                return UP
            case b'P':
                return DOWN
            case b'K':
                return LEFT
            case b'M':
                return RIGHT
            case _:
                return chr(0x2700 + k[0])
    elif k == b'\0':
        match k := msvcrt.getch():
            case b'\0':
                return '\0'
            case _:
                return chr(0x3400 + k[0])
    elif k == b'\3':
        showCursor()
        raise KeyboardInterrupt
    else:
        return k.decode('852') # Dla języka polskiego

def hideCursor():
    cursor.hide()

def showCursor():
    cursor.show()

def skipGetKey():
    msvcrt.ungetch(b'\0')
    msvcrt.ungetch(b'\0')

def clearScreen():
    print(_RESET_FORMAT + _CLEAR, end='', file=sys.__stdout__)

k = windll.kernel32
k.SetConsoleMode(k.GetStdHandle(-11), 7)
del k
clearScreen()
sys.__stdout__.flush()

if __name__ == '__main__':
    w = Window(5, 5)
    w.writeText('Spam', fg=(0, 255, 0), bg=(255, 0, 0), pos=(-2, -2))
