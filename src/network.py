import subprocess
import time

def ping_host(host):
    start_time = time.perf_counter()

    result = subprocess.run(
        ["ping", "-n", "1", host],
        capture_output=True,
        text=True
        )

    end_time = time.perf_counter()

    duration = round((end_time - start_time) * 1000)

    if result.returncode == 0:
        return 'UP', duration
    else:
        return 'DOWN', duration