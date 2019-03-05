from django.utils.encoding import force_text
from django.utils.functional import Promise

import collections
import copy


def resolve_promise(o):
    if isinstance(o, collections.Mapping):
        try:
            for k, v in o.items():
                o[k] = resolve_promise(v)
        except AttributeError:
            #ex. QueryDict may be immutable
            return resolve_promise(copy.deepcopy(o))
    elif isinstance(o, (list, tuple)):
        o = [resolve_promise(x) for x in o]
    elif isinstance(o, Promise):
        try:
            o = force_text(o)
        except:
            # Item could be a lazy tuple or list
            try:
                o = [resolve_promise(x) for x in o]
            except:
                raise Exception('Unable to resolve lazy object %s' % o)
    elif callable(o):
        o = o()

    return o
