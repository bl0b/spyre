class SpyreError(Exception):
    pass


class SpyreMethodBuilder(SpyreError):
    def __init__(self, expr):
        self.expr = expr
        msg = "'%s' is required" % expr
        self.msg = msg
