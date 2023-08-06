from jax.tree_util import register_pytree_node
from sarx.apply import apply


class Network(list):
    __call__ = apply


def flatten(network):
    return (network, None)


def unflatten(_, children):
    return Network(children)


register_pytree_node(Network, flatten, unflatten)
