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
