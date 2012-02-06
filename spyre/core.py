import __future__
import json
import errors
from httpclient import HTTPClient
from spyre.method import Method


class Spore(object):

    def __init__(self, spec_string=None, base_url=None):
        self.authentication = None
        self.middlewares = []
        self.formats = []
        self._methods = []
        self.user_agent = HTTPClient()

        if spec_string is not None:
            try:
                spec = json.loads(spec_string)
            except:
                raise errors.SpyreObjectBuilder("can't load specs")

        self._init_meta(spec, base_url)
        self._init_methods(spec)

    # TODO method to validate spec
    # TODO method to list available SPORE methods
    # TODO method to search for a given method
    def _init_meta(self, spec, base_url=None):
        self.name = spec['name']  # XXX see later what to do with this

        if base_url is None:
            base_url = spec.get('base_url', None)
            if base_url is None:
                raise errors.SpyreObjectBuilder('base_url is missing')
        self.base_url = base_url

        formats = spec.get('formats', None)
        authentication = spec.get('authentication', None)

        if formats is not None:
            self.formats = formats

        if authentication is not None:
            self.authentication = authentication

    def _init_methods(self, spec):
        # XXX check if method already exists
        for method_name, method_desc in spec['methods'].iteritems():
            self._attach_method(method_name, method_desc)

    def _attach_method(self, method_name, method_desc):
        try:
            new_method = Method(
                method_name,
                method_desc,
                base_url=self.base_url,
                user_agent=self.user_agent,
                middlewares=self.middlewares
            )
        except Exception, e:
            raise RuntimeError(e)  # XXX meh

        setattr(self, method_name, new_method)
        self._methods.append(method_name)

    def enable_if(self, predicate, middleware, **kwargs):
        pass

    def enable(self, middleware, **kwargs):
        predicate = lambda req: True
        if type(middleware) is str:
            mw_class = self._import_middleware(middleware)
            self.middlewares.append((predicate, mw_class(**kwargs)))
        elif callable(middleware):
            self.middlewares.append((predicate, middleware(**kwargs)))
        else:
            raise ValueError(middleware)

    def _import_middleware(self, mw_name):
            mw_package = "spyre.middleware.%s" % mw_name
            mw_module = __import__(mw_package, fromlist=[mw_name])
            mw_class = getattr(mw_module, mw_name)
            return mw_class
