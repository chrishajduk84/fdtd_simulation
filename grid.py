import math

from numpy import ndarray

from boundary import BoundaryPoint, InfiniteBoundaryPoint1D
from field import FieldPoint, ElectricFieldPoint, MagneticFieldPoint

class GridLayer(ndarray):
    pass
# Can't use abstraction since, ndarray is a compiled library
#     def __init__(self, dimensions, dtype):
#         self.
#         super(GridLayer, self).__init__(shape=dimensions, dtype=dtype)

# Types of layers:
# Link/colocation layers
# Source layers
# Material layers
# Annotation layers
# Measurement layers
# Field Layers
# Particle Layers (contain groups of particles with continuous variables and
#                   can be in between grid points and travel slower than speed of light)

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
            arr = GridLayer((length), dtype=FieldPoint)
            # Initialize elements
            for i in range(arr.shape[0]):
                arr[i] = field_type(0)
            # Initialize relationships between elements
            # for i in range(arr.shape[0]):
            #     pos = arr[i+1] if i+1 < arr.shape[0] else None
            #     neg = arr[i-1] if i-1 >= 0 else None
            #     arr[i].set_adjacency = {"x":{"+":pos,"-":neg}}
            self._grid[field_type] = arr

        # Source
        spread = 12
        for pos in range(length):
            self._grid[ElectricFieldPoint][pos].value += 0.1 * math.exp(-0.5*math.pow( (99 - pos)/spread, 2))
            #self._grid[MagneticFieldPoint][pos].value -= math.exp(-0.5 * math.pow((100 - pos) / spread, 2))
            #self._grid[MagneticFieldPoint][120].value = 0.5

        for field_type in fields:
            for i in range(self._grid[field_type].shape[0]):
                print(self._grid[field_type][i].value)

        # Co-location - Initialize relationships between fields
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

        # Boundary Condition
        arr = GridLayer((length), dtype=BoundaryPoint)
        # Initialize elements
        for i in range(arr.shape[0]):
            if i == 0:
                arr[i] = InfiniteBoundaryPoint1D()
            elif i == arr.shape[0] - 1:
                arr[i] = InfiniteBoundaryPoint1D()
            else:
                arr[i] = BoundaryPoint()
        # Initialize relationships between elements
        # for i in range(arr.shape[0]):
        #     pos = arr[i+1] if i+1 < arr.shape[0] else None
        #     neg = arr[i-1] if i-1 >= 0 else None
        #     arr[i].set_adjacency = {"x":{"+":pos,"-":neg}}
        self._grid[BoundaryPoint] = arr


    def update(self):

        # Boundary Updates - WHY ISN'T IT WORKING???
        length = self._grid[BoundaryPoint].shape[0]
        self._grid[BoundaryPoint][0].update(self._grid[ElectricFieldPoint][1].value)
        self._grid[BoundaryPoint][length-1].update(self._grid[ElectricFieldPoint][length-2].value)

        for i in range(self._grid[BoundaryPoint].shape[0]):
            self._grid[ElectricFieldPoint][i].value = self._grid[BoundaryPoint][i].apply(
                                                        self._grid[ElectricFieldPoint][i].value
                                                        )

        for field_type in self._fields:
            for i in range(self._grid[field_type].shape[0]):
                self._grid[field_type][i].update()

        # print(self._grid[ElectricFieldPoint][0].value)
        # print(self._grid[ElectricFieldPoint][0].colocation[MagneticFieldPoint]['x']['.'].value - self._grid[ElectricFieldPoint][0].colocation[MagneticFieldPoint]['x']['-'].value)
        # print("----")
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
