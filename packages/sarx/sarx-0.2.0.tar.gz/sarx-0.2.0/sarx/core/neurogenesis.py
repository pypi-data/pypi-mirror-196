from jax.random import split
from .synapse import synapse
from .insert import insert


def neurogenesis(key, network):
    return [
        insert(synapse(key, shape=(weights.shape[0], 1)), weights)
        for key, weights in zip(split(key, len(network)), network)
    ] + [synapse(key, shape=(1, 1))]
