import os
import sys
import fcntl, termios, struct

__all__ = ['lightkeeper', 'node', 'server']

def progname(module, command):
    module_name = module.split('.')[-1]
    return '%s %s %s' % (os.path.basename(sys.argv[0]), module_name, command)

class CommandWrapper:
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func
        self.doc = func.func_doc
        self.name = func.__name__
        self.module = func.__module__
        self.parser.description = func.func_doc
        self.parser.prog = progname(func.__module__, func.__name__)

    def call(self, args):
        if self.func.__name__ == 'log':
            optargs, unknown = self.parser.parse_known_args(args)
            self.func((optargs, unknown))
        else:
            optargs = self.parser.parse_args(args)
            self.func(optargs)

def cmd(parser):
    def decorator(func):
        return CommandWrapper(parser, func)
    return decorator

def terminal_size():
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

def print_divider(char='-'):
    max_w, max_h = terminal_size()
    print char * max_w

def print_line(line):
    max_w, max_h = terminal_size()
    if len(line) > max_w:
        print line[:max_w]
    else:
        print line

def format_lines(lines, rjust = True):
    maxlens = [0 for _ in lines[0]]
    for line in lines:
        for idx, column in enumerate(line):
            if column is None: continue
            if maxlens[idx] < len(column):
                maxlens[idx] = len(column)
    for line in lines:
        for idx, column in enumerate(line):
            if column is None: continue
            if rjust:
                print column.rjust(maxlens[idx] + 1)
            else:
                print column.ljust(maxlens[idx] + 1)
    print
