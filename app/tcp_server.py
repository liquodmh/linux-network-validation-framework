import logging
import socket
import threading
import time
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("tcp_server")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler(LOG_DIR / "tcp_server.log")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)


class TCPServer:
    def __init__(self, host="127.0.0.1", port=0):
        self.host = host
        self.port = port
        self._sock = None
        self._thread = None
        self._running = threading.Event()

    def start(self):
        if self._running.is_set():
            return

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(50)
        self._sock.settimeout(0.2)

        self.port = self._sock.getsockname()[1]
        self._running.set()
        self._thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._thread.start()
        logger.info("TCP server started on %s:%s", self.host, self.port)

    def stop(self):
        self._running.clear()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=1)
        logger.info("TCP server stopped")

    def restart(self):
        self.stop()
        time.sleep(0.05)
        self.port = 0
        self.start()

    def is_running(self):
        return self._running.is_set()

    def _accept_loop(self):
        while self._running.is_set():
            try:
                conn, addr = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            threading.Thread(
                target=self._handle_client,
                args=(conn, addr),
                daemon=True
            ).start()

    def _handle_client(self, conn, addr):
        with conn:
            try:
                data = conn.recv(65536)
                if not data:
                    logger.warning("Empty TCP payload from %s", addr)
                    return

                try:
                    message = data.decode("utf-8").strip()
                except UnicodeDecodeError:
                    conn.sendall(b"ERROR:INVALID_ENCODING")
                    logger.warning("Invalid encoding from %s", addr)
                    return

                logger.info("Received from %s: %r", addr, message)

                if message == "PING":
                    response = "PONG"
                elif message.startswith("ECHO "):
                    response = message[5:]
                elif message == "EMPTY":
                    response = ""
                elif message == "SLOW":
                    time.sleep(0.35)
                    response = "DONE"
                elif message == "CLOSE":
                    logger.info("Client requested graceful close")
                    return
                elif message.startswith("UPPER "):
                    response = message[6:].upper()
                else:
                    response = "ERROR:UNKNOWN_COMMAND"

                conn.sendall(response.encode("utf-8"))
                logger.info("Sent to %s: %r", addr, response)

            except Exception:
                logger.exception("Unhandled TCP server exception")


if __name__ == "__main__":
    server = TCPServer(port=5000)
    server.start()
    print(f"TCP server running on {server.host}:{server.port}")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
