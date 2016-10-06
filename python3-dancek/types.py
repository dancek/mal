class MalString(str):
    pass

class MalSymbol(str):
    pass

class MalList(list):
    terminator = ')'

class MalVector(list):
    terminator = ']'

class MalException(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description

class MalFunction(object):
    def __init__(self, ast, params, env, fn):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn

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