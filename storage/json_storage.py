import json
import os

class JSONStorage:
    def __init__(self, filename):
        self.filepath = os.path.join("data", filename)
        if not os.path.exists("data"):
            os.makedirs("data")

    def save(self, data):
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def load(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            # Custom fallback handling jika file JSON korup atau kosong
            return []