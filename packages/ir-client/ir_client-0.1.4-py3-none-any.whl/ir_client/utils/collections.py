from collections import OrderedDict


def defaultordereddict(default_factory):
    return DefaultOrderedDict(default_factory=default_factory)


class DefaultOrderedDict(OrderedDict):
    
    def __init__(self, default_factory):
        self.default_factory = default_factory
    
    def __missing__(self, key):
        self[key] = value = self.default_factory()
        return value
