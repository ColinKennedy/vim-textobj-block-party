#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import re


_LINE_ENDER = re.compile(r'(?P<prefix>\s*).+(?::)(?:#.+)?$')


def _get_indent(text):
    '''str: Find the indentation of a line of text.'''
    return text[:len(text) - len(text.lstrip())]


def _add_indent(text, indent=1):
    '''Add another set of indentation to `text`.'''
    if '\t' in text:
        return text + ('\t' * indent)

    # TODO : Get indent number from Vim settings. Not just `'    '`
    return text + ('    ' * indent)


def find_best_column(lines):
    '''Find the next line's indentation.

    If the next line is the start of Python block then the indentation is
    "current indentation plus one more level of indent" so that value will be
    returned instead.

    Args:
        lines (iter[str]): Some lines of Python source code.

    Returns:
        str: The found indentation, if any.

    '''
    for line in lines:
        line = line.strip()

        if not line:
            continue

        indent = _get_indent(line)

        needs_more_indentation = _LINE_ENDER.match(line)
        if needs_more_indentation:
            return _add_indent(indent)

        return indent

    return ''
