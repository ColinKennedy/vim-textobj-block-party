#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A collection of settings which are used to customize block_party's behavior.'''

# IMPORT STANDARD LIBRARIES
import copy


COMMENT_KEY = 'comment'
GREEDY_KEY = 'greedy'
SEARCH_KEY = 'search'
WHITESPACE_KEY = 'whitespace'

_ALL_BLOCK = '_all'

SETTINGS = {
    COMMENT_KEY: dict(),
    GREEDY_KEY: dict(),
    SEARCH_KEY: dict(),
    WHITESPACE_KEY: dict(),
}

_DEFAULT_SETTINGS = copy.deepcopy(SETTINGS)


def _get_setting(key, block=_ALL_BLOCK):
    '''Get the setting for the given key and block.

    Note:
        If the given `block` has no configuration setting, this function will
        fall back onto the default "all" block for a value.

    Args:
        key (str):
            The setting to search for. For example, it could be "comment" to search
            for the configuration settings for comments, specifically.
        block (`str`, optional):
            The name of block type to search for `key`. For example, this could "while".
            If no block is given, the "all" is searched, instead.

    Returns:
        bool: The found setting for `key`.

    '''
    try:
        functions = SETTINGS[key][block]
    except KeyError:
        functions = []

    for function in functions:
        try:
            return function()
        except Exception:  # pylint: disable=broad-except
            pass

    if block == _ALL_BLOCK:
        return False

    return _get_setting(key, block=_ALL_BLOCK)


def allow_comment(block=_ALL_BLOCK):
    '''Get the comment setting for the given block.

    Note:
        If the given `block` has no configuration setting, this function will
        fall back onto the default "all" block for a value.

    Args:
        block (`str`, optional):
            The name of block type to search for. For example, this could "while".
            If no block is given, the "all" is used, instead.

    Returns:
        bool: The found setting for comments.

    '''
    return _get_setting(COMMENT_KEY, block=block)


def allow_greedy(block=_ALL_BLOCK):
    '''Check if the user wants to consider text inside a Python block as "source-code".

    Note:
        If the given `block` has no configuration setting, this function will
        fall back onto the default "all" block for a value.

    Args:
        block (`str`, optional):
            The name of block type to search for. For example, this could "while".
            If no block is given, the "all" is used, instead.

    Returns:
        bool: The found setting for searches.

    '''
    return _get_setting(GREEDY_KEY, block=block)


def allow_search(block=_ALL_BLOCK):
    '''Get the search setting for the given block.

    Note:
        If the given `block` has no configuration setting, this function will
        fall back onto the default "all" block for a value.

    Args:
        block (`str`, optional):
            The name of block type to search for. For example, this could "while".
            If no block is given, the "all" is used, instead.

    Returns:
        bool: The found setting for searches.

    '''
    return _get_setting(SEARCH_KEY, block=block)


def allow_whitespace(block=_ALL_BLOCK):
    '''Get the whitespace setting for the given block.

    Note:
        If the given `block` has no configuration setting, this function will
        fall back onto the default "all" block for a value.

    Args:
        block (`str`, optional):
            The name of block type to search for. For example, this could "while".
            If no block is given, the "all" is used, instead.

    Returns:
        bool: The found setting for whitespaces.

    '''
    return _get_setting(WHITESPACE_KEY, block=block)


def register_setting(key, function, override=False, block=_ALL_BLOCK):
    '''Add the given configuration function for a block type.

    Args:
        key (str):
            The setting to search for. For example, it could be "comment" to search
            for the configuration settings for comments, specifically.
        function (callable -> bool):
            A function that, when evaluated, gives a True/False value.
        override (`bool`, optional):
            If True, remove all existing configuration settings for `key` and `block`.
            If False, add the given `function` with priority into the possible options.
            Default is False.
        block (`str`, optional):
            The name of block type to search for `key`. For example, this could "while".
            If no block is given, the "all" is searched, instead.

    '''
    SETTINGS.setdefault(key, dict())
    SETTINGS[key].setdefault(block, [])

    if not override:
        SETTINGS[key][block].insert(0, function)
    else:
        SETTINGS[key][block] = [function]


def reset():
    '''Remove all user settings and restore "default" configuration settings.'''
    global SETTINGS  # pylint: disable=global-statement

    SETTINGS = _DEFAULT_SETTINGS
