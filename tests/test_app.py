import unittest
from app import app

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
                    if response.status_code == 200:
                        print(f'{port} on {endpoint} - OK')
                        successful_tests += 1
                    else:
                        print(f'{port} on {endpoint} - Failed with status code {response.status_code}')
                        failed_tests += 1
                except requests.exceptions.RequestException as e:
                    print(f'{port} on {endpoint} - Failed with error: {e}')
                    failed_tests += 1

        print(f'\nTests completed. Successful: {successful_tests}, Failed: {failed_tests}')


if __name__ == '__main__':
    unittest.main()