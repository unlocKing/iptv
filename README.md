# WARNING

## Project is currently under reconstruction

Most of it will be changed and moved to a different folder.

If you used this project, just use an old commit until it's finished.

# iptv

IPTV M3U Playlist Generator for LiveProxy

# Guide

1. create a file called `defaults.cfg` [example](https://github.com/back-to/iptv/blob/master/example/defaults.example.cfg)

2. create a folder called `private`

3. copy your wanted streams from `streams` into `private`
   or create your own `.json` files.

Some of the streams will only work with [back-to/plugins](https://github.com/back-to/plugins)

**Example**

only valid json files will work.

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

# requirements

- **this iptv files** https://github.com/back-to/iptv/archive/master.zip
- **Python 3.6+** https://www.python.org/downloads/

# Questions

- You can open an issue here https://github.com/back-to/iptv/issues
