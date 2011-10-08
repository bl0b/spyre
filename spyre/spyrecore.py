import __future__


class spyrecore(object):
    def __init__(self, json):
        self.json = json
        self._init_meta(json)
        self._init_methods(json)

    def _init_meta(self, json):
        self.name = json['name']

    def _init_methods(self, json):
        for method_name, method_desc in json['methods'].iteritems():
            self._attach_method(method_name, method_desc)

    def _attach_method(self, method_name, method_desc):
        setattr(self, method_name, httpcall(method_name, method_desc))


class httpcall(object):
    def __init__(self, name, desc):
        self.name = name

    def __call__(self):
        return 5
