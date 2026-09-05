import socket
import time


def send_tcp(host, port, message, timeout=1.0):
    start = time.perf_counter()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall(message.encode("utf-8"))
        data = sock.recv(65536)
    duration_ms = (time.perf_counter() - start) * 1000
    return data.decode("utf-8"), duration_ms
