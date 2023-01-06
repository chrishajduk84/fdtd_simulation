import abc
from typing import Union, Iterable, Tuple

from numpy import ndarray, zeros

class Layer(abc.ABC):
    pass


class DiscreteLayer(Layer, abc.ABC):
    def __getitem__(self, index: int):
        return self._layer[index]

    def __setitem__(self, index: int, value: float):
        self._layer[index] = value

    def __setslice__(self, i: int, j: int, sequence: Iterable):
        for index in range(j-i):
            print(sequence[index])
            self._layer[index+i] = sequence[index]

    def __delslice__(self, i, j):
        raise NotImplementedError("All values instantiated at initialization, cannot delete items")

    def __delitem__(self, key):
        raise NotImplementedError("All values instantiated at initialization, cannot delete item")

    @property
    def shape(self):
        return self._layer.shape

class FieldLayer(DiscreteLayer):
    def __init__(self, dimensions: Union[Iterable, Tuple[int]]):
        # dtype might need to change to a tensor (each point in space may have multi-dimensional components)???
        self._layer = zeros(dimensions, dtype=float)



class ContinuousLayer:
    pass


if __name__ == "__main__":
    f = FieldLayer([3, 3, 3])
    print(f[:])