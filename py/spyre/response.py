import urllib2

class Response:
    def __init__(self, env):
        self.status = 200
        self.code = self.status
        self.env = env
        
