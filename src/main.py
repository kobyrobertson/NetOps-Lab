from datetime import datetime
from network import ping_host
from inventory import load_devices

devices = load_devices('devices/devices.json')
log_path = 'logs/network_log.txt'

print('NetOps Lab - Device Status')
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'Checked at: {current_time}')
print('--------------------------')

up_count = 0
down_count = 0

with open(log_path, "a") as log_file:
    for device in devices:
        name = device["name"]
        host = device["host"]
        status, duration = ping_host(host)

        if status == 'UP':
            up_count += 1
        else:
            down_count += 1

        log_line = f'{current_time} | {name} | {host} | {status} | {duration} ms'

        print(log_line)
        log_file.write(log_line + "\n")

print(f'\nSummary: {up_count} UP | {down_count} DOWN')