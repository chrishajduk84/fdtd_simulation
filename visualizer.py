from matplotlib import pyplot
from grid import Grid1D
from field import FieldPoint, ElectricFieldPoint, MagneticFieldPoint

class Visualizer1D:
    time_index = 0
    def __init__(self, grid: Grid1D):
        self.fig, self.ax = pyplot.subplots()
        self._grid = grid
        self.next_frame()

    def __next__(self):
        return self.next_frame()

    def next_frame(self):
        self.ax.clear()
        self.time_index += 1
        for field_name, data in self._grid.fields:
            if field_name in (ElectricFieldPoint, MagneticFieldPoint):
                x = list(range(len(data)))
                y = [data[i].value for i in x]
                self.ax.plot(x, y, label=field_name)  # [x1, x2], [y1, y2]
        self.ax.legend()
        pyplot.ylim((-0.1, 0.1))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        pyplot.pause(0.01)

    def go_to_frame(self):
        pass

    def show(self):
        self.ax.legend()
        pyplot.show(block=False)



if __name__ == "__main__":
    grid_1d = Grid1D(200, fields=[ElectricFieldPoint, MagneticFieldPoint])
    v = Visualizer1D(grid_1d)
    v.show()
    while True:
        grid_1d.update()
        v.next_frame()
        #input("TEST")
    input("TEST")

