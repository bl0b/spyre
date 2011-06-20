

class http_call(object):
    pass

class spore(object):
    def __init__(self, spec):
        for method_name, method in spec['methods'].iteritems():
            self.__setattr__(method_name, http_call(method))

