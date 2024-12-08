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
        self.ports = [5000, 5001, 5002, 5003]
        self.endpoints = ['/', '/current_time', '/fun_fact', '/metrics']


    def test_endpoints(self):
        successful_tests = 0
        failed_tests = 0
        for port in self.ports:
            for endpoint in self.endpoints:
                url = f'http://localhost:{port}{endpoint}'
                try:
                    response = requests.get(url)
                    self.assertEqual(response.status_code, 200)
                    print(f'{port} on {endpoint} - OK')
                    successful_tests += 1
                except requests.exceptions.RequestException as e:
                    print(f'{port} on {endpoint} - Failed with error: {e}')
                    failed_tests += 1

        print(f'\nTests completed. Successful: {successful_tests}, Failed: {failed_tests}')
        self.assertGreater(successful_tests, 0, "No successful tests")


if __name__ == '__main__':
    unittest.main()
