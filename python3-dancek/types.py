class MalString(str):
    pass

class MalSymbol(str):
    pass

class MalKeyword(str):
    pass

class MalList(list):
    terminator = ')'

class MalVector(list):
    terminator = ']'

class MalHashmap(dict):
    terminator = '}'

    def __init__(self, list_or_dict):
        if isinstance(list_or_dict, list) or isinstance(list_or_dict, tuple):
            # constructed from alternating keys and values
            dict.__init__(self, zip(list_or_dict[::2], list_or_dict[1::2]))
        else:
            dict.__init__(self, list_or_dict)

class MalException(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return str(self.description)

class MalFunction(object):
    def __init__(self, ast, params, env, fn, is_macro=False):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro

    def __call__(self, *args):
        return self.fn(*args)

class MalAtom(object):
    def __init__(self, target):
        self.set(target)

    def set(self, target):
        self.target = target
        return target

class CommentException(Exception):
    pass