import re
import sys as _sys
class __black__:
    def __str__(self):
        return "\033[90m"
    def __add__(self, other: str):
        return "\033[90m" + other
    def __radd__(self, other: str):
        return other + "\033[90m"
    normal = "\033[30m"
    dark = "\033[2;30m"
class __red__:
    def __str__(self):
        return "\033[91m"
    def __add__(self, other: str):
        return "\033[91m" + other
    def __radd__(self, other: str):
        return other + "\033[91m"
    normal = "\033[31m"
    dark = "\033[2;31m"
class __green__:
    def __str__(self):
        return "\033[92m"
    def __add__(self, other: str):
        return "\033[92m" + other
    def __radd__(self, other: str):
        return other + "\033[92m"
    normal = "\033[32m"
    dark = "\033[2;32m"
class __yellow__:
    def __str__(self):
        return "\033[93m"
    def __add__(self, other: str):
        return "\033[93m" + other
    def __radd__(self, other: str):
        return other + "\033[93m"
    normal = "\033[33m"
    dark = "\033[2;33m"
class __blue__:
    def __str__(self):
        return "\033[94m"
    def __add__(self, other: str):
        return "\033[94m" + other
    def __radd__(self, other: str):
        return other + "\033[94m"
    normal = "\033[34m"
    dark = "\033[2;34m"
class __purple__:
    def __str__(self):
        return "\033[95m"
    def __add__(self, other: str):
        return "\033[95m" + other
    def __radd__(self, other: str):
        return other + "\033[95m"
    normal = "\033[35m"
    dark = "\033[2;35m"
class __cyan__:
    def __str__(self):
        return "\033[96m"
    def __add__(self, other: str):
        return "\033[96m" + other
    def __radd__(self, other: str):
        return other + "\033[96m"
    normal = "\033[36m"
    dark = "\033[2;36m"
class __white__:
    def __str__(self):
        return "\033[97m"
    def __add__(self, other: str):
        return "\033[97m" + other
    def __radd__(self, other: str):
        return other + "\033[97m"
    normal = "\033[37m"
    dark = "\033[2;37m"

off = "\033[0m"
black = __black__()
red = __red__()
green = __green__()
yellow = __yellow__()
blue = __blue__()
purple = __purple__()
cyan = __cyan__()
white = __white__()

def setoff():
    _sys.stdout.write("\033[0m")
    _sys.stdout.flush()
class __toningName(type):
    def __repr__(cls):
        return f"<RGB color.toning({cls.R}, {cls.G}, {cls.B}) id={id(cls)}>"
class toning(str, metaclass=__toningName):
    def __new__(cls, R = 255, G: int = 255, B: int = 255, text: str = None):
        cls.R, cls.G, cls.B = R, G, B
        if type(cls.R) is str:
            RGB = []
            for i in (0, 2, 4):
                RGB.append(int(cls.R[i: i+2], 16))
            cls.R, cls.G, cls.B = RGB
        if text is not None: obj = f"\033[38;2;{cls.R};{cls.G};{cls.B}m{text}\033[0m"
        obj = f"\033[38;2;{cls.R};{cls.G};{cls.B}m"
        return str.__new__(cls, obj)
        
    #def background(self.R: int = 255, self.G: int = 255, self.B: int = 255, text: str = None):
    #    if type(self.R) is str:
    #        RGB = []
    #        for i in (0, 2, 4):
    #            RGB.append(int(self.R[i: i+2], 16))
    #        self.R, self.G, self.B = RGB
    #    if text is not None: return f"\033[48;2;{self.R};{self.G};{self.B}m{text}\033[0m"
    #    return f"\033[48;2;{self.R};{self.G};{self.B}m"

def remove_7bit(text):
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub("", text)

def remove(text):
    # remove 8 bit content
    return re.compile(r'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])').sub("", text)

def hex_convert(rh: str or list or tuple):
    rh = rh.strip("#") if type(rh) is str else rh
    return "#%02x%02x%02x" % tuple(rh) if type(rh) in (list, tuple) else tuple(int(rh[i: i+2], 16) for i in (0, 2, 4))

def color(C: str or list or tuple, obj: str = "font"):
    try:
        C = hex_convert(C) if type(C) is str else tuple(C)
        return toning.font(*C) if "f" in obj else toning.background(*C)
    except ValueError:
        try:
            return globals()[C.lower()]
        except KeyError:
            if "light" in C.lower():
                return globals()[C.lower().replace("light", "").strip()]
            if "dark" in C.lower():
                return globals()[C.lower().replace("dark", "").strip()].dark
            if "normal" in C.lower():
                return globals()[C.lower().replace("normal", "").strip()].normal
            else:
                return None