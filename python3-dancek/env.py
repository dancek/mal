from types import MalException, MalType

class Env(object):
    def __init__(self, outer):
        self.data = {}
        self.outer = outer

    def set(self, key, value):
        k = key
        if isinstance(key, MalType):
            k = key.content
        self.data[k] = value
        return value

    def find(self, key):
        if key in self.data.keys():
            return self
        elif self.outer == None:
            return None
        else:
            return self.outer.find(key)

    def get(self, key):
        env = self.find(key)
        if env == None:
            raise MalException("Symbol %s is not defined")
        return env.data[key]