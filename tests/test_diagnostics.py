import unittest

from app.tcp_server import TCPServer
from diagnostics.network_diagnostics import check_tcp_port, collect_linux_network_state


class DiagnosticTests(unittest.TestCase):
    def test_open_port_is_detected(self):
        server = TCPServer()
        server.start()
        try:
            result = check_tcp_port("127.0.0.1", server.port)
            self.assertTrue(result["reachable"])
            self.assertIsNone(result["error"])
        finally:
            server.stop()

    def test_closed_port_is_reported(self):
        result = check_tcp_port("127.0.0.1", 9, timeout=0.2)
        self.assertIn("reachable", result)
        self.assertIn("latency_ms", result)

    def test_linux_state_report_has_core_fields(self):
        result = collect_linux_network_state()
        self.assertIn("platform", result)
        self.assertIn("hostname", result)
        self.assertIn("target_host", result)
