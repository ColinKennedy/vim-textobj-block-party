#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from .block_party import party


def _get_buffer_context(scan=False, settings=False):
    code = '\n'.join(vim.current.window.buffer)
    row, column = vim.current.window.cursor
    row -= 1  # Get the current row, as a 0-based value

    boundary = party.get_boundary(code, row, column, scan=scan, settings=settings)

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


def around_deep(key):
    boundary = _get_buffer_context(scan=True, settings=True)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def inside_deep(key):
    boundary = _get_buffer_context(settings=True)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def around_shallow(key):
    boundary = _get_buffer_context(scan=True)
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))


def inside_shallow(key):
    boundary = _get_buffer_context()
    vim.command('let {key} = {boundary}'.format(key=key, boundary=boundary))
