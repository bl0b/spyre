class Request:
    def __init_(self, **env):
        self.env = env
        self.path = self.env['PATH_INFO']
        self.method = self.env['REQUEST_METHOD']
        self.port = self.env['SERVER_PORT']
        self.request_uri = self.env['REQUEST_URI']
        self.scheme = self.env['spore.scheme']
        self.script_name = self.env['SCRIPT_NAME']
        self.body = self.env['spore.payload']
        
    def finalize(self):
        pass

    def secure(self):
        return self.scheme == 'https'

    def uri(self, path_info=None, query_string=None):
        pass

