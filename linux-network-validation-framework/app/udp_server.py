import logging
import socket
import threading
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("udp_server")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(LOG_DIR / "udp_server.log")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)


class UDPServer:
    def __init__(self, host="127.0.0.1", port=0):
        self.host = host
        self.port = port
        self._sock = None
        self._thread = None
        self._running = threading.Event()

    def start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self.host, self.port))
        self._sock.settimeout(0.2)
        self.port = self._sock.getsockname()[1]
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("UDP server started on %s:%s", self.host, self.port)

    def stop(self):
        self._running.clear()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=1)
        logger.info("UDP server stopped")

    def _loop(self):
        while self._running.is_set():
            try:
                data, addr = self._sock.recvfrom(65536)
            except socket.timeout:
                continue
            except OSError:
                break

            try:
                message = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                self._sock.sendto(b"ERROR:INVALID_ENCODING", addr)
                continue

            if message == "PING":
                response = "PONG"
            elif message.startswith("ECHO "):
                response = message[5:]
            else:
                response = "ERROR:UNKNOWN_COMMAND"

            self._sock.sendto(response.encode("utf-8"), addr)
            logger.info("UDP %s -> %r", addr, response)
