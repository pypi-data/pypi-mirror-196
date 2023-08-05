import random, os, sys
from enum import Flag, auto

class FStat(Flag):
    TRACKED = auto() # The file is tacked by git
    CONFLICT = auto() # The local and remote files are in conflict
    GPG = auto() # The file is currently encrypted
    REM = auto() # The file has been removed,
    NOEXIST = auto() # The file does not exist


class File():
    def __init__(self, fname, flags=None):
        self.fname = fname
        self.flags = flags


    def __str__(self):
        return self.fname


    def __contains__(self, other):
        return other in self.flags


    def pretty(self):
        style = 'w,.'
        if FStat.CONFLICT in self: style = 'err'
        elif FStat.REM in self: style = 'm!'
        elif FStat.GPG in self and FStat.TRACKED not in self: style = 'g!'
        elif FStat.NOEXIST not in self and FStat.GPG in self: style = 'y_'
        elif FStat.TRACKED not in self and File.GPG not in self: style = 'w!;'
        icon = '💀' if self&File.REM else '🔒' if self&File.GPG else '  '
        return f'{icon}\b{style} {self}'


    def __eq__(self, other):
        return self.fname == str(other)#os.path.abspath(self.fname) == os.path.abspath(str(other))


    def __lt__(self, other):
        a = self.fname.split('/')
        b = str(other).split('/')
        if len(a) != len(b): return len(b) < len(a)
        i = 0
        while i < len(a) and a[i] == b[i]: i += 1
        return a[i] < b[i]


    def __and__(self, other):
        return self.flags & other


    def __bool__(self):
        return self.flags != None


    def matches(self, paths):
        for p in paths:
            if p.endswith('/'):
                if p == './' or self.fname.startswith(p): return p
            elif self.fname == p: return p


    def secure_delete(self):
        rbytes = random.randbytes(os.stat(self.fname).st_size)
        with open(self.fname, 'wb') as f:
            f.write(rbytes)
        os.remove(self.fname)
