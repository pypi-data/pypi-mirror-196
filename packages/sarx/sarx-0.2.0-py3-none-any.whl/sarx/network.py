from .core import network as f
from .classes import Network


def network(*args, **kwargs):
    return Network(f(*args, **kwargs))
