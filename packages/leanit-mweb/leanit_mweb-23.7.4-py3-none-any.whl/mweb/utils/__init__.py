from __future__ import annotations

import logging

from starlette.requests import Request

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    pass

def camelCaseToSnakeCase(name):
    return ''.join(['_'+i.lower() if i.isupper() else i for i in name]).lstrip('_')

def flatten(data: tuple, delimiter: str = ',') -> str:
    """
    Convert a tuple of pairs to a delimited list.

    :param data: A tuple of pairs.
    :type data: tuple
    :param delimiter: The delimiter used to join the output list. Defaults to ','.
    :type delimiter: str
    :return: A delimited list of strings, where each element of the input tuple is represented by two elements in the output list.
    :rtype: str
    """
    flattened_data = [str(item) for sublist in data for item in sublist]
    result = delimiter.join(flattened_data)
    return result

def merge_dict(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dict(value, node)
        elif isinstance(value, list):
            # get node or create one
            node = destination.setdefault(key, [])
            for item in value:
                if item not in node:
                    node.append(item)
        else:
            destination[key] = value

    return destination

def remote_ip(request: Request):
    """
    Return the remote ip address of the request depending on the ip_mode config.
    """
    from mweb import config
    ip_mode = config.get("mweb", {}).get("ip_mode", "remote_addr")

    if ip_mode == "remote_addr":
        return request.client.host
    elif ip_mode == "x_forwarded_for":
        return request.headers.get("x-forwarded-for", request.client.host)
    elif ip_mode == "cloudflare":
        return request.headers.get("cf-connecting-ip", request.client.host)
    else:
        raise NotImplementedError(f"Unknown ip_mode: {ip_mode}")


def unflatten(data: str, delimiter: str = ',') -> tuple:
    """
    Convert a delimited list to a tuple of pairs.

    :param data: A delimited list of strings.
    :type data: str
    :param delimiter: The delimiter used to split the input string. Defaults to ','.
    :type delimiter: str
    :return: A tuple of pairs, where each pair contains two elements from the input list.
    :rtype: tuple
    """
    split_data = data.split(delimiter)
    result = tuple((split_data[i], split_data[i+1]) for i in range(0, len(split_data), 2))
    return result


def unnest_query_params(input_dict: Dict[str, str]) -> Dict:
    """
    Convert a dictionary of query parameters with nested keys to a dictionary with a single level of keys.

    :param input_dict: {'filter[tenant]': 'all', 'filter[foo]': 'bar'}
    :return: {'filter': {'tenant': 'all', 'foo': 'bar'}}
    """
    output_dict = {}
    for key, value in input_dict.items():
        if '[' in key and ']' in key:
            outer_key, inner_key = key.split('[')
            inner_key = inner_key.rstrip(']')
            if outer_key not in output_dict:
                output_dict[outer_key] = {}
            output_dict[outer_key][inner_key] = value
    return output_dict

