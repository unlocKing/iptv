mydata = [
    {
        "priority": "50",
        "channel_data": [
            {
                "name": "Das Erste | zattoo.com",
                "url": "https://zattoo.com/watch/daserste",
                "type": "streamlink",
                "streamlink_data": {
                    "zattoo-email": "EMAIL",
                    "zattoo-password": "PASSWORD",
                },
            },
            {
                "name": "Das Erste | daserste.de",
                "url": "https://www.daserste.de/live/index.html",
                "type": "streamlink",
                "streamlink_data": {},
            },
            {
                "broken": "true",
                "name": "Das Erste | akamaihd.net",
                "url": "https://daserstelive-lh.akamaihd.net/i/..._av-p.m3u8",
                "type": "m3u8",
                "m3u8_data": {
                    "X-Forwarded-For": "127.0.0.1",
                    "Referer": "https://www.daserste.de/",
                }
            }
        ],
        "group": [
            "Deutsch",
            "Vollprogramm",
        ],
        "tvg-logo": "v1/de_ard_das_erste.png",
        "tvg-id": "ARD",
        "tvg-shift": "",
        "tvg-name": "",
    },
    {
        "priority": "50",
        "channel_data": [
            {
                "name": "ZDF | zattoo.com",
                "url": "https://zattoo.com/watch/zdf",
                "type": "streamlink",
                "streamlink_data": {
                    "zattoo-email": "EMAIL",
                    "zattoo-password": "PASSWORD",
                },
            }
        ],
        "group": [
            "Deutsch",
            "Vollprogramm",
        ],
        "tvg-logo": "v1/de_zdf.png",
        "tvg-id": "ZDF",
        "tvg-shift": "",
        "tvg-name": "",
        "radio": "false"
    },
]

__all__ = ["mydata"]
