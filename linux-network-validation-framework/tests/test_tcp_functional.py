import unittest

from app.tcp_client import send_tcp
from app.tcp_server import TCPServer


class TCPFunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TCPServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_tcp_ping_pong(self):
        response, _ = send_tcp("127.0.0.1", self.server.port, "PING")
        self.assertEqual(response, "PONG")

    def test_tcp_echo(self):
        response, _ = send_tcp("127.0.0.1", self.server.port, "ECHO hello")
        self.assertEqual(response, "hello")

    def test_tcp_uppercase_command(self):
        response, _ = send_tcp("127.0.0.1", self.server.port, "UPPER network qa")
        self.assertEqual(response, "NETWORK QA")

    def test_tcp_latency_is_measured(self):
        _, duration_ms = send_tcp("127.0.0.1", self.server.port, "PING")
        self.assertGreaterEqual(duration_ms, 0)

    def test_tcp_large_payload(self):
        payload = "x" * 8000
        response, _ = send_tcp("127.0.0.1", self.server.port, f"ECHO {payload}")
        self.assertEqual(response, payload)
