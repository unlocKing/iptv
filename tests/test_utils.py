import unittest

from iptv.utils import comma_list
from iptv.utils import comma_list_filter
from iptv.utils import comma_list_filter_remove


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
            {
                'data': 'Das Erste,Россия 24',
                'result': ['Das Erste', 'Россия 24']
            },
        ]

        for data in test_data:
            self.assertEqual(
                comma_list(data['data']), data['result'])

    def test_comma_list_filter(self):
        test_data = [
            {
                'acceptable': ['foo', 'bar', 'com'],
                'data': 'foo,example,bar',
                'result': ['foo', 'bar']
            },
            {
                'acceptable': ['DE', 'bar', 'com'],
                'data': 'DE,FR,RU,US',
                'result': ['DE']
            },
            {
                'acceptable': ['bar', 'com', 'RU'],
                'data': 'DE,FR,RU,US',
                'result': ['RU']
            },
        ]

        for data in test_data:
            func = comma_list_filter(data['acceptable'])
            self.assertEqual(func(data['data']), data['result'])

    def test_comma_list_filter_remove(self):
        test_data = [
            {
                'not_acceptable': ['foo', 'bar', 'com'],
                'data': 'foo,example,bar',
                'result': ['example']
            },
            {
                'not_acceptable': ['DE', 'Das Erste', 'bar', 'com'],
                'data': 'DE,FR,RU,US',
                'result': ['FR', 'RU', 'US']
            },
            {
                'not_acceptable': ['bar', 'Россия 24', 'foo'],
                'data': 'Das Erste,Россия 24',
                'result': ['Das Erste']
            },
            {
                'not_acceptable': ['bar', 'Das Erste', 'foo'],
                'data': 'Das Erste,Россия 24',
                'result': ['Россия 24']
            },
            {
                'not_acceptable': ['bar', 'News', 'foo'],
                'data': 'Das Erste,Россия 24,News',
                'result': ['Das Erste', 'Россия 24']
            },
        ]

        for data in test_data:
            func = comma_list_filter_remove(data['not_acceptable'])
            self.assertEqual(func(data['data']), data['result'])
