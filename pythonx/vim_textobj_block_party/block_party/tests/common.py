#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A base class for the Blocks-related unittest classes.'''

# IMPORT STANDARD LIBRARIES
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from block_party import party


class Common(unittest.TestCase):

    '''The main class which will be used for testing.'''

    cursor = '|cursor|'
    end = '|end|'
    start = '|start|'

    @staticmethod
    def _filter_marker(lines, marker):
        '''Find a cursor marker in the given Python source-code lines.

        Args:
            lines (list[str]): The source-code to search for `marker`.
            marker (str): The marker to search for.

        Returns:
            tuple[list[str], tuple[int, int]]:

        '''
        cursor_row = -1
        cursor_column = -1
        output_lines = []

        for row, line in enumerate(lines):
            if cursor_row == -1 or cursor_column == -1:
                try:
                    cursor_column = line.index(marker)
                    line = line.replace(marker, '')
                    cursor_row = row
                except ValueError:
                    pass

            output_lines.append(line)

        return (output_lines, (cursor_row, cursor_column))

    def compare(self, code, extra_lines=False, two_way=False, search=False):
        '''Check if the code's start, end, and cursor positions are correct.

        Args:
            code (str):
                Some Python code to parse. The text should contain
                "|start|", "|end|", and "|cursor|" somewhere within it.
            extra_lines (`bool`, optional):
                If True, do a second search after the 1st search completes which
                looks for newlines. If False, only do a single search.
                Default is False.
            two_way (`bool`, optional):
                If True and `extra_lines` is also True, search for newlines
                both before and after the found block.
                If False, only search above the found block.
                Default is False.
            search (`bool`, optional):
                If True, search for source-code mentioned in the block.
                If False, do not. Default is False.

        Raises:
            RuntimeError: If no cursor could be found.
            AssertionError: If the test fails.

        '''
        lines = code.split('\n')

        (lines, boundary_start) = self._filter_marker(lines, self.start)
        (lines, boundary_end) = self._filter_marker(lines, self.end)
        (lines, (cursor_row, cursor_column)) = self._filter_marker(lines, self.cursor)

        if cursor_row == -1 or cursor_column == -1:
            raise RuntimeError('Cursor could not be found.')

        code = '\n'.join(lines)

        (start, end) = party.get_boundary(
            code,
            cursor_row,
            cursor_column,
            extra_lines=extra_lines,
            search=search,
            two_way=two_way,
        )

        self.assertEqual(start, boundary_start[0])
        self.assertEqual(end, boundary_end[0])
