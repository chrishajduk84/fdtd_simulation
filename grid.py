import math

from numpy import ndarray
from field import FieldPoint, ElectricFieldPoint, MagneticFieldPoint

class Grid:
    _grid = {}
    _shape = None
    _time_index = 0  # determines which buffers to use
    def __init__(self):
        pass

    @property
    def shape(self):
        return self._shape

    @property
    def fields(self):
        return self._grid.items()


class Grid1D(Grid):
    """ 1D Spatial grid + with N field layers, temporal solution is managed within the field"""
    def __init__(self, length: int, fields=[]):
        self._shape = (length)
        self._fields = fields
        for field_type in fields:
            arr = ndarray((length), dtype=FieldPoint)
            # Initialize elements
            for i in range(arr.shape[0]):
                arr[i] = field_type(0)
            # Initialize relationships between elements
            # for i in range(arr.shape[0]):
            #     pos = arr[i+1] if i+1 < arr.shape[0] else None
            #     neg = arr[i-1] if i-1 >= 0 else None
            #     arr[i].set_adjacency = {"x":{"+":pos,"-":neg}}
            self._grid[field_type] = arr

        spread = 12
        for pos in range(length):
            self._grid[MagneticFieldPoint][pos].value += math.exp(-0.5*math.pow( (99 - pos)/spread, 2))
            self._grid[MagneticFieldPoint][pos].value -= math.exp(-0.5 * math.pow((100 - pos) / spread, 2))
            #self._grid[MagneticFieldPoint][120].value = 0.5

        for field_type in fields:
            for i in range(self._grid[field_type].shape[0]):
                print(self._grid[field_type][i].value)

        # Initialize relationships between fields
        for field_type in fields:
            for i in range(arr.shape[0]):
                colocated = {}
                for f_type in fields:
                    if f_type != field_type:
                        pos = self._grid[f_type][i+1] if i+1 < self._grid[f_type].shape[0] else self._grid[f_type][i-1]
                        neg = self._grid[f_type][i-1] if i-1 >= 0 else self._grid[f_type][i+1]
                        middle = self._grid[f_type][i]
                        colocated[f_type] = {"x": {"+": pos, ".": middle, "-": neg}}
                self._grid[field_type][i].set_colocated_fields(colocated)

    def update(self):
        for field_type in self._fields:
            for i in range(self._grid[field_type].shape[0]):
                self._grid[field_type][i].update()


class Grid2D(Grid):
    """ 2-d Spatial grid + 1-d temporal grid"""
    def __init__(self):

        pass

class Grid3D(Grid):
    """ 3-d Spatial grid + 1-d temporal grid"""
    def __init__(self):
        pass



if __name__ == "__main__":
    grid_1d = Grid1D(100, fields=[ElectricFieldPoint, MagneticFieldPoint])
    grid_1d.update()
