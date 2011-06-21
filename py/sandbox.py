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

class http_call_exception(Exception):
    def __init__(self, *a, **k):
        Exception.__init__(self, *a, **k)



def http_call(spo, spec):
    class http_call_handler(object):
        __doc__ = ""+('documentation' in spec and spec['documentation'] or spec['method']+' '+spec['path'])
        def __init__(self, spo):
            self.spo = spo
            self.req = spec['required_params']
            self.opt = spec['optional_params']
            self.authentication = 'authentication' in spec and spec['authentication']=='true' or False
        def __check_args(self, args, kwargs):
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
                kset = set(kwargs.iterkeys())
                req = set(self.req)
                opt = set(self.opt)
                params = req.union(opt)

                stuff_remains = kset.difference(self.req+self.opt)
                if stuff_remains:
                    raise http_call_exception("Unknown argument names : "+', '.join(stuff_remains)+' (only the following names are defined :'+', '.join(params)+')')
                missing_req = req.difference(kset)
                if missing_req:
                    raise http_call_exception("Missing arguments : "+', '.join(missing_req))
                arg_dic = kwargs
            return arg_dic

        def __call__(self, *args, **kwargs):
            try:
                arg_dic = self.__check_args(args, kwargs)
                print "I should do some HTTP stuff but instead I'll print the method argument dictionary"
                print arg_dic
            except http_call_exception, hce:
                print hce
                return None
    return http_call_handler(spo)


class spore(object):
    def __init__(self, spec):
        for method_name, method in spec['methods'].iteritems():
            self.__setattr__(method_name, http_call(method))


def make_adhoc_class(cspec):
    pass













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

