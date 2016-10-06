import printer, reader
from types import MalList, MalString, MalAtom

def pr_str(*args):
    return MalString(' '.join(map(printer.pr_str, args)))

def str_(*args):
    return MalString(''.join(map(lambda x: printer.pr_str(x, False), args)))

def prn(*args):
    print(' '.join(map(printer.pr_str, args)))

def println(*args):
    print(' '.join(map(lambda x: printer.pr_str(x, False), args)))

def slurp(filename):
    with open(filename) as f:
        return MalString(f.read())

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
    '=': lambda a,b: a == b and type(a) == type(b),
    '<': lambda a,b: a < b,
    '<=': lambda a,b: a <= b,
    '>': lambda a,b: a > b,
    '>=': lambda a,b: a >= b,
    'read-string': reader.read_str,
    'slurp': slurp,
    'atom': lambda x: MalAtom(x),
    'atom?': lambda x: isinstance(x, MalAtom),
    'deref': lambda atom: atom.target,
    'reset!': lambda atom, target: atom.set(target),
    'swap!': lambda atom, f, *args: atom.set(f(atom.target, *args)),
    '*ARGV*': MalList([]),
    'cons': lambda x, tail: MalList([x] + tail),
    'concat': lambda *args: MalList(sum(args, [])),
}
