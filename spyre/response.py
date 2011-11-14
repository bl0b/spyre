class Response(object):

    def __init__(self, env, status, resp, content):
        self.env = env
        self.status = status
        self.code = status
        self.resp = resp
        self.content = content
        self.content_type = resp.get('content-type')
        self.content_length = resp.get('content-length')

        if status >= 200 and status < 300:
            self.is_success = True
        else:
            self.is_success = False

    def finalize(self):
        pass
