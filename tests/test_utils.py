import unittest

from iptv.utils import comma_list


class TestUtils(unittest.TestCase):

    def test_comma_list(self):
        test_data = [
            {
                'data': 'foo.bar,example.com',
                'result': ['foo.bar', 'example.com']
            },
            {
                'data': '/var/run/foo,/var/run/foo',
                'result': ['/var/run/foo', '/var/run/foo']
            },
        ]

        for data in test_data:
            self.assertEqual(
                comma_list(data['data']), data['result'])
