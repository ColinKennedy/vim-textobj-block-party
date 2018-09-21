#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from .block_party import party


def _get_buffer_context(search=True, two_way=False, customize=True):
    code = '\n'.join(vim.current.window.buffer)
    row, column = vim.current.window.cursor
    row -= 1  # Get the current row, as a 0-based value

    boundary = party.get_boundary(code, row, column, search=search, two_way=two_way, customize=customize)

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


def around_deep(key, search=True):
    boundary = _get_buffer_context(search=search, two_way=True)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def inside_deep(key, search=True):
    boundary = _get_buffer_context(search=search)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def around_shallow(key, search=True):
    boundary = _get_buffer_context(search=search, two_way=True, customize=False)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def inside_shallow(key, search=True):
    boundary = _get_buffer_context(search=search, customize=False)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))
