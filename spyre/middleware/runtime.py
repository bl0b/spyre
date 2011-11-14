from spyre.middleware import Middleware
from functools import partial
import datetime


class runtime(Middleware):
    def __init__(self, **kwargs):
        pass

    def __call__(self, env):
        start_time = datetime.datetime.now()
        cb = partial(self.response_cb, start_time)
        return cb

    def response_cb(self, start_time, response):
        req_time = datetime.datetime.now() - start_time
        response.env['X-Spore-RunTime'] = str(req_time)