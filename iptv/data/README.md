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
      "usage": "",              /* (String) Required: The usage of the URL; eg. direct, streamlink, streamlink_301 or web */
      "streamlink_data": {},    /* (Object) Optional: additional streamlink URL options; eg. {"http-header": "User-Agent=Mozilla"} */
      "direct_data": {},        /* (Object) Optional: additional direct URL options; eg. {"User-Agent": "Mozilla"} */
      "attributes": {
        "datetime": "",         /* (String)  Optional: An ISO 8601 Timestamp of the last update; eg. 1970-01-01T00:00:00.000-00:00 */
        "geolocked": "",        /* (Boolean) Optional: If the stream is geolocked or not; Default=false */
        "authentication": "",   /* (Boolean) Optional: If the streams require authentication; Default=false */
        "subscription": "",     /* (Boolean) Optional: If the stream requires a subscription; Default=false */
        "drm": "",              /* (Boolean) Optional: If the stream is protected by DRM; Default=false */
        "hd": ""                /* (Boolean) Optional: If the stream is available in High Definition; Default=false */
      }
    }
  ],
  "m3u": {           /* (Object) Optional: Metadata for m3u files. */
    "logo": "",      /* (String) Optional: channel logo URL; eg. http://foo.bar/logo.png */
    "id": "",        /* (String) Optional: TV guide channel ID */
    "shift": "",     /* (String) Optional: TV guide time shifting */
    "name": "",      /* (String) Optional: TV guide channel name */
    "radio": false,  /* (Boolean) Optional: Audio only; Default=false */
    "chno": "",      /* (String) Optional: Channel number; eg. 35 */
    "group": ""      /* (String) Optional: Group Titles separated by a semicolon; eg. News;Sports */
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
      "usage": "direct streamlink streamlink_301 web",
      "streamlink_data": {},
      "direct_data": {},
      "attributes": {
        "datetime": "",
        "geolocked": false true,
        "authentication": false true,
        "subscription": false true,
        "drm": false true,
        "hd": false true
      }
    }
  ],
  "m3u": {
    "logo": "",
    "id": "",
    "shift": "",
    "name": "",
    "radio": false,
    "chno": "",
    "group": ""
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
      "usage": "direct streamlink streamlink_301 web",
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
    "chno": "",
    "group": ""
  }
}
```
