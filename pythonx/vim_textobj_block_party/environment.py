#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module that sets up the user's Vim with block_party environment variables.'''

# IMPORT STANDARD LIBRARIES
import functools

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from .block_party import config


def _include_comment(block):
    '''If the given block has comments enabled for it.

    Args:
        block (str): The name of the block to check.

    Returns:
        bool: If comments are allowed.

    '''
    try:
        return bool(int(vim.eval('g:vim_block_party_{block}include_comments'.format(block=block))))
    except Exception:
        return True


def _include_whitespace(block):
    '''If the given block has whitespace enabled for it.

    Args:
        block (str): The name of the block to check.

    Returns:
        bool: If whitespace are allowed.

    '''
    try:
        return bool(int(vim.eval('g:vim_block_party_{block}include_whitespace'.format(block=block))))
    except Exception:
        return True


def _include_search(block):
    '''If the given block has search enabled for it.

    Args:
        block (str): The name of the block to check.

    Returns:
        bool: If search are allowed.

    '''
    try:
        return bool(int(vim.eval('g:vim_block_party_{block}search'.format(block=block))))
    except Exception:
        return False


def init():
    '''Create all of the configuration settings for Vim.

    This function is what enables all of the global variables that Vim uses.

    '''
    registry = {
        'comment': _include_comment,
        'search': _include_search,
        'whitespace': _include_whitespace,
    }

    blocks = (
        'for',
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
