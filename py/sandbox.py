import os, sys
import json


spec = """
{
    "base_url" : "http://github.com/api/v2/",
    "version" : "0.4",
    "methods" : {
        "user_search" : {
            "path" : "/:format/user/search/:search",
            "method" : "GET",
            "required_params" : [
                "format",
                "search"
            ]
        },
        "get_info" : {
            "path" : "/:format/user/show/:username",
            "method" : "GET",
            "required_params" : [
                "format",
                "username"
            ]
        },
        "get_profile" : {
            "path" : "/:format/user/show",
            "method" : "GET",
            "required_params" : [
                "format"
            ],
            "authentication" : true
        }
    }
}
"""

spec2 = """
{
    "base_url" : "http://api.twitter.com/1",
    "version" : "0.1",
    "methods" : {
        "public_timeline" : {
            "optional_params" : [
                "trim_user",
                "include_entities"
            ],
            "required_params" : [
                "format"
            ],
            "path" : "/statuses/public_timeline.:format",
            "method" : "GET"
        }
    }
}
"""


#        my $env = {
#            REQUEST_METHOD => $method->method,
#            SERVER_NAME    => $base_url->host,
#            SERVER_PORT    => $base_url->port,
#            SCRIPT_NAME    => (
#                $base_url->path eq '/'
#                ? ''
#                : $base_url->path
#            ),
#            PATH_INFO               => $method->path,
#            REQUEST_URI             => '',
#            QUERY_STRING            => '',
#            HTTP_USER_AGENT         => $self->api_useragent->agent,
#            'spore.expected_status' => [ $method->expected_status ],
#            'spore.authentication'  => $authentication,
#            'spore.params'          => $params,
#            'spore.payload'         => $payload,
#            'spore.errors'          => *STDERR,
#            'spore.url_scheme'      => $base_url->scheme,
#            'spore.formats'         => $formats,
#        };
#
#        $env->{'spore.form_data'} = $method->form_data
#          if $method->has_form_data;
#
#        $env->{'spore.headers'} = $method->headers if $method->has_headers;
#
#


class perlish(dict):
    def __init__(self, target):
        self.target = target
    def __getitem__(self, key):
        #try:
            return type.__getattribute__(self.target, key)
        #except AttributeError, ae:
        #    raise KeyError(key)


class http_call_exception(Exception):
    def __init__(self, *a, **k):
        Exception.__init__(self, *a, **k)


http_call_fail_silently = True

safe = lambda d, k,t=None: k in d and d[k] or t

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















# Add auto-completion and a stored history file of commands to your Python
# interactive interpreter. Requires Python 2.0+, readline. Autocomplete is
# bound to the Esc key by default (you can change it - see readline docs).
#
# Store the file in ~/.pystartup, and set an environment variable to point
# to it:  "export PYTHONSTARTUP=~/.pystartup" in bash.

import atexit
import os
import readline
import rlcompleter

historyPath = os.path.expanduser(os.getenv("PYHISTORY") and "../"+os.getenv("PYHISTORY") or "~/.pyhistory")

print "[HISTORY] Using", historyPath

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath

