import __future__
from spyre import core
from spyre.errors import *
import os.path


class Spyre(object):

    @classmethod
    def new_from_spec(cls, spec_file, base_url=None):
        spec_string = cls._read_from_file(spec_file)
        spore = cls.new_from_string(spec_string, base_url)
        return spore

    @classmethod
    def new_from_string(cls, spec_string, base_url=None):
        try:
            spore = core.base(spec_string=spec_string, base_url=base_url)
        except Exception, e:
            raise SpyreObjectBuilder(e)
        return spore

    @classmethod
    def new_from_dict(cls, dict):
        pass

    @classmethod
    def new_from_url(cls, spec_url):
        pass

    @classmethod
    def _read_from_file(cls, spec_file):
        if os.path.exists(spec_file) == False:
            raise SpyreObjectBuilder("Spec file %s does not exists" %
                    spec_file)

        try:
            f = open(spec_file, 'r')
            spec = f.read()
            f.close()
        except Exception, e:
            raise RuntimeError("Error while loading JSON spec (%s): %s"
                    % (spec_file, e))

        return spec
