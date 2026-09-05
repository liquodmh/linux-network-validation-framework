import unittest

from app.udp_client import send_udp
from app.udp_server import UDPServer


class UDPFunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = UDPServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_udp_ping_pong(self):
        response, _ = send_udp("127.0.0.1", self.server.port, "PING")
        self.assertEqual(response, "PONG")

    def test_udp_echo(self):
        response, _ = send_udp("127.0.0.1", self.server.port, "ECHO udp-test")
        self.assertEqual(response, "udp-test")

    def test_udp_invalid_command(self):
        response, _ = send_udp("127.0.0.1", self.server.port, "BAD")
        self.assertEqual(response, "ERROR:UNKNOWN_COMMAND")
