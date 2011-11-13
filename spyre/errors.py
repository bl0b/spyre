class SpyreError(Exception):
    pass


class SpyreObjectBuilder(SpyreError):
    def __init__(self, expr):
        self.expr = expr
        msg = "'%s'" % expr
        self.msg = msg


class SpyreMethodBuilder(SpyreError):
    def __init__(self, expr):
        self.expr = expr
        msg = "'%s' is required" % expr
        self.msg = msg


class SpyreMethodCall(SpyreError):
    def __init__(self, expr):
        self.expr = expr
        msg = "'%s' is rquired" % expr
        self.msg = msg


class SpyreMethodPayload(SpyreError):
    def __init__(self):
        self.msg = "NON"


class SpyreStatusInvalid(SpyreError):
    def __init__(self):
        self.msg = "NON"


class SpyreMethodPayloadRequired(SpyreError):
    def __init__(self):
        self.msg = "payload is missing"