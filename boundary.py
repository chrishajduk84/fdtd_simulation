import abc
import math
#from abc import ABC


class BoundaryPoint:
    # Default transform is to take the input value and return it as the output
    def __init__(self, boundary_condition=lambda value: value):
        self._transform = boundary_condition

    def apply(self, value):
        # In the simple case, a single-variate transform is applied
        return self._transform(value)

    def set_condition(self, boundary_condition):
        self._transform = boundary_condition

    def update(self):
        pass

class InfiniteBoundaryPoint1D(BoundaryPoint):
    def __init__(self):
        # For infinite boundary condition - we will absorb the waves without reflection
        # It takes two time steps for the wave to cross a cell, therefore, we need to assign a value at the boundary
        # according to the adjacent value, two time-steps ago
        self._adjacent_history = [0]
        self._transform = lambda value: self._adjacent_history[0]

    def update(self, adjacent_value):
        self._adjacent_history.append(adjacent_value)
        self._adjacent_history.pop(0)


