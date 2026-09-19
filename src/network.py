import subprocess
import socket
import urllib.request
import urllib.error

def ping_host(host):
    result = subprocess.run(
        ["ping", "-4", "-n", "1", host],
        capture_output=True,
        text=True
        )

    if result.returncode == 0:
        output = result.stdout

        if "time=" in output:
            latency = output.split('time=')[1].split('ms')[0]
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
        connection = socket.create_connection((host, port), timeout=3)
        connection.close()
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

    except urllib.error.HTTPError as error:
        return error.code
    
    except urllib.error.URLError:
        return 'ERROR'

def check_ssh(host, port):
    try:
        connection = socket.create_connection((host, port), timeout=3)

        banner = connection.recv(1024).decode().strip()

        connection.close()

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