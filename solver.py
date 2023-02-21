import math

from data_handler import DataHandler


class Solver:
    pass

class EMSolver:
    def __init__(self, electric_field, magnetic_field, electric_source=None, magnetic_source=None):
        #TODO: Speed improvement - double buffer + multiprocess (1 process to calculate, 1 to save to disk/draw)
        self.electric_field = electric_field  # E
        self.magnetic_field = magnetic_field  # H
        self.electric_source = electric_source  # E_source (time-varying)
        self.magnetic_source = magnetic_source  # H_source (time-varying)
        #TODO: how do I do the current_density thing - this might be a duplicate of the electric source
        self.current_density = None           # J = sigma * E, where sigma is conductivity [S/m]

        self.shape = self.electric_field.shape #TODO: magnetic field should be the same
        self.dimensionality = len(self.shape)
        self.time_step = 0

    @property
    def fields(self):
        return {0: self.electric_field, 1: self.magnetic_field}

    def next_step(self):
        imp_0 = 377.0 # This is equal to sqrt(u_0/epsilon_0), which is the characteristic impedance of free space
        #TODO: expand to multiple dimensions
        for dim in range(self.dimensionality):
            for i in range(self.shape[dim]-1):
                self.magnetic_field[i] = self.magnetic_field[i] + (self.electric_field[i+1] - self.electric_field[i]) / imp_0
                print(self.magnetic_field[i])
            for i in range(1, self.shape[dim]):
                self.electric_field[i] = self.electric_field[i] + (self.magnetic_field[i] - self.magnetic_field[i-1]) * imp_0

            # TODO: Hardwired Source Node - how do we change this...? Sources can be time-varying and not always hardwired

            # Additive sources functions - f(t, x,y,z), where y,z depend on the dimension being used
            # self.electric_source is a pre-computed multi-dimensional array (time dimension, followed by spatial dimensions)
            # Total dimensionality of the electric_source is (dimensions + 1)
            for i in range(1, self.shape[dim]):
                self.electric_field[i] += self.electric_source[self.time_step][i]

            # Hard-wire sources are last
            # TODO: are hard-wire sources EVER useful? Do I need to do this?


        self.time_step += 1





if __name__ == "__main__":
    # Use EMSolver, which requires ElectricFieldLayer, MagneticFieldLayer, (opt) ElectricSourceLayer, (opt) MagneticSourceLayer
    from layers import FieldLayer
    from matplotlib import pyplot
    electric_field = FieldLayer([100])
    magnetic_field = FieldLayer([100])
    print(len(electric_field.shape))

    # Pre-generate electric source
    electric_source = []
    for t in range(250):
        time_layer = FieldLayer([100])
        # for i in range(100):
        #     time_layer[i] = math.exp(-(i - 30.) * (i - 30.) / 10.)
        time_layer[50] = math.exp(-(t - 30.) * (t - 30.) / 100.)
        #time_layer[80] = 1#math.exp(-(t - 30.) * (t - 30.) / 100.)
        electric_source.append(time_layer)

    # Solve
    solver = EMSolver(electric_field, magnetic_field, electric_source=electric_source)

    # Save data
    writer = DataHandler(1)

    for i in range(250):
        solver.next_step()
        field = solver.fields
        #print(field)
        writer.save_frame(field)
        #print(field[0].shape)
        x = [i for i in range(100)]
        y = [i for i in field[0]]
        pyplot.plot(x, y)
        pyplot.pause(0.1)
