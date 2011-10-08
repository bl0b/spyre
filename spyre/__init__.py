import __future__
import json
from spyre import spyrecore


class Spyre(object):

    @classmethod
    def new_from_spec(cls, spec_file, **args):
        json = cls._read_from_file(spec_file)
        spore = spyrecore.spyrecore(json)
        return spore

    @classmethod
    def new_from_string(cls, spec):
        pass

    @classmethod
    def new_from_dict(cls, dict):
        pass

    @classmethod
    def _read_from_file(cls, spec_file):
        spec = None
        try:
            f = open(spec_file)
            spec = json.load(f)
            f.close()
        except Exception, e:
            raise RuntimeError("Error while loading JSON spec (%s): %s"
                    % (spec_file, e))

        return spec
