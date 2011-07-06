__all__ = ['new_from_spec']

safe = lambda d, k,t=None: k in d and d[k] or t

class spore_base(object):
    def __init__(self):
        self.middlewares = []
        for mname in self.spore_spec:
            self.__getattr__(mname).__get__(self)
    def _iter_middlewares(self, req):
        return (mw_func(req) for mw_pred, mw_func in self.middlewares if mw_pred(req))
    def _run_middlewares(self, req, mwlist):
        return map(lambda mw: mw(req), mwlist)
    def enable(self, middleware, **kwargs):
        self.enable_if(lambda req: True, middleware, **kwargs)
    def enable_if(self, predicate, middleware, **kwargs):
        if type(middleware) is str:
            midmod = __import__(middleware, fromlist=['new']) # we actually get the whole module, the whole namespace
            self.middlewares.append( (predicate, midmod.new(**kwargs)) )
        elif callable(middleware):
            self.middlewares.append( (predicate, middleware(**kwargs)) )
        else:
            raise ValueError(middleware)
    def _exec_call(self, req):
        resp_callbacks = self._run_middlewares(req, self._iter_middlewares(req))
        # perform actual call with req
        resp = None#FIXME
        self._run_middlewares(resp, reversed(resp_callbacks))
        return resp




def new_from_spec(name, spec=None, **named):
    if not spec:
        spec = named
    # uncomment to override spec with given named args
    #spec.update(named)
    dic = {
        #'SPoREwashere': 42,
        '__doc__': safe(spec, 'documentation', '')+'\n'+str(spec),
        'version': safe(spec, 'version', 'please specify me'),
        'base_url': safe(spec, 'base_url', 'perdu.com'),
        'spore_spec': spec
    }
    if 'methods' in spec:
        for mname, mspec in spec['methods'].iteritems():
            hc = http_call(mname, mspec)
            dic[mname] = hc
    return type(name, (spore_base,), dic)

