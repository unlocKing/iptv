# -*- coding: utf-8 -*-
import argparse

from textwrap import dedent

from iptv import __version__
from iptv.constants import HOST, PORT
from iptv.utils import comma_list


def build_parser():
    '''create the args parser for IPTV'''

    parser = argparse.ArgumentParser(
        prog='iptv',
        fromfile_prefix_chars='@',
        add_help=True,
        description=dedent('''
        IPTV is a command-line utility that creates valid M3U playlist files.
        '''),
        epilog=dedent('''
        Please report bugs to the issue tracker on Github:
          https://github.com/back-to/iptv/issues
        ''')
    )

    subparsers = parser.add_subparsers(dest='which')

    general = parser.add_argument_group('General options')
    general.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s {0}'.format(__version__),
        help='''
        Show version number and exit.
        '''
    )

    # --- START M3U --- #
    m3u_options = subparsers.add_parser(
        'm3u',
        usage='''
        iptv m3u [OPTIONS]
        ''',
        help='''
        create a M3U file
        '''
    )
    m3u = m3u_options.add_argument_group('M3U options')
    m3u.add_argument(
        '--output',
        metavar='FILENAME',
        required=True,
        help='''
        Write m3u data to FILENAME
        '''
    )
    m3u.add_argument(
        '--clean-metadata',
        action='store_true',
        help='''
        Removes all M3U metadata and creates a clean playlist.
        '''
    )
    m3u.add_argument(
        '--group-country',
        action='store_true',
        default=False,
        help='''
        Adds the country iso code as a m3u group.

          "RU"

        Default: False
        '''
    )
    m3u.add_argument(
        '--group-language',
        action='store_true',
        default=False,
        help='''
        Adds the language iso code as a m3u group.

          "RUS"

        Default: False
        '''
    )
    m3u.add_argument(
        '--limit-group',
        action='store_true',
        default=False,
        help='''
        Add only the first m3u group instead of multiple,
        some players will not correctly with multiple groups.

        Default: False
        '''
    )
    m3u.add_argument(
        '--limit-mirror',
        type=int,
        default=3,
        metavar='NUMBER',
        help='''
        Limit the number of Channel URL mirrors,
        that will be added to the playlist.

        Default: 3
        '''
    )
    m3u.add_argument(
        '--logopath',
        type=str,
        metavar='PATH',
        help='''
        Custom Channels can have a logo set without a path,
        it can be added afterwards with this.
        '''
    )
    m3u.add_argument(
        '--host',
        type=str,
        metavar='HOST',
        default=HOST,
        help='''
        IP for LiveProxy

        Default: {0}
        '''.format(HOST)
    )
    m3u.add_argument(
        '--port',
        type=str,
        metavar='PORT',
        default=PORT,
        help='''
        PORT for LiveProxy

        Default: {0}
        '''.format(PORT)
    )
    m3u.add_argument(
        '--direct-to-streamlink',
        action='store_true',
        help='''
        Use direct URLs with a streamlink URL for LiveProxy.
        '''
    )

    name = m3u_options.add_argument_group("Channel name options")
    name.add_argument(
        '--name-netloc',
        action='store_true',
        help='''
        Adds the netloc of an URL after the Channel name.

          "BBC 1 | bbc.co.uk"

        '''
    )
    name.add_argument(
        '--name-no-hd',
        action='store_true',
        help='''
        Removes `HD` after every HD Channel name.
        '''
    )

    remove = m3u_options.add_argument_group("Remove TV Channels options")
    remove.add_argument(
        '--remove-name',
        type=comma_list,
        metavar='CHANNEL',
        help='''
        Removes all Channels with the selected Names
        by using a comma-separated list:

          "Das Erste,Россия 24"

        Note: The name must be the same as in the JSON files.
        '''
    )
    remove.add_argument(
        '--remove-radio',
        action='store_true',
        default=False,
        help='''
        Removes every Radio Channel.
        '''
    )
    remove.add_argument(
        '--remove-group',
        type=comma_list,
        metavar='GROUP',
        help='''
        Removes all Channels with specified groups,
        by using a comma-separated list:

          "News,FR"

        '''
    )
    remove.add_argument(
        '--remove-country',
        type=comma_list,
        metavar='ISO-CODE',
        help='''
        Removes all Channels with specified countries,
        by using a comma-separated list:

          "FR,RU"

         Opposite of --source-country
        '''
    ),
    remove.add_argument(
        '--remove-language',
        type=comma_list,
        metavar='ISO-CODE',
        help='''
        Removes all Channels with specified languages,
        by using a comma-separated list:

          "deu,rus"

        Opposite of --source-language
        '''
    )
    remove.add_argument(
        '--only-direct',
        action='store_true',
        help='''
        Removes all Channels without a direct stream URL.
        '''
    )

    source = m3u_options.add_argument_group("Data source options")
    source.add_argument(
        '--source-country',
        type=comma_list,
        metavar='ISO-CODE',
        help='''
        Allow only selected countries

        Opposite of --remove-country
        '''
    )
    source.add_argument(
        '--source-language',
        type=comma_list,
        metavar='ISO-CODE',
        help='''
        Allow only selected languages

        Opposite of --remove-language
        '''
    )
    source.add_argument(
        '--source-dirs-public',
        type=comma_list,
        metavar='PATH',
        help='''
        Similar to --source-country and --remove-country
        but it won't load all data only the selected dirs.
        '''
    )
    source.add_argument(
        '--source-dirs-private',
        type=comma_list,
        metavar='PATH',
        help='''
        Use Private JSON files from a different folder,
        if this is used only the selected PATHs will be added.
        '''
    )
    # --- END M3U --- #

    # --- START JSON --- #
    _json = subparsers.add_parser(
        'json',
        help='''
        create a JSON data file
        '''
    )
    _options = _json.add_argument_group(
        'JSON options',
        'create a valid JSON data file for private or public Channels'
    )
    _options.add_argument(
        '--output',
        metavar='FOLDER',
        default=False,
        help='''
        Folder where the generated JSON file will be stored.

        Default: public folder in "iptv/data/"
        '''
    )
    _options.add_argument(
        '--country',
        type=str,
        required=True,
        metavar='ISO-CODE',
        help='''
        (String) Optional: An ISO 3166-1 alpha-2 country code; eg. BE'
        '''
    )
    _options.add_argument(
        '--language',
        type=str,
        required=True,
        metavar='ISO-CODE',
        help='''
        (String) Optional: An ISO 639-3 language code; eg. eng
        '''
    )
    _options.add_argument(
        '--name',
        type=str,
        required=True,
        default='',
        metavar='NAME',
        help='''
        (String) Required: A TV Channel Name; eg. TV1
        '''
    )

    _json_m3u = _json.add_argument_group('M3U meta data')
    _json_m3u.add_argument(
        '--chno',
        type=str,
        metavar='CHNO',
        default='',
        help='''
        (String) Optional: Channel number; eg. 35
        '''
    )
    _json_m3u.add_argument(
        '--group',
        type=str,
        metavar='GROUP',
        default='',
        help='''
        (String) Optional: Group Titles separated by a semicolon; eg. News;Sports
        '''
    )
    _json_m3u.add_argument(
        '--id',
        type=str,
        metavar='ID',
        default='',
        help='''
        (String) Optional: TV guide channel ID
        '''
    )
    _json_m3u.add_argument(
        '--logo',
        type=str,
        metavar='LOGO',
        default='',
        help='''
        (String) Optional: channel logo URL; eg. http://foo.bar/logo.png
        '''
    )
    _json_m3u.add_argument(
        '--name-epg',
        type=str,
        metavar='NAME',
        default='',
        help='''
        (String) Optional: TV guide channel name
        '''
    )
    _json_m3u.add_argument(
        '--radio',
        action='store_true',
        default=False,
        help='''
        (Boolean) Optional: Audio only; Default=false
        '''
    )
    _json_m3u.add_argument(
        '--shift',
        type=str,
        metavar='SHIFT',
        default='',
        help='''
        (String) Optional: TV guide time shifting
        '''
    )

    _json_stream = _json.add_argument_group('Stream data')
    _json_stream.add_argument(
        '--authentication',
        action='store_true',
        default=False,
        help='''
        (Boolean) Optional: If the streams require authentication; Default=false
        '''
    )
    _json_stream.add_argument(
        '--drm',
        action='store_true',
        default=False,
        help='''
        (Boolean) Optional: If the stream is protected by DRM; Default=false
        '''
    )
    _json_stream.add_argument(
        '--geolocked',
        action='store_true',
        default=False,
        help='''
        (Boolean) Optional: If the stream is geolocked or not; Default=false
        '''
    )
    _json_stream.add_argument(
        '--hd',
        action='store_true',
        default=False,
        help='''
        (Boolean) Optional: If the stream is available in High Definition; Default=false
        '''
    )
    _json_stream.add_argument(
        '--subscription',
        action='store_true',
        default=False,
        help='''
        (Boolean) Optional: If the stream requires a subscription; Default=false
        '''
    )
    _json_stream.add_argument(
        '--url',
        type=str,
        required=True,
        metavar='URL',
        help='''
        (String) Required: The URL for the stream, eg. https://www.daserste.de/live/index.html
        '''
    )
    _json_stream.add_argument(
        '--usage',
        type=str,
        required=True,
        metavar='USAGE',
        help='''
        (String) Required: The usage of the URL; eg. direct, streamlink, streamlink_301 or web
        '''
    )
    # --- END JSON --- #

    return parser


__all__ = [
    'build_parser',
]
