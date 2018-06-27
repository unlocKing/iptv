# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


def comma_list(values, split_at=None):
    '''
    converts a comma-separated list into a valid list for python
    :param values: (string) comma-separated list
    '''
    if not split_at:
        split_at = ','
    if isinstance(values, list):
        return values
    elif isinstance(values, str):
        return [val.strip() for val in values.split(split_at)]
    else:
        raise TypeError(
            'values type is "{0}"", only "list" or "str" is allowed.'.format(
                type(values).__name__))


def comma_list_filter(acceptable, split_at=None):
    '''
    creates a function that will only allow strings from 'acceptable'
    :param acceptable: (list) allowed strings
    '''
    if not split_at:
        split_at = ','

    def func(p):
        values = comma_list(p, split_at)
        return list(filter(lambda v: v in acceptable, values))

    return func


def comma_list_filter_remove(not_acceptable, split_at=None):
    '''
    creates a function that will not allow any strings from 'not_acceptable'
    :param not_acceptable: (list) not allowed strings
    '''
    if not split_at:
        split_at = ','

    def func(p):
        values = comma_list(p, split_at)
        return list(filter(lambda v: v not in not_acceptable, values))

    return func


__all__ = [
    'comma_list',
    'comma_list_filter',
    'comma_list_filter_remove',
]
