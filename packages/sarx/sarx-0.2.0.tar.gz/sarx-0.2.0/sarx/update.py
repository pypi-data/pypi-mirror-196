from jax.tree_util import tree_map
from .core import update as f


def update(network, gradient, learning_rate):
    return tree_map(
        lambda network, gradient: f(network, gradient, learning_rate),
        network,
        gradient,
    )
