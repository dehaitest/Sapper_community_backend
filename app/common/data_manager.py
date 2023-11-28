from threading import Lock

class DataManager:
    def __init__(self):
        self.data = {}
        self.lock = Lock()

    def update_data(self, key, value):
        with self.lock:
            self.data[key] = value

    def get_data(self, key):
        with self.lock:
            return self.data.get(key, None)

    def get_all_data(self):
        with self.lock:
            return dict(self.data)  # Return a copy of the data

# Create a global instance of DataManager
spl_data_manager = DataManager()
