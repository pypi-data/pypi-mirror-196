from jax.numpy import where, minimum
from jax import custom_jvp


@custom_jvp
def spike(x):
    return where(x >= 1, minimum(x, 2), 0)


@spike.defjvp
def spike_jvp(primals, tangents):
    (x,) = primals
    (dy,) = tangents
    return spike(x), dy
