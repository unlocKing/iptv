# -*- coding: utf-8 -*-
import json
import logging
import os.path
import pathlib

from datetime import datetime, timezone
from fastjsonschema import compile, JsonSchemaException
from time import time

from iptv.constants import JSON_SCHEMA
from iptv.output import write_data

log = logging.getLogger(__name__)


def create_json_data(args):
    iso_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    data = {
        'country': args.country.upper(),
        'language': args.language.lower(),
        'm3u': {
            'chno': args.chno,
            'group': args.group,
            'id': args.id,
            'logo': args.logo,
            'name': args.name_epg,
            'radio': args.radio,
            'shift': args.shift
        },
        'name': args.name,
        'streams': [
            {
                'attributes': {
                    'authentication': args.authentication,
                    'datetime': iso_time,
                    'drm': args.drm,
                    'geolocked': args.geolocked,
                    'hd': args.hd,
                    'subscription': args.subscription
                },
                'direct_data': {},
                'streamlink_data': {},
                'url': args.url.lower(),
                'usage': args.usage.lower()
            }
        ]
    }

    validate = compile(JSON_SCHEMA)

    try:
        data = validate(data)
    except JsonSchemaException as e:
        log.debug('invalid JSON:\n{0}'.format(json.dumps(data,
                                                         sort_keys=True,
                                                         indent=4,
                                                         ensure_ascii=False)))
        log.error('{0}'.format(str(e)))
        return ''

    data = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    data += '\n'

    if args.output:
        p_path = os.path.join(args.output, args.country.upper())
    else:
        p_path = os.path.join(os.path.dirname(__file__),
                              'data', args.country.upper())

    pathlib.Path(p_path).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(p_path, args.name.replace(' ', '-'))
    suffix = '.json'

    file_d = filename + suffix
    if os.path.isfile(file_d):
        log.debug('File already exists. Using a different file instead.')
        file_d = filename + '_' + str(int(time())) + suffix

    write_data(file_d, data)
