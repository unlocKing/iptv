import json
import unittest

from fastjsonschema import JsonSchemaException, compile
from iptv.constants import JSON_SCHEMA


class TestConstants(unittest.TestCase):

    def test_JSON_SCHEMA(self):
        validate = compile(JSON_SCHEMA)

        # valid data
        test_data = [
            '''
            {
              "name": "TV Channel",
              "country": "DE",
              "language": "deu",
              "streams": [
                {
                  "url": "https://foo.bar",
                  "usage": "streamlink",
                  "streamlink_data": {},
                  "direct_data": {},
                  "attributes": {
                    "geolocked": false,
                    "authentication": false,
                    "subscription": true,
                    "drm": false,
                    "hd": false
                  }
                }
              ],
              "m3u": {
                "logo": "https://foo.bar/img.png",
                "id": "1",
                "shift": "2",
                "name": "TV",
                "radio": false,
                "group": "News"
              }
            }
            ''',
            '''
            {
              "name": "TV Channel 2",
              "country": "DE",
              "language": "deu",
              "streams": [
                {
                  "url": "https://foo.bar",
                  "usage": "streamlink",
                  "streamlink_data": {
                    "hls-start-offset": "10:00:00"
                  },
                  "direct_data": {},
                  "attributes": {
                    "geolocked": false,
                    "authentication": false,
                    "subscription": true,
                    "drm": false,
                    "hd": false
                  }
                }
              ],
              "m3u": {
                "logo": "https://foo.bar/img.png",
                "id": "1",
                "shift": "2",
                "name": "TV",
                "radio": false,
                "group": "News"
              }
            }
            ''',
            '''
            {
              "name": "TV Channel 3",
              "country": "DE",
              "language": "deu",
              "streams": [
                {
                  "url": "https://foo.bar",
                  "usage": "direct"
                }
              ]
            }
            ''',
        ]

        for data in test_data:
            self.assertTrue(validate(json.loads(data)))

        # invalid data
        test_data = [
            # invalid length "country"
            '''
            {
              "name": "TV Channel regio",
              "country": "DE-DE",
              "language": "deu",
              "streams": [
                {
                  "url": "https://foo.bar",
                  "usage": "streamlink"
                }
              ]
            }
            ''',
            # invalid length "language"
            '''
            {
              "name": "TV Channel language",
              "country": "DE",
              "language": "deutsch",
              "streams": [
                {
                  "url": "https://foo.bar",
                  "usage": "streamlink"
                }
              ]
            }
            ''',
            # Required "url"
            '''
            {
              "name": "TV Channel url",
              "country": "DE",
              "language": "deu",
              "streams": [
                {
                  "usage": "streamlink"
                }
              ]
            }
            ''',
            # Required "usage"
            '''
            {
              "name": "TV Channel usage",
              "country": "DE",
              "language": "deu",
              "streams": [
                {
                  "url": "https://foo.bar"
                }
              ]
            }
            ''',
            # Required "streams"
            '''
            {
              "name": "TV Channel streams",
              "country": "DE",
              "language": "deu"
            }
            ''',
        ]

        for data in test_data:
            with self.assertRaises(JsonSchemaException):
                validate(json.loads(data))
