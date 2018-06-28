# iptv

[![Build Status](https://travis-ci.org/back-to/iptv.svg?branch=master)](https://travis-ci.org/back-to/iptv)

IPTV is a **M3U Playlist Generator** and a **TV Channel database**.

- Source: https://github.com/back-to/iptv
- Issues: https://github.com/back-to/iptv/issues
- PyPI: https://pypi.org/project/iptv/

# Installation

#### Installation via Python pip

Python **3.5+** is required

```
pip install git+https://github.com/back-to/iptv.git
```

##### Dependencies

**fastjsonschema**

IPTV is currently only tested with the dev version,
you might need to install it.

```
pip install git+https://github.com/seznam/python-fastjsonschema.git
```

# Guide

## JSON file

```
iptv json -h
```

JSON file example https://github.com/back-to/iptv/tree/master/iptv/data

## M3U file

```
iptv m3u -h
```
