from spyre.middleware import Middleware
from functools import partial
import json


class formatjson(Middleware):
    def __init__(self, **kwargs):
        pass

    def __call__(self, env):
        cb = partial(self.response_cb)
        return cb

    def response_cb(self, response):
        import inspect
        print 'caller name:', inspect.stack()[1][3]
        response.content = json.loads(response.content)
