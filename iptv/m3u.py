# -*- coding: utf-8 -*-
import logging

from collections import namedtuple
from urllib.parse import urljoin, urlencode, urlparse

from iptv.utils import comma_list, comma_list_filter_remove

log = logging.getLogger(__name__)

Stream = namedtuple(
    'Stream', 'name country language usage hd dataline'
)


class PlaylistM3U(object):

    def sort_streams(self, item):
        return (-item['attributes'].get('hd', False),
                -item['attributes'].get('geolocked', False),
                -item['attributes'].get('authentication', False),
                -item['attributes'].get('subscription', False),
                -item['attributes'].get('drm', False),
                item['usage'],
                item['url'])

    def m3u_group_iso(self, group, args, country, language):
        if (args.group_language and language):
            group = ';'.join(filter(None, [language.upper(), group]))
        if (args.group_country and country):
            group = ';'.join(filter(None, [country.upper(), group]))
        return group

    def m3u_item(self, item, value):
        if not (item and value):
            return ''
        return f' {item}="{value}"'

    def m3u_key(self, key, stream_m3u, data_m3u):
        try:
            return stream_m3u[key]
        except (KeyError, TypeError):
            try:
                return data_m3u[key]
            except (KeyError, TypeError):
                return ''

    def m3u_logopath(self, logo, logopath):
        if not logo:
            return
        elif logopath and not logo.startswith(('http://', 'https://')):
            logo = urljoin(logopath, logo)

        if logo.startswith(('http://', 'https://')):
            return logo

    def m3u_metadata(self, stream_m3u, data_m3u, m3u_tvg_logo):
        tvg_chno = self.m3u_item('tvg-chno',
                                 self.m3u_key('chno', stream_m3u, data_m3u))
        tvg_id = self.m3u_item('tvg-id',
                               self.m3u_key('id', stream_m3u, data_m3u))
        tvg_name = self.m3u_item('tvg-name',
                                 self.m3u_key('name', stream_m3u, data_m3u))
        tvg_shift = self.m3u_item('tvg-shift',
                                  self.m3u_key('shift', stream_m3u, data_m3u))
        tvg_logo = self.m3u_item('tvg-logo', m3u_tvg_logo)
        tvg_radio = self.m3u_item('radio', 'true') if self.m3u_key('radio', stream_m3u, data_m3u) else ''

        line = (f'#EXTINF:-1{tvg_id}{tvg_name}{tvg_chno}{tvg_shift}'
                + f'{tvg_radio}{tvg_logo}')

        return line

    def m3u_name_netloc(self, url):
        '''
        removes subdomains from an URL

        :param url: URL
        '''
        _url_netloc = urlparse(url).netloc.split('.')
        url_netloc = f'{_url_netloc[-2]}.{_url_netloc[-1]}'

        if (len(url_netloc) <= 6
                and len(_url_netloc) >= 3
                and _url_netloc[-3] != 'www'):
            url_netloc = f'{_url_netloc[-3]}.{url_netloc}'

        return url_netloc

    def _generate(self, data, args):
        lines = []
        streams = sorted(data['streams'],
                         key=lambda x: self.sort_streams(x))

        for stream in streams:
            _stream_m3u = stream.get('m3u')
            data_m3u = data.get('m3u')

            if self.m3u_key('radio', _stream_m3u, data_m3u) and args.remove_radio:
                continue

            if args.clean_metadata:
                data_m3u = _stream_m3u = {}

            m3u_tvg_logo = self.m3u_logopath(
                self.m3u_key('logo', _stream_m3u, data_m3u), args.logopath)

            line = self.m3u_metadata(_stream_m3u, data_m3u, m3u_tvg_logo)

            stream_attributes = stream.get('attributes')
            stream_direct_data = stream.get('direct_data')
            stream_streamlink_data = stream.get('streamlink_data')

            _stream_usage = stream['usage']
            _stream_name = (stream.get('name') or data.get('name') or 'unknown')

            if (args.remove_name and (_stream_name.lower() in [
                    e.lower() for e in args.remove_name])):
                log.debug(f'Removed name: {_stream_name}')
                continue

            _stream_language = stream.get('language') or data.get('language')
            if not _stream_language:
                log.error(f'Missing language code for {_stream_name}')
                continue

            _stream_country = stream.get('country') or data.get('country')
            if not _stream_country:
                log.error(f'Missing country code for {_stream_name}')
                continue

            if (args.remove_country and (_stream_country.lower() in [
                    e.lower() for e in args.remove_country])):
                log.debug(f'Removed country {_stream_country}: {_stream_name}')
                continue

            if (args.remove_language and (_stream_language.lower() in [
                    e.lower() for e in args._stream_language])):
                log.debug(f'Removed language {_stream_language}: {_stream_name}')
                continue

            if (args.source_country and (_stream_country.lower() not in [
                    e.lower() for e in args.source_country])):
                continue
            if (args.source_language and (_stream_language.lower() not in [
                    e.lower() for e in args.source_language])):
                continue

            if args.only_direct and not _stream_usage == 'direct':
                log.debug(f'Skip {_stream_usage}: {_stream_name}')
                continue

            if _stream_usage == 'web':
                log.error(
                    f'Streams with the usage WEB can not be added. {_stream_name}')
                continue

            if stream_attributes.get('drm'):
                log.error(
                    f'Streams with DRM protection can not be added. {_stream_name}')
                continue

            if (stream_attributes.get('authentication')
                    or stream_attributes.get('subscription')):
                log.info('Added a stream which requires an authentication '
                         f'or a subscription. {_stream_name}')

            if not args.clean_metadata:
                _group = self.m3u_group_iso(self.m3u_key('group', _stream_m3u, data_m3u),
                                            args,
                                            _stream_country,
                                            _stream_language)
            else:
                _group = ''

            if (args.remove_group and _group):
                _le = len(_group)
                _f = comma_list_filter_remove(args.remove_group, ';')
                _group = ';'.join(filter(None, _f(_group)))
                if len(_group) != _le:
                    log.debug(f'Removed group: {_stream_name}')
                    continue

            if (args.limit_group and _group):
                if isinstance(_group, str):
                    _group = comma_list(_group, ';')
                if isinstance(_group, list) and len(_group) > 0:
                    _group = _group[0]

            tvg_group = self.m3u_item('group-title', _group)

            stream_line = f'{line}{tvg_group},{_stream_name}'

            if (not args.name_no_hd and stream_attributes.get('hd')):
                stream_line += ' HD'
            if args.name_netloc:
                url_netloc = self.m3u_name_netloc(stream['url'])
                stream_line += f' | {url_netloc}'
            stream_line += '\n'

            # XXX args.direct_to_streamlink
            if _stream_usage == 'direct':
                stream_line += stream['url']
                if stream_direct_data:
                    params = []
                    for k in stream_direct_data.keys():
                        params += [f'{k}={stream_direct_data[k]}']
                    if params:
                        stream_line += '|'
                        stream_line += '|'.join(params)
            elif (_stream_usage == 'streamlink'
                  or _stream_usage == 'streamlink_301'):

                stream_streamlink_data.update({'url': stream['url']})

                stream_line += (f'http://{args.host}:{args.port}/{_stream_usage}'
                                + f'/?{urlencode(stream_streamlink_data)}')

            stream_line += '\n'
            lines += [
                Stream(_stream_name,
                       _stream_country,
                       _stream_language,
                       _stream_usage,
                       stream_attributes.get('hd'),
                       stream_line
                       )
            ]

        return lines
