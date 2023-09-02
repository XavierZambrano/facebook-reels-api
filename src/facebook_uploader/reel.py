import os


class Reel:
    def __init__(self, description: str, file_path: str = '', updated_time: str = None, id: str = None):
        self.id = id
        self.file_path = file_path
        self.description = description
        self.updated_time = updated_time

        if file_path:
            self.file_size = os.path.getsize(file_path)
            with open(file_path, 'rb') as file:
                self.file_data = file.read()
        else:
            self.file_size = None
            self.file_data = None

    def __str__(self):
        return f'Reel: {self.id} {self.description}'
