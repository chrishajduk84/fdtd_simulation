from matplotlib import pyplot
from data_handler import DataHandler, DataHandlerDType

class Visualizer1D:
    time_index = -1
    def __init__(self, data_path):
        self.fig, self.ax = pyplot.subplots()
        self.data_path = data_path
        self.data_handler = DataHandler(1, data_path)
        self.next_frame()

    def __next__(self):
        return self.next_frame()

    def next_frame(self):
        self.ax.clear()
        self.time_index += 1
        frame_data = self.data_handler.read_frame(self.time_index)

        if frame_data is None:
            # Short-cut None-type, which indicates there is no 'next_frame'
            return False

        for layer_id, data in frame_data.items():
            if layer_id in (0, 1): # TODO: These are hardcoded for now (Electric field, Magnetic field)
                x = list(range(len(data)))
                y = [data[i] for i in x]
                self.ax.plot(x, y, label=layer_id)  # [x1, x2], [y1, y2] # TODO: label should evenutally be a string of the layer name
        self.ax.legend()
        pyplot.ylim((-1, 1))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        pyplot.pause(0.01)

        return True

    def go_to_frame(self):
        pass

    def show(self):
        self.ax.legend()
        pyplot.show(block=False)



if __name__ == "__main__":
    v = Visualizer1D("")
    v.show()

    while v.next_frame():
        pass
    input("Press enter to close the window...")


