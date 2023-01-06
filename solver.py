import math


class Solver:
    pass

class EMSolver:
    def __init__(self, electric_field, magnetic_field, electric_source=None, magnetic_source=None):
        #TODO: Speed improvement - double buffer + multiprocess (1 process to calculate, 1 to save to disk/draw)
        self.electric_field = electric_field  # E
        self.magnetic_field = magnetic_field  # H
        self.electric_source = electric_source  # E_source (time-varying)
        self.magnetic_source = magnetic_source  # H_source (time-varying)
        #TODO: how do I do the current_density thing
        self.current_density = None           # J = sigma * E, where sigma is conductivity [S/m]

        self.shape = self.electric_field.shape #TODO: magnetic field should be the same
        self.dimensionality = len(self.shape)
        self.time_step = 0

    @property
    def fields(self):
        return [self.electric_field, self.magnetic_field]

    def next_step(self):
        imp_0 = 377.0
        #TODO: expand to multiple dimensions
        for dim in range(self.dimensionality):
            for i in range(self.shape[dim]-1):
                self.magnetic_field[i] = self.magnetic_field[i] + (self.electric_field[i+1] - self.electric_field[i]) / imp_0
                print(self.magnetic_field[i])
            for i in range(1, self.shape[dim]):
                self.electric_field[i] = self.electric_field[i] + (self.magnetic_field[i] - self.magnetic_field[i-1]) * imp_0

            self.electric_field[0] = math.exp(-(self.time_step - 30.) * (self.time_step - 30.) / 100.);

        self.time_step += 1





if __name__ == "__main__":
    # Use EMSolver, which requires ElectricFieldLayer, MagneticFieldLayer, (opt) ElectricSourceLayer, (opt) MagneticSourceLayer
    from layers import FieldLayer
    from matplotlib import pyplot
    electric_field = FieldLayer([100])
    magnetic_field = FieldLayer([100])
    print(len(electric_field.shape))
    solver = EMSolver(electric_field, magnetic_field)

    for i in range(250):
        solver.next_step()
        field = solver.fields
        print(field[0].shape)
        x = [i for i in range(100)]
        y = [i for i in field[0]]
        pyplot.plot(x, y)
        pyplot.pause(0.1)
