import subprocess
import socket
import urllib.request
import urllib.error
import platform

def ping_host(host):

    # OS specific syntax, force IPv4 on Windows to match resolve_host()
    if platform.system() == 'Windows':
        ping_command = ["ping", "-4", "-n", "1", host]
    else:
        ping_command = ["ping", "-c", "1", host]

    result = subprocess.run(
        ping_command,
        capture_output=True,
        text=True
        )

    if result.returncode == 0:
        output = result.stdout

        # Obtains the actual latency reported by the ping command
        if "time=" in output:
            latency = output.split('time=')[1].split('ms')[0].strip()
            return 'UP', latency

        elif 'time<1ms' in output:
            return 'UP', '<1'

        else:
            return 'UP', 'UNKNOWN'

    else:
        return 'DOWN', 'N/A'

def resolve_host(host):
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        return 'UNRESOLVED'

def check_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=3):
            return 'OPEN'
    except ConnectionRefusedError:
        return 'CLOSED'
    except TimeoutError:
        return "TIMEOUT"
    except OSError:
        return 'ERROR'

def check_web(host):
    url = f'https://{host}'

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status

    # HTTP error responses still confirm that the web server responded
    except urllib.error.HTTPError as error:
        return error.code
    
    except urllib.error.URLError:
        return 'ERROR'

def check_ssh(host, port):
    try:
        with socket.create_connection((host, port), timeout=3) as connection:

            # SSH servers send an identification banner after the TCP connection opens
            banner = connection.recv(1024).decode().strip()

        if banner.startswith('SSH'):
            return 'AVAILABLE'
        else:
            return 'INVALID RESPONSE'

    except OSError:
        return 'ERROR'

def check_dns(host):
    try:
        result = subprocess.run(
            ['nslookup', 'example.com', host],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and 'Name:' in result.stdout:
            return 'RESPONDING'
        else:
            return 'ERROR'

    except subprocess.TimeoutExpired:
        return 'TIMEOUT'

def check_service(host, port, service):
    if service == 'HTTPS':
        return check_web(host)

    elif service == 'SSH':
        return check_ssh(host, port)

    elif service == 'DNS':
        return check_dns(host)

    else:
        return 'UNKNOWN'