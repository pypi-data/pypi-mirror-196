import os as _os
import sys as _sys
import string as _string
from . import color as _color

__oldround = round

def getFloat(obj: float, reType=str):
    _obj = str(obj)
    dec = []
    for index in range(1, len(_obj)):
        if _obj[-index] == ".": break
        else: dec.append(_obj[-index])
    dec.reverse()
    return reType("".join(dec))
def round(obj: float, _to: int = 0):
    if not _to: return __oldround(obj)
    if len(str(getFloat(obj))) < _to:
        return __oldround(obj, _to)
    decimals = list(str(getFloat(obj)))
    count = 1
    AddOne = False
    if len(decimals) == 1: 
        if int(decimals[0]) == 0: return obj
        else: return round(obj)
    try:
        if int(decimals[_to]) >= 5:
            decimals[_to - 1] = str(int(decimals[_to - 1]) + 1)
    except IndexError:
        count = 1
        while True:
            try:
                if int(decimals[_to - count]) >= 5:
                    decimals[_to - 1] = str(int(decimals[_to - 1]) + 1)
                break
            except IndexError: continue
    del decimals[_to: len(decimals)]
    while int(decimals[_to - count]) == 10:
        if _to - count <= 0: decimals[_to - count] = "0"; AddOne = True; break
        decimals[_to - count] = "0"
        decimals[_to - count - 1] = str(int(decimals[_to - count - 1]) + 1)
        count += 1
    decimals = "".join(decimals)
    Object = str(int(obj))
    res = Object + "." + decimals
    if AddOne: return float(res) + 1
    else: return float(res)
def getIndex(a: list, start=0, end=0): return range(start, len(a) + end)
def center(size):
    cols, rows = _shutil.get_terminal_size()
    space = int(cols / 2 - len(string) / 2)
    return " " * space
def zip(listA, listB):
    for count in range(len(listA if len(listA) > len(listB) else listB)):
        aItem = listA[count] if len(listA) > count else None
        bItem = listB[count] if len(listB) > count else None
        yield (aItem, bItem)

class Cursor:
    def __init__(self):
        self._ci = None
        if _os.name == "nt":
            self._msvcrt = __import__("msvcrt")
            self._ctypes = __import__("ctypes")
            class _CursorInfo(self._ctypes.Structure):
                _fields_ = [("size", self._ctypes.c_int), ("visible", self._ctypes.c_byte)]
            self._ci = _CursorInfo()
    def hide(self):
        if _os.name == "nt":
            handle = self._ctypes.windll.kernel32.GetStdHandle(-11)
            self._ctypes.windll.kernel32.GetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
            self._ci.visible = False
            self._ctypes.windll.kernel32.SetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
        elif _os.name == "posix":
            _sys.stdout.write("\033[?25l")
            _sys.stdout.flush()
    def show(self):
        if _os.name == "nt":
            handle = self._ctypes.windll.kernel32.GetStdHandle(-11)
            self._ctypes.windll.kernel32.GetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
            self._ci.visible = True
            self._ctypes.windll.kernel32.SetConsoleCursorInfo(handle, self._ctypes.byref(self.ci))
        elif _os.name == "posix":
            _sys.stdout.write("\033[?25h")
            _sys.stdout.flush()
    if _os.name == "posix":
        def position(self):
            import re as _re
            import tty as _tty
            import termios as _termios
            _buffer = ""
            stdin = _sys.stdin.fileno()
            termios_attrs = _termios.tcgetattr(stdin)
            try:
                _tty.setcbreak(stdin, _termios.TCSANOW)
                _sys.stdout.write("\x1b[6n")
                _sys.stdout.flush()
                while True:
                    _buffer += _sys.stdin.read(1)
                    if _buffer[-1] == "R": break
            finally:
                _termios.tcsetattr(stdin, _termios.TCSANOW, termios_attrs)
            try:
                matches = _re.match(r"^\x1b\[(\d*);(\d*)R", _buffer)
                groups = matches.groups()
            except AttributeError:
                return None
            class pos: 
                def __init__(self, groups):
                    self.x = int(groups[1])
                    self.y = int(groups[0])
                    self.cols = int(groups[1])
                    self.lines = int(groups[0])
                def __str__(self):
                    return f"<cursor cols(x): {self.x} cursor lines(y): {self.y}>"
            return pos(groups)

if _os.name != "nt":    
    import termios as _termios
    class KeyEvent:
        def __init__(self):
            self.fd = _sys.stdin.fileno()
            self.oldttyInfo = _termios.tcgetattr(self.fd)
            self.newttyInfo = self.oldttyInfo[:]
            self.newttyInfo[3] &= ~_termios.ICANON
            self.newttyInfo[3] &= ~_termios.ECHO
            self.shiftKeys = ["\x08", "\x1bb", "\x1bf", "\x1b[Z"]
            self.ctrlKeys = ["\x1b\x7f", "\x1bd"]
            self.altKeys = ["\x1b[3~", "\x1bd", "\x1b[5~", "\x1b[6~"]
            self.shiftKeys.extend(tuple(_string.ascii_uppercase))
        def waitPress(self, sKeys):
            try:
                _termios.tcsetattr(self.fd, _termios.TCSANOW, self.newttyInfo)
                key = _os.read(self.fd, 7)
                sKeys["shift"] = 1 if key.decode("utf-8") in self.shiftKeys  else 0
                sKeys["ctrl"] = 1 if key.decode("utf-8") in self.ctrlKeys  else 0
                sKeys["alt"] = 1 if key.decode("utf-8") in self.altKeys else 0
                return key
            finally:
                _termios.tcsetattr(self.fd, _termios.TCSANOW, self.oldttyInfo)
        def oldConsole(self):
            _termios.tcsetattr(self.fd, _termios.TCSANOW, self.newttyInfo)
        def newConsole(self):
            _termios.tcsetattr(self.fd, _termios.TCSANOW, self.oldttyInfo)
        Up = "\x1b[A"
        Down = "\x1b[B"
        Left = "\x1b[D"
        Right = "\x1b[C"
        Enter = "\n"
        Tap = "\t"
        BackSpace = "\x7f"
        Space = " "
        
        
    
    