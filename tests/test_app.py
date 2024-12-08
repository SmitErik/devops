import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import unittest
import socket
from main import app


def is_host_reachable(ip, port=5000):
    try:
        socket.create_connection((ip, port), timeout=2)
        return True
    except socket.error:
        return False

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.ips = [20, 21, 22, 23]
        self.endpoints = ['/', '/current_time', '/fun_fact', '/metrics']

    def test_endpoints(self):
        successful_tests = 0
        failed_tests = 0
        timeout_seconds = 2

        for ip in self.ips:
            ip_address = f"172.100.0.{ip}"
            if not is_host_reachable(ip_address):
                print(f"Skipping {ip_address}: Host not reachable")
                continue

            for endpoint in self.endpoints:
                url = f'http://{ip_address}:5000{endpoint}'
                try:
                    print(f"Testing {url}...")
                    response = requests.get(url, timeout=timeout_seconds)
                    self.assertEqual(response.status_code, 200)
                    successful_tests += 1
                except requests.exceptions.RequestException as e:
                    failed_tests += 1
                    print(f"Failed: {url} - Error: {e}")

        print(f"\nTests completed. Successful: {successful_tests}, Failed: {failed_tests}")
        self.assertGreater(successful_tests, 0, "No successful tests")

if __name__ == '__main__':
    unittest.main()
