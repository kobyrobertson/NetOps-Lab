from datetime import datetime
from network import ping_host, resolve_host, check_port, check_web, check_ssh, check_dns
from devices import load_devices

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
        port = device["port"]
        service = device["service"]

        if service == 'HTTPS':
            web_status = check_web(host)
        else:
            web_status = None

        if service == 'SSH':
            ssh_status = check_ssh(host, port)
        else:
            ssh_status = None

        if service == 'DNS':
            dns_status = check_dns(host)
        else:
            dns_status = None

        ip_address = resolve_host(host)
        status, latency = ping_host(host)
        port_status = check_port(host, port)

        if status == 'UP':
            up_count += 1
        else:
            down_count += 1

        if ip_address == host:
            log_line = f'{current_time} | {name} | IP/host: {ip_address} ({service}) | Ping: {status} ({latency} ms) | Port {port}: {port_status}'
        else:
            log_line = f'{current_time} | {name} | {host} ({service}) | IP: {ip_address} | Ping: {status} ({latency} ms) | Port {port}: {port_status}'

        if web_status is not None:
            log_line += f' | HTTP: {web_status}'

        if ssh_status is not None:
            log_line += f' | SSH: {ssh_status}'

        if dns_status is not None:
            log_line += f' | DNS: {dns_status}'

        print(log_line)
        log_file.write(log_line + "\n")

print(f'\nSummary: {up_count} UP | {down_count} DOWN')