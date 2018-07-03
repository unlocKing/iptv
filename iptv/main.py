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
from iptv.argparser import build_parser
from iptv.constants import JSON_SCHEMA
# from iptv.jsondata import create_json_data
from iptv.m3u import PlaylistM3U
from iptv.output import write_data
from iptv.utils import comma_list

FORMAT = '[%(name)s][%(levelname)s] %(message)s'
logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)


def sort_streams(item):
    return (
        item.language,
        item.name.lower(),
        -item.hd,
    )


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
            log.error(f'Directory does not exist. {_f}')
            folders.remove(_f)
            continue
        log.debug(f'Added Directory {_f}')
        json_files += list(glob(os.path.join(_f, '*.json')))

    return json_files


def log_current_versions():
    '''Show current installed versions'''
    # MAC OS X
    if sys.platform == 'darwin':
        os_version = f'macOS {platform.mac_ver()[0]}'
    # Windows
    elif sys.platform.startswith('win'):
        os_version = f'{platform.system()} {platform.release()}'
    # linux / other
    else:
        os_version = platform.platform()

    log.info(f'OS:     {os_version}')
    log.info(f'Python: {platform.python_version()}')
    log.info(f'IPTV:   {iptv_version}')
    log.debug(f'Fastjsonschema({fastjsonschema_version})')


def m3u_load_data(args):
    log.info('Load JSON data')
    validate = compile(JSON_SCHEMA)

    data = []
    json_files = get_json_files(public=args.source_dirs_public,
                                private=args.source_dirs_private)

    for json_file in json_files:
        with open(json_file) as f:
            try:
                data += [validate(json.load(f))]
            except JsonSchemaException as e:
                log.error('{0}: {1}'.format(
                    os.path.split(json_file)[-1],
                    str(e),
                ))
    log.info(f'Found {len(data)} channels')

    m3u = PlaylistM3U()
    streams = []
    for _x in data:
        streams += m3u._generate(_x, args)
    return streams


def setup_args():
    log.debug('Set up args')
    parser = build_parser()
    arglist = sys.argv[1:]
    args, unknown = parser.parse_known_args(arglist)
    return args


def main():
    args = setup_args()
    log_current_versions()

    if args.which == 'm3u':
        '''create M3U file'''
        log.debug('Found M3U command.')
        data = m3u_load_data(args)
        data = sorted(data, key=sort_streams)

        lines = []
        cd = {}
        for x in data:
            # START - mirror
            if not cd.get(x.country):
                cd[x.country] = {}

            if not cd[x.country].get(x.language):
                cd[x.country][x.language] = {}

            if not cd[x.country][x.language].get(x.name):
                cd[x.country][x.language][x.name] = 1
            else:
                cd[x.country][x.language][x.name] += 1

            _mirror = cd[x.country][x.language][x.name]

            if args.limit_mirror <= _mirror:
                log.debug(f'Skip mirror {_mirror}: {x.name}')
                continue
            # END - mirror

            lines += [x.dataline]

        lines = ''.join(lines)
        lines = f'#EXTM3U\n{lines}'
        write_data(args.output, lines)
    elif args.which == 'json':
        '''create JSON file'''
        log.error('currently deactivated')
        # log.debug('Found JSON command.')
        # return create_json_data(args)
    else:
        log.error('invalid command name')
        return
