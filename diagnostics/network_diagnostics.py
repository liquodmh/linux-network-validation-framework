import platform
import shutil
import socket
import subprocess
import time


def _run(command):
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        return {
            "command": " ".join(command),
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except Exception as exc:
        return {
            "command": " ".join(command),
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
        }


def check_tcp_port(host, port, timeout=0.5):
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.perf_counter() - start) * 1000
            return {
                "reachable": True,
                "latency_ms": round(elapsed, 2),
                "error": None,
            }
    except OSError as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "reachable": False,
            "latency_ms": round(elapsed, 2),
            "error": str(exc),
        }


def collect_linux_network_state(host="127.0.0.1", port=None):
    report = {
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "target_host": host,
    }

    if port is not None:
        report["tcp_port_check"] = check_tcp_port(host, port)

    # These commands are collected only when available.
    commands = [
        (["ip", "addr"], "ip_addr"),
        (["ip", "route"], "ip_route"),
        (["ss", "-lnt"], "listening_tcp"),
        (["ping", "-c", "1", host], "ping"),
    ]

    for command, key in commands:
        if shutil.which(command[0]):
            report[key] = _run(command)
        else:
            report[key] = {"available": False}

    return report
