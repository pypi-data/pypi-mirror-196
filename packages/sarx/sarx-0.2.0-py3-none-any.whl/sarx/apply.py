from jax import jit
from .forward import forward


@jit
def apply(*args, **kwargs):
    return forward(*args, **kwargs)[1][-1]
