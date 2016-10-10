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
        if self.eof():
            return None
        token = self.tokens[self.position]

        # skip comments
        while token.startswith(';'):
            #print('skipping %s' % token)
            self.position += 1
            if self.eof():
                return None
            token = self.tokens[self.position]

        return token

    def eof(self):
        """Is the reader at the end of the string?

        This is not in the MAL guide, but I find it useful."""
        return self.position >= len(self.tokens)

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

    # data structures
    if first_token == '(':
        return read_list(reader)
    elif first_token == '[':
        return read_list(reader, MalVector)
    elif first_token == '{':
        return read_list(reader, MalHashmap)

    # reader macros
    elif first_token == "'":
        return reader_macro(reader, 'quote')
    elif first_token == "`":
        return reader_macro(reader, 'quasiquote')
    elif first_token == "~":
        return reader_macro(reader, 'unquote')
    elif first_token == "~@":
        return reader_macro(reader, 'splice-unquote')
    elif first_token == "@":
        return reader_macro(reader, 'deref')

    # atoms
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
        elif token == '' or reader.eof(): # EOF too early
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
        s = atom[1:-1]
        unescaped = s \
            .replace('\\"', '"') \
            .replace('\\n', '\n') \
            .replace('\\\\', '\\')
        return MalString(unescaped)
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

def reader_macro(reader, symbol):
    reader.next()
    return MalList([MalSymbol(symbol), read_form(reader)])