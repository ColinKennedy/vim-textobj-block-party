#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from .block_party import config


def _include_comments(block):
    try:
        return bool(int(vim.eval('g:vim_block_party_{block}include_comments'.format(block=block))))
    except Exception:
        return False


def _include_whitespace(block):
    try:
        return bool(int(vim.eval('g:vim_block_party_{block}include_whitespace'.format(block=block))))
    except Exception:
        return False


def _include_search(block):
    try:
        return bool(int(vim.eval('g:vim_block_party_{block}search'.format(block=block))))
    except Exception:
        return False


def init():
    registry = {
        'comments': _include_comments,
        'search': _include_search,
        'whitespace': _include_whitespace,
    }

    blocks = (
        'for'
        'if',
        'try',
        'while',
    )

    for key, base_function in registry.items():
        # Create the master environment config variable
        config.register_setting(key, functools.partial(base_function, ''))

        # And now the same mapping for each block
        for block in blocks:
            function = functools.partial(base_function, block + '_')
            config.register_setting(key, function, block=block)
