import socket
import unittest

from app.tcp_client import send_tcp
from app.tcp_server import TCPServer


class NegativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TCPServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_unknown_command(self):
        response, _ = send_tcp("127.0.0.1", self.server.port, "NOT_A_COMMAND")
        self.assertEqual(response, "ERROR:UNKNOWN_COMMAND")

    def test_closed_port_connection_fails(self):
        temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp.bind(("127.0.0.1", 0))
        closed_port = temp.getsockname()[1]
        temp.close()

        with self.assertRaises(OSError):
            send_tcp("127.0.0.1", closed_port, "PING", timeout=0.2)

    def test_timeout_is_detected(self):
        with self.assertRaises(socket.timeout):
            send_tcp("127.0.0.1", self.server.port, "SLOW", timeout=0.05)

    def test_graceful_close_returns_empty_response(self):
        response, _ = send_tcp("127.0.0.1", self.server.port, "CLOSE")
        self.assertEqual(response, "")
