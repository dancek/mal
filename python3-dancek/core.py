import printer
from types import MalList

def pr_str(*args):
    return ' '.join(map(printer.pr_str, args))

def str_(*args):
    return ''.join(map(lambda x: printer.pr_str(x, False), args))

def prn(*args):
    print(' '.join(map(printer.pr_str, args)))

def println(*args):
    print(' '.join(map(lambda x: printer.pr_str(x, False), args)))

ns = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: int(a/b),
    'pr-str': pr_str,
    'str': str_,
    'prn': prn,
    'println': println,
    'list': lambda *args: MalList(args),
    'list?': lambda xs: isinstance(xs, MalList),
    'empty?': lambda xs: len(xs) == 0,
    'count': lambda xs: len(xs) if isinstance(xs, MalList) else 0,
    '=': lambda a,b: a == b,
    '<': lambda a,b: a < b,
    '<=': lambda a,b: a <= b,
    '>': lambda a,b: a > b,
    '>=': lambda a,b: a >= b,
}
