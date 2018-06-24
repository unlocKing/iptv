# JSON database of IPTV channels

IPTV channels are sorted after Country's origin

Country name is defined in ISO 3166-1 alpha-2

### JSON Example with comments

```js
{
  "name": "",                   /* (String) Required: A TV Channel Name; eg. TV1 */
  "region": "",                 /* (String) Optional: An ISO 3166-1 alpha-2 country code; eg. BE' */
  "language": "",               /* (String) Optional: An ISO 639-3 language code; eg. eng */
  "streams": [
    {
      "url": "",                /* (String) Required: The URL for the stream, eg. https://www.daserste.de/live/index.html */
      "usage": "",              /* (String) Required: The usage of the URL; eg. direct, streamlink or web */
      "streamlink_data": {},    /* (Object) Optional: additional streamlink URL options; eg. {"http-header": "User-Agent=Mozilla"} */
      "direct_data": {},        /* (Object) Optional: additional direct URL options; eg. {"User-Agent": "Mozilla"} */
      "attributes": {
        "geolocked": "",        /* (Boolean) Optional: If the stream is geolocked or not; Default=false */
        "authentication": "",   /* (Boolean) Optional: If the streams require authentication; Default=false */
        "subscription": "",     /* (Boolean) Optional: If the stream requires a subscription; Default=false */
        "drm": "",              /* (Boolean) Optional: If the stream is protected by DRM; Default=false */
        "hd": ""                /* (Boolean) Optional: If the stream is available in High Definition; Default=false */
      }
    }
  ],
  "m3u": {
    "logo": "",      /* (String) Optional: tvg-logo */
    "id": "",        /* (String) Optional: tvg-id */
    "shift": "",     /* (String) Optional: tvg-shift */
    "name": "",      /* (String) Optional: tvg-name */
    "radio": false,  /* (Boolean) Optional: radio; Default=false */
    "group": [""]    /* (String) Optional: group-title */
  }
}
```

### JSON Example without comments

```js
{
  "name": "",
  "region": "",
  "language": "",
  "streams": [
    {
      "url": "",
      "usage": "",
      "streamlink_data": {},
      "direct_data": {},
      "attributes": {
        "geolocked": "",
        "authentication": "",
        "subscription": "",
        "drm": "",
        "hd": ""
      }
    }
  ],
  "m3u": {
    "logo": "",
    "id": "",
    "shift": "",
    "name": "",
    "radio": false,
    "group": [""]
  }
}
```

### JSON Example without comments for LiveProxy

```js
{
  "name": "",
  "region": "",
  "language": "",
  "streams": [
    {
      "url": "",
      "usage": "",
      "streamlink_data": {},
      "direct_data": {}
    }
  ],
  "m3u": {
    "logo": "",
    "id": "",
    "shift": "",
    "name": "",
    "radio": false,
    "group": [""]
  }
}
```
