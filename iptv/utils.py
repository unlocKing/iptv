# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def comma_list(values):
    return [val.strip() for val in values.split(',')]


__all__ = [
    'comma_list',
]
