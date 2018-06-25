# -*- coding: utf-8 -*-

JSON_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-06/schema#',
    'type': 'object',
    'title': 'IPTV Channel',
    'description': '(Object) Required: Data',
    'required': ['name', 'streams'],
    'properties': {
        'name': {
             'type': 'string',
             'description': '(String) Required: A TV Channel Name; eg. TV1'
        },
        'region': {
            'type': 'string',
            'description': '(String) Optional: An ISO 3166-1 alpha-2 country code; eg. BE',
            'minLength': 2,
            'maxLength': 2
        },
        'language': {
            'type': 'string',
            'description': '(String) Optional: An ISO 639-3 language code; eg. eng',
            'minLength': 3,
            'maxLength': 3
        },
        'streams': {
            'type': 'array',
            'description': '(Array) Required: A list of Streams',
            'items': {
                'type': 'object',
                'description': '(Object) Required: Stream informations',
                'required': ['url', 'usage'],
                'properties': {
                    'url': {
                        'type': 'string',
                        'format': 'uri',
                        'description': '(String) Required: The URL for the stream, eg. https://www.daserste.de/live/index.html'
                    },
                    'usage': {
                        'type': 'string',
                        'description': '(String) Required: The usage of the URL; eg. direct, streamlink or web'
                    },
                    'streamlink_data': {
                        'type': 'object',
                        'default': {},
                        'description': '(Object) Optional: additional streamlink URL options; eg. {"http-header": "User-Agent=Mozilla"}'
                    },
                    'direct_data': {
                        'type': 'object',
                        'default': {},
                        'description': '(Object) Optional: additional direct URL options; eg. {"User-Agent": "Mozilla"}'
                    },
                    'attributes': {
                        'type': 'object',
                        'description': '(Object) Optional: additional Stream informations',
                        'properties': {
                            'geolocked': {
                                'type': 'boolean',
                                'default': False,
                                'description': '(Boolean) Optional: If the stream is geolocked or not; Default=false'
                            },
                            'authentication': {
                                'type': 'boolean',
                                'default': False,
                                'description': '(Boolean) Optional: If the streams require authentication; Default=false'
                            },
                            'subscription': {
                                'type': 'boolean',
                                'default': False,
                                'description': '(Boolean) Optional: If the stream requires a subscription; Default=false'
                            },
                            'drm': {
                                'type': 'boolean',
                                'default': False,
                                'description': '(Boolean) Optional: If the stream is protected by DRM; Default=false'
                            },
                            'hd': {
                                'type': 'boolean',
                                'default': False,
                                'description': '(Boolean) Optional: If the stream is available in High Definition; Default=false'
                            }
                        }
                    }
                }
            }
        },
        'm3u': {
            'type': 'object',
            'description': '(Object) Optional: Metadata for m3u files, mostly used for LiveProxy.',
            'properties': {
                'logo': {
                    'type': 'string',
                    'description': '(String) Optional: tvg-logo'
                },
                'id': {
                    'type': 'string',
                    'description': '(String) Optional: tvg-id'
                },
                'shift': {
                    'type': 'string',
                    'description': '(String) Optional: tvg-shift'
                },
                'name': {
                    'type': 'string',
                    'description': '(String) Optional: tvg-name'
                },
                'radio': {
                    'type': 'boolean',
                    'default': False,
                    'description': '(Boolean) Optional: radio; Default=false'
                },
                'group': {
                    'type': 'array',
                    'description': '(Array) Optional: group-title',
                    'items': {
                        'type': 'string',
                        'description': '(String) Optional: group-title',
                    }
                }
            }
        }
    }
}

__all__ = [
    'JSON_SCHEMA',
]
