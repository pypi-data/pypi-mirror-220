import unittest
from scraputils.advanced_request import AdvancedRequest

class TestAdvancedRequest(unittest.TestCase):
    def test_headers(self):
        request = AdvancedRequest('http://example.com')
        self.assertIn('User-Agent', request.headers)
        self.assertIsNotNone(request.headers['User-Agent'])

if __name__ == '__main__':
    unittest.main()
