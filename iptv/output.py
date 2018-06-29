# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def write_data(filename, data):
    log.info(f'Write data to {filename}')
    with open(filename, 'w', encoding='utf8') as f:
        f.write(data)
    f.close()
    log.info('--- END ---')


__all__ = [
    'write_data',
]
