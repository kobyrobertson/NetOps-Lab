# NetOps Lab

NetOps Lab is a lightweight Python network monitoring tool that checks the reachability and health of configured network services.

The program reads devices from a JSON inventory, performs multiple layers of network checks, logs the results, and prints a summary of device health. Version 1 supports DNS, HTTPS, and SSH service checks.

## Features

- Loads devices from a JSON inventory
- Resolves hostnames to IPv4 addresses
- Checks host reachability using ICMP ping
- Reports the round-trip latency returned by the system ping command
- Checks TCP port availability
- Performs service-specific health checks for:
  - DNS
  - HTTPS
  - SSH
- Logs each check with a timestamp
- Summarizes ping, port, and service health
- Supports Windows and macOS ping syntax
- Uses only Python standard-library modules

## Supported Services

| Service | Default Port | Health Check |
| --- | ---: | --- |
| DNS | 53 | Performs a DNS lookup through the configured DNS server |
| HTTPS | 443 | Sends an HTTPS request and evaluates the HTTP response |
| SSH | 22 | Connects to the service and validates the SSH identification banner |

## Project Structure

```
NetOps-Lab/
├── devices/
│   └── devices.json
├── src/
│   ├── main.py
│   ├── network.py
│   └── devices.py
├── logs/
│   └── network_log.txt
├── .gitignore
└── README.md
```

The `logs/`directory is created automatically when the program runs and is ignored by Git.

## Device Inventory

Devices are configured in `devices/devices.json`.

Example:

```json
[
  {
    "name": "google-dns",
    "host": "8.8.8.8",
    "port": 53,
    "service": "DNS"
  },
  {
    "name": "youtube",
    "host": "youtube.com",
    "port": 443,
    "service": "HTTPS"
  },
  {
    "name": "github-ssh",
    "host": "github.com",
    "port": 22,
    "service": "SSH"
  }
]
```

Each device contains:

- `name` - human-readable label for the device or service
- `host` - hostname or IP address to monitor
- `port` - expected TCP service port
- `service` - service-specific health check to perform

Currently supported service values are `DNS`, `HTTPS`, and `SSH`.

## Running NetOps Lab

Clone the repository:

```bash
git clone https://github.com/kobyrobertson/NetOps-Lab.git
cd NetOps-Lab
```

A virtual environment is optional because NetOps Lab currently uses only Python standard-library modules.

### Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python src/main.py
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 src/main.py
```

## Example Output

```
NetOps Lab - Device Status
Checked: 2026-09-19 10:19:30
--------------------------
google-dns (DNS)
  IP/Host: 8.8.8.8
  Ping: UP (17.152 ms)
  Port 53: OPEN
  DNS: RESPONDING

youtube (HTTPS)
  Host: youtube.com
  IP: 142.251.116.93
  Ping: UP (18.355 ms)
  Port 443: OPEN
  HTTPS: 200

github-ssh (SSH)
  Host: github.com
  IP: 140.82.114.3
  Ping: UP (31.685 ms)
  Port 22: OPEN
  SSH: AVAILABLE

Summary:
  Devices checked: 3
  Ping successful: 3/3
  Ports open: 3/3
  Services healthy: 3/3
```

IP addresses and latency values will vary between runs/OS (the example output was ran on macOS).

## How It Works

For each configured device, NetOps Lab performs several layers of checks:

1. **Hostname resolution** - Resolves the configured hostname to an IPv4 address.
2. **ICMP ping** - Checks whether the host responds to ping and reads the reported round-trip latency.
3. **TCP port check** - Attempts to establish a TCP connection to the configured service port.
4. **Service health check** - Performs a check specific to the configured service:
   - **DNS:** uses `nslookup` to request a known domain through the configured DNS server.
   - **HTTPS:** sends an HTTPS request and evaluates the returned HTTP status code.
   - **SSH:** reads the server identification banner and checks that it begins with `SSH`.

These checks help distinguish basic network reachability from port availability and application-level service health.

## Logging

Each run writes a compact record for every device to:

```
logs/network_log.txt
```

The log includes the timestamp, device information, resolved address, ping result and latency, TCP port status, and service-specific health result.

## Version 1

Version 1 focuses on lightweight command-line monitoring for DNS, HTTPS, and SSH services.

Possible future improvements include:

- Additional service checks
- Scheduled monitoring and alerts
- Monitoring for local or virtual lab devices
- Improved reporting or dashboard visualization