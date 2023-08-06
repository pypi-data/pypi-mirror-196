from jax.numpy import clip
from .gd import gd


def update(network, gradient, learning_rate):
    return gd(network, clip(gradient, -8, 8), learning_rate)
