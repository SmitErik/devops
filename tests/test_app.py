import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import unittest
from main import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.ips = [20, 21, 22, 23]
        self.endpoints = ['/', '/current_time', '/fun_fact', '/metrics']

    def test_endpoints(self):
        successful_tests = 0
        failed_tests = 0
        for ip in self.ips:
            for endpoint in self.endpoints:
                url = f'http://172.100.0.{ip}:5000{endpoint}'
                try:
                    response = requests.get(url)
                    self.assertEqual(response.status_code, 200)
                    successful_tests += 1
                except requests.exceptions.RequestException as e:
                    failed_tests += 1
                    self.fail(f'{ip} on {endpoint} failed with error: {e}')

        self.assertGreater(successful_tests, 0, "No successful tests")
        self.assertGreater(failed_tests, 0, f"Some tests failed. Total failed: {failed_tests}")

if __name__ == '__main__':
    unittest.main()
