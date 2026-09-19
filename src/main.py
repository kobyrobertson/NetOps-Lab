import os
from datetime import datetime
from devices import load_devices
from network import ping_host, resolve_host, check_port, check_service

def format_header(current_time):
    return (
        "NetOps Lab - Device Status\n"
        f"Checked: {current_time}\n"
        "--------------------------"
    )

def format_device_status(name, host, port, service, ip_address, status, latency, port_status, service_status):
    if ip_address == host:
        address_line = f'  IP/Host: {ip_address}'
    else:
        address_line = f'  Host: {host}\n  IP: {ip_address}'

    return (
        f'{name} ({service})\n'
        f'{address_line}\n'
        f'  Ping: {status} ({latency} ms)\n'
        f'  Port {port}: {port_status}\n'
        f'  {service}: {service_status}\n'
    )

def format_log_line(current_time, name, host, port, service, ip_address, status, latency, port_status, service_status):
    if ip_address == host:
        address = f'IP/Host: {ip_address} ({service})'
    else:
        address = f'{host} ({service}) | IP: {ip_address}'

    return (
        f'{current_time} | {name} | {address} | Ping: {status} ({latency} ms) | Port {port}: {port_status} | {service}: {service_status}'
    )

def update_summary_counts(status, port_status, service, service_status, ping_up_count, port_open_count, service_up_count):
    if status == "UP":
        ping_up_count += 1

    if port_status == "OPEN":
        port_open_count += 1

    # Determine service health based on the expected result for each service type
    if service == "HTTPS":
        if isinstance(service_status, int) and 200 <= service_status < 400:
            service_up_count += 1

    elif service == "SSH":
        if service_status == "AVAILABLE":
            service_up_count += 1

    elif service == "DNS":
        if service_status == "RESPONDING":
            service_up_count += 1

    return ping_up_count, port_open_count, service_up_count

def summary(total_devices, ping_up_count, port_open_count, service_up_count):
    return (
        "Summary:\n"
        f"  Devices checked: {total_devices}\n"
        f"  Ping successful: {ping_up_count}/{total_devices}\n"
        f"  Ports open: {port_open_count}/{total_devices}\n"
        f"  Services healthy: {service_up_count}/{total_devices}"
    )

def main(): 
    devices = load_devices('devices/devices.json')

    # Makes "logs" path automatically 
    os.makedirs('logs', exist_ok=True)
    log_path = 'logs/network_log.txt'

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ping_up_count = 0
    port_open_count = 0
    service_up_count = 0

    print(format_header(current_time))

    with open(log_path, "a") as log_file:
        for device in devices:
            name = device["name"]
            host = device["host"]
            port = device["port"]
            service = device["service"]

            ip_address = resolve_host(host)
            status, latency = ping_host(host)
            port_status = check_port(host, port)
            service_status = check_service(host, port, service)

            print(format_device_status(name, host, port, service, ip_address, status, latency, port_status, service_status))

            ping_up_count, port_open_count, service_up_count = update_summary_counts(status, port_status, service, service_status, ping_up_count, port_open_count, service_up_count)

            log_line = format_log_line(current_time, name, host, port, service, ip_address, status, latency, port_status, service_status)

            log_file.write(log_line + "\n")

    print(summary(len(devices), ping_up_count, port_open_count, service_up_count))

if __name__ == '__main__':
    main()