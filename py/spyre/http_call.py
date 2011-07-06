__all__ = ['http_call', 'http_call_exception']



http_call_fail_silently = True




class http_call_exception(Exception):
    def __init__(self, *a, **k):
        Exception.__init__(self, *a, **k)


# external definition
def validate_arguments(self, args, kwargs):
    arg_dic = None
    # if using unnamed arguments (assumedly ONLY unnamed arguments)
    if args:
        if len(args)<len(self.req) or len(args) > (len(self.req)+len(self.opt)):
            # we bad
            if self.opt:
                raise http_call_exception("Invalud argument count : expected between %i and %i arguments, got %i instead"%(len(self.req), len(self.opts), len(args)))
            else:
                raise http_call_exception("Invalud argument count : expected %i arguments, got %i instead"%(len(self.req), len(args)))
        else:
            # we good
            arg_dic = dict(zip(self.req+self.opt, args))
    else:
        # otherwise we're using named arguments, just perform checks
        kset = set(kwargs.iterkeys())   # all provided named arguments
        req = set(self.req)             # all required arguments
        opt = set(self.opt)             # all optional arguments
        params = req.union(opt)         # all possible arguments
        stuff_remains = kset.difference(req+opt)
        if stuff_remains:
            raise http_call_exception("Unknown argument names : "+', '.join(stuff_remains)+' (only the following names are defined :'+', '.join(params)+')')
        missing_req = req.difference(kset)
        if missing_req:
            raise http_call_exception("Missing arguments : "+', '.join(missing_req))
        arg_dic = kwargs
    return arg_dic


def http_call(name, spec):
    class http_call_handler(object):
        __doc__ = (""+safe(spec, 'documentation', '')+'\n'+spec['method']+' '+spec['path']).strip()

        def __init__(self, name):
            self.im_func = self
            self.im_self = None
            self.im_class = http_call_handler
            self.name = name
            self.req = spec['required_params'] # this one MUST NOT fail, so let the exception go
            self.opt = safe(spec, 'optional_params', [])
            self.authentication = safe(spec, 'authentication', False)=='true'
            self.path = spec['path']
            self.method = spec['method']

        def __check_args(self, args, kwargs):
            return validate_arguments(self, args, kwargs)

        def expand(self, txt, dic):
            for k, v in dic.iteritems():
                txt = v.join(txt.split(':'+k))
            return txt

        def __call__(self, spo, *args, **kwargs):
            try:
                arg_dic = self.__check_args(args, kwargs)
                print "I should do some HTTP stuff but instead I'll print the method argument dictionary"
                print arg_dic
                spo._exec_call(request(method=self.method, url=self.expand(self.path, arg_dic)))
            except response, resp:
                return resp

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


    return http_call_handler(name)
