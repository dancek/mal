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

class MalFunction(object):
    def __init__(self, ast, params, env, fn, is_macro=False, metadata=None):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro
        self.metadata = metadata

    def __call__(self, *args):
        return self.fn(*args)

    @staticmethod
    def with_metadata(f, metadata):
        # allow setting metadata on core functions too
        if not isinstance(f, MalFunction):
            return MalFunction(None, None, None, f, False, metadata)
        return MalFunction(f.ast, f.params, f.env, f.fn, f.is_macro, metadata)

class MalAtom(object):
    def __init__(self, target):
        self.set(target)

    def set(self, target):
        self.target = target
        return target

class CommentException(Exception):
    pass