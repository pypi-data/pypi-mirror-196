from multipledispatch import dispatch
from .core.mse import mse


@dispatch(object, object, object)
def loss(network, x, y):
    return mse(y, network(x))


@dispatch(object)
def loss(f):
    def function(network, x):
        yhat = network(x)
        return mse(f(yhat), yhat)

    return function
