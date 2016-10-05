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
