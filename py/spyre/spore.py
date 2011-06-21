class spore(object):
    def __init__(self):
        pass

    def http_call():
        class http_call_handler(object):
            def __init__(self,spo):
                pass

            def __call__(self, *args,**kwargs):
                print "pouet"

class spore_meta(type):
    def __init__(class, name, bases, dic):
        spec = dic['spore_desc']
        if 'documentation' in spec:
            dic['__doc__'] = spec['documentation']
            dic['base_url'] = spec['base_url']
            dic['version'] = spec['version']
        for mspec in spec['methods']:
            pass
        
        
        
