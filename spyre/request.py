import httplib2


class spyrerequest(object):
    def __init__(self, env):
        self.env = env
        self.finalize()

    def finalize(self):
        print self.env
        pass
