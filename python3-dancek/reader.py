import re
from types import *

TOKENIZER_RE = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)''')

INT_RE = re.compile('-?\d+')

class Reader(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        token = self.tokens[self.position]
        self.position += 1
        return token

    def peek(self):
        token = self.tokens[self.position]
        return token

def read_str(s):
    tokens = tokenizer(s)
    reader = Reader(tokens)
    return read_form(reader)

def tokenizer(s):
    return TOKENIZER_RE.findall(s)

def read_form(reader):
    first_token = reader.peek()
    if first_token == '(':
        return read_list(reader)
    elif first_token == '[':
        return read_list(reader, MalVector)
    else:
        return read_atom(reader)

def read_list(reader, type=MalList):
    reader.next()
    ls = []
    while True:
        token = reader.peek()
        if token == type.terminator:
            reader.next()
            return type(ls)
        elif token == '': # EOF too early
            raise MalException("expected '%s', got EOF", type.terminator)
        else:
            ls.append(read_form(reader))

def read_atom(reader):
    atom = reader.next()
    if INT_RE.fullmatch(atom):
        return int(atom)
    elif atom.startswith('"'):
        return MalString(atom[1:-1])
    else:
        return MalSymbol(atom)