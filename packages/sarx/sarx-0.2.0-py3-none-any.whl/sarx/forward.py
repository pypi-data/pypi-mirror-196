from .core import forward as f
from .core import spike


def forward(*args, **kwargs):
    return f(spike)(*args, **kwargs)
