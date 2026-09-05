import unittest
from concurrent.futures import ThreadPoolExecutor

from app.tcp_client import send_tcp
from app.tcp_server import TCPServer


class ConcurrencyRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.server = TCPServer()
        self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_multiple_simultaneous_clients(self):
        def ping(_):
            response, _ = send_tcp("127.0.0.1", self.server.port, "PING")
            return response

        with ThreadPoolExecutor(max_workers=10) as pool:
            results = list(pool.map(ping, range(10)))

        self.assertEqual(results, ["PONG"] * 10)

    def test_repeated_connections(self):
        for _ in range(15):
            response, _ = send_tcp("127.0.0.1", self.server.port, "PING")
            self.assertEqual(response, "PONG")

    def test_server_restart_recovery(self):
        old_port = self.server.port
        self.server.restart()
        self.assertTrue(self.server.is_running())
        self.assertNotEqual(self.server.port, 0)
        response, _ = send_tcp("127.0.0.1", self.server.port, "PING")
        self.assertEqual(response, "PONG")
