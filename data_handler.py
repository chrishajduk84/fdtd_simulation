import os

class DataHandler:
    def __init__(self):
        self.frame_count = 0
        self.base_path = ""
    def save_frame(self, field_data):
        with open(os.path.join(self.base_path, f"frame.{self.frame_count}"), 'w') as f:
            for field_name, data in field_data.items():
                f.write()
