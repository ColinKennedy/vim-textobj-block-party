#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''All of the main functions that Vim uses to find Python code blocks.'''

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from .block_party import party
from . import columnwise


def _get_buffer_context(
        extra_lines=False,
        search=True,
        two_way=False,
        customize=True,
        cursor=None,
        include_column=False,
):
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
        include_column (int, optional):
            If True then the exact column number of the first non-whitespace
            character is returned. Otherwise, just return 0. Default is False.

    Returns:
        list[list[int, int, int, int]]:
            The rows of the start and end of the boundary. These values are used
            directly by Vim to create a text object and should not be messed with.

    '''
    lines = vim.current.window.buffer
    code = '\n'.join(lines)

    if not code.endswith('\n'):
        # Forcibly add a newline if there isn't one so that the last block
        # doesn't edit at the wrong boundary
        #
        # Reference: https://github.com/ColinKennedy/vim-textobj-block-party/issues/3
        #
        code += '\n'

    if cursor:
        row, column = cursor
    else:
        row, column = vim.current.window.cursor
        row -= 1  # Get the current row, as a 0-based value

    previous_lines = reversed(lines[:row])
    column = max(column, len(columnwise.find_best_indent(previous_lines)))

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

    if not include_column:
        column = 0
    else:
        column += 1

    return [
        [
            0,
            boundary[0] + 1,
            column,
            0,
        ],
        [
            1,
            boundary[1] + 1,
            column,
            0,
        ],
    ]


def get_next_block():
    '''tuple[int, int]: Find row and column of the next block of Python code.'''
    row, column = vim.current.window.cursor
    lines = vim.current.window.buffer
    code = '\n'.join(lines)

    next_row = party.get_next_block(code, row, column)
    next_row += 1  # This moves to cursor directly the next block

    previous_lines = reversed(lines[:next_row])
    next_column = max(column, len(columnwise.find_best_indent(previous_lines)))

    return (next_row, next_column)


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


def inside_shallow(key, search=True, cursor=None, count=1, include_column=False):
    '''Search for a boundary before the block.

    Args:
        key (str):
            The temporary Vim variable that will be used to export our boundary.
        search (`bool`, optional):
            If True, allow the user to search for code related to the block (if the setting is enabled).
            If False, do not affect any source-lines outside of the current block.
            Default is True.
        count (int, optional):
            The number of blocks ahead to search for. A value of 1 will get the
            next block. 0 gets the current block. Default: 1.
        include_column (int, optional):
            If True then the exact column number of the first non-whitespace
            character is returned. Otherwise, just return 0. Default is False.

    '''
    if count < 0:
        raise ValueError('Count cannot be less than zero.')

    latest_boundary = []

    for _ in range(count):
        boundary = _get_buffer_context(
            search=search,
            customize=False,
            cursor=cursor,
            include_column=include_column,
        )

        if boundary:
            latest_boundary = boundary
            cursor = (boundary[0][1], boundary[0][2])
            break

    vim.command('let {key} = {latest_boundary}'.format(
        key=key, latest_boundary=latest_boundary))
