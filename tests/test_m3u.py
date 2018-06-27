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

    def test_m3u_name_netloc(self):
        test_data = [
            ('https://www.zdf.de/', 'zdf.de'),
            ('https://www.5-tv.ru/live/', '5-tv.ru'),
            ('https://www.fox.com.tr/canli-yayin', 'fox.com.tr'),
            ('https://www.bbc.co.uk/iplayer/live/bbcone', 'bbc.co.uk'),
        ]

        for url, result in test_data:
            self.assertEqual(self.m3u.m3u_name_netloc(url), result)
