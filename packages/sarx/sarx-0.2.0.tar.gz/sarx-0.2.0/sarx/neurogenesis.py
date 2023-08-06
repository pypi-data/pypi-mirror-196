from .core import neurogenesis as f
from .classes import Network


def neurogenesis(*args, **kwargs):
    return Network(f(*args, **kwargs))
