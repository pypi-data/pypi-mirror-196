from jax.random import split
from .synapse import synapse


def network(key, inputs, layers=1):
    return [synapse(key, shape=(inputs, layers))] + [
        synapse(key, shape=(1, layers - index))
        for index, key in zip(range(1, layers), split(key, layers - 1))
    ]
