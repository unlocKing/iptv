# iptv

IPTV M3U Playlist Generator for LiveProxy

# Guide

create a file called `defaults.cfg`
a valid file can be found in the [example](https://github.com/back-to/iptv/tree/master/example) folder.

create a valid json file for every channel in the folder `streams`,
for this example the file name will be `DasErste.json`,


```json
{
    "priority": "50",
    "channel_data": [
        {
            "name": "Das Erste HD",
            "url": "https://zattoo.com/watch/ard",
            "type": "streamlink",
            "streamlink_data": {
                "zattoo-email": "EMAIL",
                "zattoo-password": "PASSWORD"
            }
        }
    ],
    "group": [
        "Deutsch"
    ],
    "tvg-logo": "v1/das_erste.png",
    "tvg-id": "Das Erste",
    "tvg-name": "Das Erste"
}
```

After you created all valid files ...

- Run `python run.py` to create a playlist.m3u
- Run `python upload.py` to upload the m3u file to a ftp server

# requirements

- **this iptv files** https://github.com/back-to/iptv/archive/master.zip
- **Python 3.5+** https://www.python.org/downloads/

# Questions

- You can open an issue here https://github.com/back-to/iptv/issues
