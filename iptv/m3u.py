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
        return ' {0}="{1}"'.format(item, value)

    def m3u_logopath(self, logo, logopath):
        if not logo:
            return
        elif logopath and not logo.startswith(('http://', 'https://')):
            logo = urljoin(logopath, logo)

        if logo.startswith(('http://', 'https://')):
            return logo

    def m3u_name_netloc(self, url):
        '''
        removes subdomains from an URL

        :param url: URL
        '''
        _url_netloc = urlparse(url).netloc.split('.')
        url_netloc = '{0}.{1}'.format(_url_netloc[-2],
                                      _url_netloc[-1])
        if (len(url_netloc) <= 6
                and len(_url_netloc) >= 3
                and _url_netloc[-3] != 'www'):
            url_netloc = '{0}.{1}'.format(_url_netloc[-3],
                                          url_netloc)
        return url_netloc

    def _generate(self, data, args):
        data_m3u = data.get('m3u')

        if args.clean_metadata:
            log.debug('Removed M3U metadata.')
            data_m3u = {}

        m3u_group_title = data_m3u.get('group')
        m3u_radio = data_m3u.get('radio')
        m3u_tvg_id = data_m3u.get('id')
        m3u_tvg_logo = self.m3u_logopath(data_m3u.get('logo'), args.logopath)
        m3u_tvg_name = data_m3u.get('name')
        m3u_tvg_shift = data_m3u.get('shift')
        m3u_tvg_chno = data_m3u.get('chno')

        if m3u_radio and args.remove_radio:
            log.debug('Skip Radio: {0}'.format(data['name']))
            return ''

        line = '#EXTINF:-1{tvg_id}{tvg_name}{tvg_chno}{tvg_shift}{group_title}{radio}{tvg_logo},{name}'.format(
            group_title=self.m3u_item('group-title', m3u_group_title),
            name=data['name'],
            radio=self.m3u_item('radio', 'true') if m3u_radio else '',
            tvg_chno=self.m3u_item('tvg-chno', m3u_tvg_chno),
            tvg_id=self.m3u_item('tvg-id', m3u_tvg_id),
            tvg_logo=self.m3u_item('tvg-logo', m3u_tvg_logo),
            tvg_name=self.m3u_item('tvg-name', m3u_tvg_name),
            tvg_shift=self.m3u_item('tvg-shift', m3u_tvg_shift),
        )

        lines = ''
        streams = sorted(data['streams'],
                         key=lambda x: self.sort_streams(x))

        mirror = 0
        for stream in streams:
            if args.limit_mirror <= mirror:
                log.debug('Skip mirror {0}: {1}'.format(mirror, data['name']))
                return ''
            mirror += 1
            stream_attributes = stream.get('attributes')
            stream_direct_data = stream.get('direct_data')
            stream_streamlink_data = stream.get('streamlink_data')

            if stream['usage'] == 'web':
                log.error('Streams with the usage WEB can not be added. {0}'.format(data['name']))
                continue

            if stream_attributes.get('drm'):
                log.error('Streams with DRM protection can not be added. {0}'.format(data['name']))
                continue

            if (stream_attributes.get('authentication')
                    or stream_attributes.get('subscription')):
                log.info('Added a stream which requires '
                         'a authentication or a subscription. {0}'.format(data['name']))

            stream_line = line
            if (not args.name_no_hd and stream_attributes.get('hd')):
                stream_line += ' HD'
            if args.name_netloc:
                url_netloc = self.m3u_name_netloc(stream['url'])
                stream_line += ' | {0}'.format(url_netloc)
            stream_line += '\n'

            # XXX args.direct_to_streamlink
            if stream['usage'] == 'direct':
                stream_line += stream['url']
                if stream_direct_data:
                    params = []
                    for k in stream_direct_data.keys():
                        params += ['{0}={1}'.format(k, stream_direct_data[k])]
                    if params:
                        stream_line += '|'
                        stream_line += '|'.join(params)
            elif (stream['usage'] == 'streamlink'
                  or stream['usage'] == 'streamlink_301'):

                stream_streamlink_data.update({'url': stream['url']})

                stream_line += 'http://{host}:{port}/{usage}/?{data}'.format(
                    host=args.host,
                    port=args.port,
                    usage=stream['usage'],
                    data=urlencode(stream_streamlink_data),
                )

            stream_line += '\n'
            lines += stream_line

        return lines
