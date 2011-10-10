class spyreresponse(object):

    def __init__(self, env, status, resp, content):
        self.env = env
        self.status = status
        self.resp = resp
        self.content = content
