from types import MalException, MalList

class Env(object):
    def __init__(self, outer, binds=[], exprs=[]):
        self.data = {}
        self.outer = outer

        # bind parameter values to names
        for i in range(len(binds)):
            bind = binds[i]
            if bind == '&': # variable-length args as list
                self.set(binds[i+1], MalList(exprs[i:]))
                break
            self.set(bind, exprs[i])

    def set(self, key, value):
        self.data[key] = value
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
            raise MalException("Symbol %s is not defined" % key)
        return env.data[key]