import re
from types import *

TOKENIZER_RE = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""")

INT_RE = re.compile('-?\d+')

class Reader(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        token = self.peek()
        self.position += 1
        return token

    def peek(self):
        if self.position >= len(self.tokens):
            return None
        token = self.tokens[self.position]

        # skip comments
        while token.startswith(';'):
            #print('skipping %s' % token)
            self.position += 1
            if self.position >= len(self.tokens):
                return None
            token = self.tokens[self.position]

        return token

def read_str(s):
    tokens = tokenizer(s)
    #print(tokens)
    reader = Reader(tokens)
    form = read_form(reader)
    #print(form)
    return form

def tokenizer(s):
    return TOKENIZER_RE.findall(s)

def read_form(reader):
    first_token = reader.peek()
    if first_token == '(':
        return read_list(reader)
    elif first_token == '[':
        return read_list(reader, MalVector)
    elif first_token == '{':
        return read_list(reader, MalHashmap)
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
            raise MalException("expected '%s', got EOF" % type.terminator)
        else:
            ls.append(read_form(reader))

def read_atom(reader):
    atom = reader.next()
    if atom is None:
        return None
    elif INT_RE.fullmatch(atom):
        return int(atom)
    elif atom.startswith('"'):
        return MalString(atom[1:-1])
    elif atom.startswith(':'):
        return MalKeyword(atom)
    elif atom == 'nil':
        return None
    elif atom == 'true':
        return True
    elif atom == 'false':
        return False
    else:
        return MalSymbol(atom)