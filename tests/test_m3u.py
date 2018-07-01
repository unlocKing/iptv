import unittest

from iptv.m3u import PlaylistM3U


class TestPlaylistM3U(unittest.TestCase):

    def setUp(self):
        self.m3u = PlaylistM3U()

    def test_m3u_item(self):
        test_data = [
            ('radio', 'true', ' radio="true"'),
            ('tvg-chno', '1', ' tvg-chno="1"'),
            ('tvg-id', '23', ' tvg-id="23"'),
            ('tvg-logo', '123.png', ' tvg-logo="123.png"'),
            ('tvg-name', 'Channel', ' tvg-name="Channel"'),
            ('tvg-shift', '2', ' tvg-shift="2"'),
            ('group-title', 'News;Sports', ' group-title="News;Sports"'),
            ('item', '', ''),
            ('', 'value', ''),
        ]

        for item, value, result in test_data:
            self.assertEqual(self.m3u.m3u_item(item, value), result)

    def test_m3u_key(self):
        test_data = [
            ('id', {}, {}, ''),
            ('id', {'id': 'stream'}, {'id': 'data'}, 'stream'),
            ('id', {'id': 'stream'}, {'id': ''}, 'stream'),
            ('id', {}, {'id': 'data'}, 'data'),
            ('id', {'id': ''}, {'id': 'data'}, ''),
        ]
        for key, stream_m3u, data_m3u, result in test_data:
            self.assertEqual(
                self.m3u.m3u_key(key,
                                 stream_m3u,
                                 data_m3u),
                result)

    def test_m3u_logopath(self):
        test_data = [
            ('img.png', 'https://www.zdf.de/', 'https://www.zdf.de/img.png'),
            ('/12.png', 'https://www.foo.bar/live/', 'https://www.foo.bar/12.png'),
            ('https://live/live.png', 'https://www/player/', 'https://live/live.png'),
            ('https://foo', '', 'https://foo'),
            ('img.png', '', None),
            ('', 'https://foo', None),
            ('img.png', 'XXXXXXXXXX', None),
        ]

        for logo, logopath, result in test_data:
            self.assertEqual(self.m3u.m3u_logopath(logo, logopath), result)

    def test_m3u_metadata(self):
        # stream_m3u - data_m3u - LOGOPATH - RESULT LINE
        test_data = [
            (
                {'id': '2', 'radio': False},
                {}, '',
                '#EXTINF:-1 tvg-id="2"'
            ),
            (
                {'radio': False}, {}, '',
                '#EXTINF:-1'
            ),
            (
                {'radio': True}, {}, '',
                '#EXTINF:-1 radio="true"'
            ),
            (
                {}, {}, 'http://example.com/foo.png',
                '#EXTINF:-1 tvg-logo="http://example.com/foo.png"'
            ),

            (
                {'shift': '4'}, {}, '',
                '#EXTINF:-1 tvg-shift="4"'
            ),
            (
                {'chno': '55', 'name': 'ID'}, {}, '',
                '#EXTINF:-1 tvg-name="ID" tvg-chno="55"'
            ),
            (
                {'chno': '222', 'name': 'ID'},
                {'chno': '55', 'name': 'ID'}, '',
                '#EXTINF:-1 tvg-name="ID" tvg-chno="222"'
            ),
            (
                {'chno': '', '': 'ID'},
                {'chno': '55', 'name': 'ID'}, '',
                '#EXTINF:-1 tvg-name="ID"'
            ),
            (
                {'name': 'ID1'},
                {'chno': '55', 'name': 'ID'}, '',
                '#EXTINF:-1 tvg-name="ID1" tvg-chno="55"'
            ),
        ]

        for _stream_m3u, _data_m3u, _logo, _result in test_data:
            self.assertEqual(
                self.m3u.m3u_metadata(
                    _stream_m3u,
                    _data_m3u,
                    _logo),
                _result)

    def test_m3u_name_netloc(self):
        test_data = [
            ('https://www.zdf.de/', 'zdf.de'),
            ('https://www.5-tv.ru/live/', '5-tv.ru'),
            ('https://www.fox.com.tr/canli-yayin', 'fox.com.tr'),
            ('https://www.bbc.co.uk/iplayer/live/bbcone', 'bbc.co.uk'),
        ]

        for url, result in test_data:
            self.assertEqual(self.m3u.m3u_name_netloc(url), result)
