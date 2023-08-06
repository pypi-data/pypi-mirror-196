from jax.numpy import concatenate
from .right import right
from .left import left


def insert(a, b):
    return concatenate([left(b), a, right(b)], axis=1)
