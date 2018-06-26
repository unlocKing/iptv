#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os.path
import platform
import sys

from fastjsonschema import (
    compile,
    JsonSchemaException,
    VERSION as fastjsonschema_version,
)
from glob import glob
from iptv import __version__ as iptv_version
from iptv.constants import JSON_SCHEMA
from iptv.m3u import PlaylistM3U
from iptv.utils import comma_list

FORMAT = '[%(name)s][%(levelname)s] %(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)


def sort_streams(item):
    return (item['m3u'].get('chno', '9999'),
            item.get('language', 'ZZZ'),
            item['name'])


def get_json_files(public=None, private=None):
    '''
    :param public: ** or ISO 3166-1 alpha-2 code that should be used
    :param private: path of data folders
    '''
    folders = []

    if private:
        folders = comma_list(private)
    else:
        if public is None:
            public = '**'
            log.debug('Using all public Directorys.')

        for p_dir in comma_list(public):
            p_folder = os.path.join(os.path.dirname(__file__), 'data', p_dir)
            folders += [p_folder]

    json_files = []
    for _f in folders:
        if not (_f.endswith('**') or os.path.isdir(_f)):
            log.error('Directory does not exist. {0}'.format(_f))
            folders.remove(_f)
            continue
        log.debug('Added Directory {0}'.format(_f))
        json_files += list(glob(os.path.join(_f, '*.json')))

    return json_files


def log_current_versions():
    '''Show current installed versions'''
    # MAC OS X
    if sys.platform == 'darwin':
        os_version = 'macOS {0}'.format(platform.mac_ver()[0])
    # Windows
    elif sys.platform.startswith('win'):
        os_version = '{0} {1}'.format(platform.system(), platform.release())
    # linux / other
    else:
        os_version = platform.platform()

    log.info('OS:     {0}'.format(os_version))
    log.info('Python: {0}'.format(platform.python_version()))
    log.info('IPTV:   {0}'.format(iptv_version))
    log.debug('Fastjsonschema({0})'.format(fastjsonschema_version))


def main():
    log_current_versions()

    # XXX add args
    options = {
        'm3u-netloc': True,
    }

    validate = compile(JSON_SCHEMA)

    log.info('Load JSON data')
    data = []

    public = private = None
    json_files = get_json_files(public=public, private=private)

    for json_file in json_files:
        with open(json_file) as f:
            try:
                data += [validate(json.load(f))]
            except JsonSchemaException as e:
                log.error('{0}: {1}'.format(
                    os.path.join(json_file.parts[-2],
                                 json_file.parts[-1]),
                    str(e),
                ))
    log.info('Found {0} channels'.format(len(data)))

    m3u = PlaylistM3U()
    data = sorted(data, key=sort_streams)

    lines = '#EXTM3U\n'
    for _x in data:
        lines += m3u._generate(_x, options=options)
