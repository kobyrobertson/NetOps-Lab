import json

def load_devices(file_path):
    with open(file_path, 'r') as file:
        devices = json.load(file)

    return devices