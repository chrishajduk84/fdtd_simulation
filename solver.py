import math
from typing import Optional, List, Dict

from data_handler import DataHandler
from layers import FieldLayer

class EMSolver1D:
    def __init__(self, electric_field: FieldLayer, magnetic_field: FieldLayer, electric_source: Optional[List[FieldLayer]] = None, magnetic_source: Optional[List[FieldLayer]] = None, eps_r: Optional[List[float]] = None, mu_r: Optional[List[float]] = None, loss: Optional[List[float]] = None, left_boundary: Optional[bool] = None, right_boundary: Optional[bool] = None):
        #TODO: Speed improvement - double buffer + multiprocess (1 process to calculate, 1 to save to disk/draw)
        self.electric_field = electric_field  # E
        self.magnetic_field = magnetic_field  # H
        self.electric_source = electric_source  # E_source (time-varying)
        self.magnetic_source = magnetic_source  # H_source (time-varying)
        self.eps_r = eps_r if eps_r is not None else [1.0] * self.electric_field.shape[0]
        self.mu_r = mu_r if mu_r is not None else [1.0] * self.electric_field.shape[0]
        self.loss = loss if loss is not None else [0.0] * self.electric_field.shape[0]
        self.left_boundary = left_boundary                # Boundary conditions
        self.right_boundary = right_boundary                # Boundary conditions
        #TODO: how do I do the current_density thing - this might be a duplicate of the electric source
        #self.current_density = None           # J = sigma * E, where sigma is conductivity [S/m]

        self.shape = self.electric_field.shape #TODO: magnetic field should be the same
        self.dimensionality = len(self.shape)
        self.time_step = 0

    @property
    def fields(self) -> Dict[int, FieldLayer]:
        return {0: self.electric_field, 1: self.magnetic_field}

    def next_step(self) -> None:
        imp_0 = 377.0 # This is equal to sqrt(u_0/epsilon_0), which is the characteristic impedance of free space
        # Note since we are keeping the courant number as unity (Sc = 1), we do not need to multiply by the time step or spatial step

        for dim in range(self.dimensionality):


            if self.right_boundary:
                self.magnetic_field[-1] = self.magnetic_field[-2]

            for i in range(self.shape[dim]-1):
                self.magnetic_field[i] = self.magnetic_field[i]*(1.0-self.loss[i])/(1.0+self.loss[i]) + (self.electric_field[i+1] - self.electric_field[i]) / imp_0 / self.mu_r[i] / (1.0+self.loss[i])

            # Additive magnetic source function
            for i in range(self.shape[dim]-1):
                self.magnetic_field[i] += self.magnetic_source[self.time_step][i]

            if self.left_boundary:
                self.electric_field[0] = self.electric_field[1]
            
            for i in range(1, self.shape[dim]):
                self.electric_field[i] = self.electric_field[i]*(1.0-self.loss[i])/(1.0+self.loss[i]) + (self.magnetic_field[i] - self.magnetic_field[i-1]) * imp_0 / self.eps_r[i]/(1+self.loss[i])



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

    # Pre-generate electric source (Additive)
    electric_source = []
    for t in range(250):
        time_layer = FieldLayer([100])
        # Total-field / scattered-field source at index 50
        time_layer[50] = math.exp(-(t + 1 - 30.) * (t + 1 - 30.) / 100.)
        electric_source.append(time_layer)
    
    # Pre-generate magnetic corrections for TFSF boundary
    magnetic_source = []
    for t in range(250):
        time_layer = FieldLayer([100])
        # Correction at index 49 for scattered field separation
        time_layer[49] = -1/377.0 * math.exp(-(t - 30.) * (t - 30.) / 100.)
        magnetic_source.append(time_layer)

    # Initialize relative permittivity and permeability
    eps_r = [1.0] * 100
    mu_r = [1.0] * 100
    # Change eps and mu at 70 onwards
    eps_r[70:] = [9.0] * 30
    #mu_r[70:] = [1.0] * 30
    # Initialize loss
    loss = [0.0] * 100
    loss[90:] = [0.2] * 10

    # Solve
    solver = EMSolver1D(electric_field, magnetic_field, electric_source=electric_source, magnetic_source=magnetic_source, eps_r=eps_r, mu_r=mu_r, loss=loss, left_boundary=True, right_boundary=True)

    # Save data
    #writer = DataHandler(1)

    for i in range(250):
        solver.next_step()
        field = solver.fields
        #writer.save_frame(field)
        x = [i for i in range(100)]
        y = [i for i in field[0]]
        pyplot.plot(x, y)
        pyplot.pause(0.1)
