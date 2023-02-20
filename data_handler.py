import collections.abc
import os

import numpy
import numpy as np


DataHandlerDType = {type(np.dtype(np.float64)): 1, }
# 0-index is reserved for "custom"    # TODO: no support yet, but custom would read/write object structure to/from json
# 0-index is the default if non of the standard data types match
CUSTOM = 0

class DataHandler:
    ### Frame format: ###
    #TODO: Header:
    # - Dimensionality (d)                      - 4 byte
    # - Number of layers (n)                    - 4 bytes
    # - (n) * Size of each layer in bytes       - 4 bytes
    # -

    # - Layer id                                - 4 bytes
    # - Layer Shape (number of dimensions)      - 4 bytes
    # - Layer dtype enum (int, float, etc)      - 4 bytes
    # - Size of dimension                       - 4 bytes per dimension
    # - Elements                                - variable (buffer dump)


    def __init__(self, dimensions):
        self.frame_count = 0
        self.base_path = ""
        self.dimensions = dimensions
    def save_frame(self, field_data):
        with open(os.path.join(self.base_path, f"frame.{self.frame_count}"), 'wb') as f:
            # Header
            d = self.dimensions
            n = len(field_data)
            f.write(d.to_bytes(4, 'little'))
            f.write(n.to_bytes(4, 'little'))

            print(d.to_bytes(4, 'little'))
            print(n.to_bytes(4, 'little'))

            # Layers
            layers = []
            for field_id, data in field_data.items():
                arr = bytearray()
                print(f"Writing data for {field_id}: {field_id.to_bytes(4,'little')}")
                print(f"Writing data for length: {len(data.shape).to_bytes(4, 'little')}")
                print(f"Writing data for {data.shape}: {bytes(data.shape)}")
                arr.extend(field_id.to_bytes(4, 'little'))                                        # field id
                arr.extend(len(data.shape).to_bytes(4, 'little'))                                 # number of field dimensions
                arr.extend(DataHandlerDType.get(type(data.dtype), CUSTOM).to_bytes(4, 'little'))  # Data Type enumeration
                for dim in data.shape:
                    arr.extend(dim.to_bytes(4, 'little'))           # For each dimension, 4 bytes indicating the number of elements per dimension

                arr.extend(data.tobytes())
                layers.append(arr)

            # Finish writing header - layer size (bytes used to store the layer)
            for layer in layers:
                f.write(len(layer).to_bytes(4, 'little'))

            # Write all layer data to file
            for layer in layers:
                f.write(layer)

        # Update data handler state
        self.frame_count += 1

    def read_frame(self, frame_num):
        # Return field_data
        with open(os.path.join(self.base_path, f"frame.{frame_num}"), 'rb') as f:
            d = int.from_bytes(f.read(4), 'little')
            n = int.from_bytes(f.read(4), 'little')
            print(d)
            print(n)

            layers_length = []
            # Lets figure out how many bytes for each layer we need to read
            for i in range(n):
                layers_length.append(int.from_bytes(f.read(4), 'little'))

            layers = {}
            for i in range(n):
                layer_id = int.from_bytes(f.read(4), 'little')
                layer_num_dim = int.from_bytes(f.read(4), 'little')
                layer_dtype = int.from_bytes(f.read(4), 'little')
                # Lets read out each dimension's length/shape to create a multi-dimensional shape variable
                layer_dimensions = [int.from_bytes(f.read(4), 'little') for i in range(layer_num_dim)]
                # We have now read the layer header (16 bytes)... lets read the actual numpy buffer data (layer_length - 16)
                numpy_data = f.read(layers_length[i] - 16)


                # Iterate through each layer
                numpy_object = np.frombuffer(numpy_data, DataHandlerDType.get(layer_dtype)) # Populate using field_id, layer_data
                numpy_object.shape = layer_dimensions
                layers[layer_id] = numpy_object
        return layers





if __name__ == "__main__":
    x = DataHandler(1)
    data = x.read_frame(1)
    from matplotlib import pyplot


    x = [i for i in range(100)]
    y = [i for i in data[0]]
    pyplot.plot(x, y)