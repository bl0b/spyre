import __future__
from spyre import core
from spyre.errors import *
import os.path


def new_from_spec(spec_file, base_url=None):
    spec_string = _read_from_file(spec_file)
    spore = new_from_string(spec_string, base_url)
    return spore


def new_from_string(spec_string, base_url=None):
    try:
        spore = core.base(spec_string=spec_string, base_url=base_url)
    except Exception, e:
        raise SpyreObjectBuilder(e)
    return spore

# TODO new_from_url
# TODO new_from_dict


def _read_from_file(spec_file):
    if os.path.exists(spec_file) == False:
        raise SpyreObjectBuilder(
            "Spec file {file} does not exists".format(file=spec_file))

    try:
        f = open(spec_file, 'r')
        spec = f.read()
        f.close()
    except Exception, e:
        raise RuntimeError(
            "Error while loading JSON spec {file}: {error}".format(
                file=spec_file, error=e))

    return spec
