import socket
import time


def send_udp(host, port, message, timeout=1.0):
    start = time.perf_counter()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(message.encode("utf-8"), (host, port))
        data, _ = sock.recvfrom(65536)
    duration_ms = (time.perf_counter() - start) * 1000
    return data.decode("utf-8"), duration_ms
