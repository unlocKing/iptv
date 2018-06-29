# -*- coding: utf-8 -*-
import logging

from urllib.parse import urljoin, urlencode, urlparse

log = logging.getLogger(__name__)


class PlaylistM3U(object):

    def sort_streams(self, item):
        return (-item['attributes'].get('hd', False),
                -item['attributes'].get('geolocked', False),
                -item['attributes'].get('authentication', False),
                -item['attributes'].get('subscription', False),
                -item['attributes'].get('drm', False),
                item['usage'],
                item['url'])

    def m3u_item(self, item, value):
        if not (item and value):
            return ''
        return f' {item}="{value}"'

    def m3u_logopath(self, logo, logopath):
        if not logo:
            return
        elif logopath and not logo.startswith(('http://', 'https://')):
            logo = urljoin(logopath, logo)

        if logo.startswith(('http://', 'https://')):
            return logo

    def m3u_metadata(self, channel_name, data_m3u, m3u_tvg_logo):
        tvg_group = self.m3u_item('group-title', data_m3u.get('group'))
        tvg_chno = self.m3u_item('tvg-chno', data_m3u.get('chno'))
        tvg_id = self.m3u_item('tvg-id', data_m3u.get('id'))
        tvg_name = self.m3u_item('tvg-name', data_m3u.get('name'))
        tvg_shift = self.m3u_item('tvg-shift', data_m3u.get('shift'))
        tvg_logo = self.m3u_item('tvg-logo', m3u_tvg_logo)
        tvg_radio = self.m3u_item('radio', 'true') if data_m3u.get('radio') else ''

        line = (f'#EXTINF:-1{tvg_id}{tvg_name}{tvg_chno}{tvg_shift}'
                + f'{tvg_group}{tvg_radio}{tvg_logo},{channel_name}')

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
        channel_name = data['name']
        data_m3u = data.get('m3u')

        if args.clean_metadata:
            log.debug('Removed M3U metadata.')
            data_m3u = {}

        if data_m3u.get('radio') and args.remove_radio:
            log.debug(f'Skip Radio: {channel_name}')
            return ''

        m3u_tvg_logo = self.m3u_logopath(data_m3u.get('logo'), args.logopath)
        line = self.m3u_metadata(channel_name, data_m3u, m3u_tvg_logo)

        lines = ''
        streams = sorted(data['streams'],
                         key=lambda x: self.sort_streams(x))

        mirror = 0
        for stream in streams:
            stream_usage = stream['usage']
            if args.only_direct and not stream_usage == 'direct':
                log.debug(f'Skip {stream_usage}: {channel_name}')
                continue
            if args.limit_mirror <= mirror:
                log.debug(f'Skip mirror {mirror}: {channel_name}')
                return ''
            mirror += 1
            stream_attributes = stream.get('attributes')
            stream_direct_data = stream.get('direct_data')
            stream_streamlink_data = stream.get('streamlink_data')

            if stream_usage == 'web':
                log.error(
                    f'Streams with the usage WEB can not be added. {channel_name}')
                continue

            if stream_attributes.get('drm'):
                log.error(
                    f'Streams with DRM protection can not be added. {channel_name}')
                continue

            if (stream_attributes.get('authentication')
                    or stream_attributes.get('subscription')):
                log.info('Added a stream which requires an authentication '
                         f'or a subscription. {channel_name}')

            stream_line = line
            if (not args.name_no_hd and stream_attributes.get('hd')):
                stream_line += ' HD'
            if args.name_netloc:
                url_netloc = self.m3u_name_netloc(stream['url'])
                stream_line += f' | {url_netloc}'
            stream_line += '\n'

            # XXX args.direct_to_streamlink
            if stream_usage == 'direct':
                stream_line += stream['url']
                if stream_direct_data:
                    params = []
                    for k in stream_direct_data.keys():
                        params += [f'{k}={stream_direct_data[k]}']
                    if params:
                        stream_line += '|'
                        stream_line += '|'.join(params)
            elif (stream_usage == 'streamlink'
                  or stream_usage == 'streamlink_301'):

                stream_streamlink_data.update({'url': stream['url']})

                stream_line += (f'http://{args.host}:{args.port}/{stream_usage}'
                                + f'/?{urlencode(stream_streamlink_data)}')

            stream_line += '\n'
            lines += stream_line

        return lines
