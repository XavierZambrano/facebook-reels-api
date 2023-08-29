import os


class Reel:
    def __init__(self, file_path, description):
        self.id = None
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        self.file_data = open(file_path, 'rb')
        self.description = description
