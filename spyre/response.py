class Response(object):

    is_success = False

    def __init__(self, env, status=200, headers=None, content=None):
        self.env = env
        self._headers = headers

        self.status = status
        self.code = status

        if self._headers is not None:
            self.content_type = self._headers.get('content-type', None)
            self.content_length = self._headers.get('content-length', 0)

        if content is not None:
            self.content = content
            self.body = content
            self.raw_body = content

        if self.status >= 200 and self.status < 300:
            self.is_success = True

    def header(self, header_name):
        if self._headers is None:
            return None
        else:
            return self._headers.get(header_name, None)

    def headers(self):
        if self._headers is None:
            return {}
        headers = self._headers.keys()
        return headers
