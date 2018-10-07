#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''All of the main functions that Vim uses to find Python code blocks.'''

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from .block_party import party
from . import columnwise


def _get_buffer_context(extra_lines=False, search=True, two_way=False, customize=True):
    '''Get the user's buffer and cursor and return a boundary.

    Args:
        extra_lines (`bool`, optional):
            If True, after a match is found, add any neighboring newlines to the boundary.
            If False, leave the boundary alone.
            This is useful if you want to delete whitespace around a block.
            Default is False.
        search (`bool`, optional):
            If True, allow the user to search for code related to the block (if the setting is enabled).
            If False, do not affect any source-lines outside of the current block.
            Default is True.
        two_way (`bool`, optional):
            If True, search for newlines, comments, and source-lines below the current block.
            If False, only search above the current block, if at all.
            Default is False.
        customize (`bool`, optional):
            If True, the user's environment preferences will affect the returned boundary.
            If False, the boundary will disable all forms of searching (whitespace, comments, etc.)
            Default is True.

    Returns:
        list[list[int, int, int, int]]:
            The rows of the start and end of the boundary. These values are used
            directly by Vim to create a text object and should not be messed with.

    '''
    lines = vim.current.window.buffer
    code = '\n'.join(lines)
    row, column = vim.current.window.cursor
    row -= 1  # Get the current row, as a 0-based value

    previous_lines = reversed(lines[:row])
    column = max(column, columnwise.find_best_column(previous_lines))

    boundary = party.get_boundary(
        code,
        row,
        column,
        extra_lines=extra_lines,
        search=search,
        two_way=two_way,
        customize=customize,
    )

    boundary_was_not_found = boundary == (-1, -1)
    if boundary_was_not_found:
        return []

    return [
        [
            0,
            boundary[0] + 1,
            0,
            0,
        ],
        [
            1,
            boundary[1] + 1,
            0,
            0,
        ],
    ]


def around_deep(key, search=True, two_way=False):
    '''Search for a boundary using the user's configuration before and after the block.

    Args:
        key (str):
            The temporary Vim variable that will be used to export our boundary.
        search (`bool`, optional):
            If True, allow the user to search for code related to the block (if the setting is enabled).
            If False, do not affect any source-lines outside of the current block.
            Default is True.
        two_way (`bool`, optional):
            If True, search for whitespaces/comments/etc before and after the block.
            If False, only search up.
            Default is False.

    '''
    boundary = _get_buffer_context(extra_lines=True, search=search, two_way=two_way)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def inside_deep(key, search=True):
    '''Search for a boundary using the user's configuration before the block.

    Args:
        key (str):
            The temporary Vim variable that will be used to export our boundary.
        search (`bool`, optional):
            If True, allow the user to search for code related to the block (if the setting is enabled).
            If False, do not affect any source-lines outside of the current block.
            Default is True.

    '''
    boundary = _get_buffer_context(search=search)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def around_shallow(key, search=True, two_way=False):
    '''Search for a boundary before and after the block.

    Args:
        key (str):
            The temporary Vim variable that will be used to export our boundary.
        search (`bool`, optional):
            If True, allow the user to search for code related to the block (if the setting is enabled).
            If False, do not affect any source-lines outside of the current block.
            Default is True.
        two_way (`bool`, optional):
            If True, search for whitespaces/comments/etc before and after the block.
            If False, only search up.
            Default is False.

    '''
    boundary = _get_buffer_context(extra_lines=True, search=search, two_way=two_way, customize=False)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def inside_shallow(key, search=True):
    '''Search for a boundary before the block.

    Args:
        key (str):
            The temporary Vim variable that will be used to export our boundary.
        search (`bool`, optional):
            If True, allow the user to search for code related to the block (if the setting is enabled).
            If False, do not affect any source-lines outside of the current block.
            Default is True.

    '''
    boundary = _get_buffer_context(search=search, customize=False)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))
