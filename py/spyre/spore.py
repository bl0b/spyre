import spore.request


def spore_method(name, spec):
    class spore_method_handler(object):
        def __init__(self, name):
            self.im_func = self
            self.im_self = None
            self.im_class = spore_method_handler
            self.name = name
            self.req = spec['required_params']
            self.opt = safe(spec, 'optional_params', [])
            self.path = spec['path']
            self.method = spec['method']

        def __check_args(self, args, kwargs):
            return validate_arguments(self, args, kwargs)

        def expand(self, txt, dic):
            for k, v in dic.iteritems():
                txt = v.join(txt.split(':' + k))
            return txt

        def __call__(self, spo, *args, **kwargs):
            try:
                arg_dic = self.__check_args(args, kwargs)
                env = {
                    'REQUEST_METHOD' = self.method,
                }
                spo._exec_call(request(method=self.method, url=self.expand(self.path, arg_dic)))
            except http_call_exception, hce:
                print hce
                if http_call_fail_silently:
                    return None
                else:
                    raise hce

        def __get__(self, i, c):
            ret = lambda *a, **k: self(i, *a, **k)
            ret.__doc__ = self.__doc__
            ret.__name__ = str(self.name)
            return ret

    return spore_method_handler


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
