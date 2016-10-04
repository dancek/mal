class MalType(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.content)

class MalString(MalType):
    pass

class MalSymbol(MalType):
    pass

class MalList(MalType):
    pass


class MalException(Exception):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content
