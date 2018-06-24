#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os.path

from fastjsonschema import JsonSchemaException, compile
from pathlib import Path

from iptv.utils import schema

FORMAT = '[%(name)s][%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



def main():
    p = Path(os.path.dirname(__file__))
    json_files = list(p.glob('data/**/*.json'))

    validate = compile(schema)

    log.info('Load JSON data')
    data = []
    for json_file in json_files:
        with json_file.open() as f:
            try:
                data += [validate(json.load(f))]
            except JsonSchemaException as e:
                log.error('{0}: {1}'.format(
                    os.path.join(json_file.parts[-2],
                                 json_file.parts[-1]),
                    str(e),
                ))
    return log.info('Found {0} channels'.format(len(data)))
