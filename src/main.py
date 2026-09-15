import json
import subprocess

with open('devices/devices.json', 'r') as file:
    devices = json.load(file)

for device in devices:
    name = device["name"]
    host = device["host"]

    result = subprocess.run(["ping", "-n", "1", host])

    if result.returncode == 0:
        print(f"Name: {name} | Host: {host} | Status: UP")
    else:
        print(f"Name: {name} | Host: {host} | Status: DOWN")