def spore_method(name, spec):
    class spore_method_handler(object):
        def __init__(self, name):
            pass

def new_from_spec(name, spec=None, **named):
    if not spec:
        spec = named
    dic = {
        'spore_spec': spec,
    }
    if 'methods' in spec:
        for mname, mspec in spec['methods'].iteritems():
            spore_method = spore_method(mname, mspec)
            dic[mname] = spore_method
    return type(name, (spore_base,), dic)

class spore_meta(object):
    def __init__(class, name, bases, dic):
        for mname in self.spore_spec:
            self.__getattr__(mname).__get__(self)
