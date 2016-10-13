import time

import printer, reader
from types import *

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

# deep equality that checks type but considers MalList and MalVector the same
def equals(a, b):
    if a == b and type(a) == type(b):
        return True
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return all(equals(a_, b_) for a_, b_ in zip(a,b))
    else:
        return False

def nth(xs, i):
    try:
        return xs[i]
    except IndexError:
        raise MalException("Index %d out of bounds for %s" % (i, xs))

def throw(msg):
    raise MalException(msg)

def conj(xs, *ys):
    if isinstance(xs, MalList):
        return MalList(list(ys[::-1]) + xs)
    elif isinstance(xs, MalVector):
        return MalVector(xs + list(ys))

def seq(xs):
    if not xs:
        return None

    # convert as follows:
    # MalList -> MalList
    # MalVector -> MalList
    # MalString -> MalList (containing each character)
    return MalList(xs)

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
    'count': lambda xs: len(xs) if isinstance(xs, list) else 0,
    '=': equals,
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
    'nth': nth,
    'first': lambda xs: xs[0] if xs else None,
    'rest': lambda xs: MalList(xs[1:] if xs else []),
    'throw': throw,
    'apply': lambda f, *args: f(*(list(args[:-1]) + args[-1])),
    'map': lambda f, xs: MalList(map(f, xs)),
    'nil?': lambda x: x is None,
    'true?': lambda x: x is True,
    'false?': lambda x: x is False,
    'string?': lambda x: isinstance(x, MalString),
    'symbol?': lambda x: isinstance(x, MalSymbol),
    'keyword?': lambda x: isinstance(x, MalKeyword),
    'map?': lambda x: isinstance(x, MalHashmap),

    'symbol': lambda s: MalSymbol(s),
    'keyword': lambda s: MalKeyword(':' + s),
    'vector': lambda *xs: MalVector(xs),
    'vector?': lambda x: isinstance(x, MalVector),
    'hash-map': lambda *xs: MalHashmap(xs),
     # this assoc impl requires Python 3.5 (PEP 448) for multiple unpackings!
    'assoc': lambda dct, *xs: MalHashmap({**dct, **MalHashmap(xs)}),
    'dissoc': lambda dct, *rm: MalHashmap({k:v for k,v in dct.items() if k not in rm}),
    'get': lambda dct, key: dct.get(key, None) if dct else None,
    'contains?': lambda dct, key: key in dct,
    'keys': lambda dct: MalList(dct.keys()),
    'vals': lambda dct: MalList(dct.values()),
    'sequential?': lambda x: isinstance(x, list),

    'readline': lambda prompt: input(prompt),
    'meta': lambda x: x.metadata if hasattr(x, 'metadata') else None,
    'with-meta': MalFunction.with_metadata,
    'time-ms': lambda: int(time.time() * 1000),
    'conj': conj,
    'seq': seq,
}
