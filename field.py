import abc
import math
from abc import ABC


class FieldPoint(ABC):
    # Rotating buffer system, ensures calculations
    # Buffer 1: READ/CALCULATE/VISUALIZE
    # Buffer 2: WRITE
    _epsilon = 8.8541878128E-12
    _mu = 4 * math.pi * 1E-7

    def __init__(self, val):
        self._value = [0, 0]
        self._read_index = 0
        self._value[0] = val
        self._value[1] = val
        pass


    @abc.abstractmethod
    def update(self):
        # Input = data from calculation
        pass

    @property
    def value(self):
        """ Get the value of the field at this field point """
        return self._value[self._read_index]

    @value.setter
    def value(self, data):
        self._value[(self._read_index+0) % len(self._value)] = data

    def set_adjacency(self, adjacency_dict):
        """ This will set the adjacency links between field point such that calculations of curl can be made
            The dict must contain the axes of interest and 1 positive and 1 negative link at each location"""
        self.adjacency = adjacency_dict

    def set_colocated_fields(self, colocation_dict):
        self.colocation = colocation_dict

class ElectricFieldPoint(FieldPoint):
    def update(self):
        """ Electric Field updates require the following:
        E(t+dt) = E(t) + dt/ε * [∇ x H(t+dt/2)]        (2)
        * time_delta - (dt)
        * electric permeability - (µ)
        * previous time-step of the electric field - E(t)
        * previous time-step curl of the magnetic field - dH/dx + dH/dy + dH/dz
        """
        #1D: <x,y,z>
        #z: Ex, Hy

        #2D: <x,y,z>
        # Ez, Hx, Hy

        #3D: E<P,Q,R>
        #curlx = (Ry - Qz)i
        #curly = (Rx - Pz)j
        #curlz = (Qx - Py)k

        # Curl of magnetic field - 1D
        curl = (self.colocation[MagneticFieldPoint]['x']['.'].value -
                self.colocation[MagneticFieldPoint]['x']['-'].value)
        write_index = (self._read_index + 1) % len(self._value)
        self._value[write_index] = self._value[self._read_index] + 0.5 * curl
        self._read_index = (self._read_index+1) % len(self._value)   # Ping-pong between buffers

class MagneticFieldPoint(FieldPoint):
    def update(self):
        """ Magnetic Field updates require the following:
        H(t+dt/2) = H(t-dt/2) - dt/µ * [∇ x E(t)]      (1)
        * time_delta - (dt)
        * magnetic permeability - (µ)
        * previous time-step of the magnetic field - H(t-dt/2)
        * previous time-step curl of the electric field - dE/dx + dE/dy + dE/dz
        """
        dx = 2
        dt = 1
        # dt/dx = 1/(2*c0) is fixed due to the Courant stability condition - dt = dx/(2*c0)
        # c0 = 1/sqrt(µ_0*ε_0) thus this term cancels out when multiplied by 1/(2*c0)
        # Adding material variations to the vacuum permittivity/magnetic permeability will require
        # multiplying by 1/sqrt(µ*ε) depending on whether they differ from the base values.

        curl = (self.colocation[ElectricFieldPoint]['x']['+'].value -
                self.colocation[ElectricFieldPoint]['x']['.'].value)
        write_index = (self._read_index+1) % len(self._value)
        self._value[write_index] = self._value[self._read_index] + 0.5 * curl
        self._read_index = (self._read_index+1) % len(self._value)   # Ping-pong between buffers