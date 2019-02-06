#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from . import common


class Next(common.Common):
    def test_start(self):
        code = textwrap.dedent(
            '''\
            for something in another:
                # more lines
                |cursor|
                stuff = 'thing'

            for more in whatever:
                |start|
                things = 'are'

                here = 'there'

            for last in parts:
                # more text

                # and more

                and_more = False
            '''
        )

        self.compare_next(code)

    def test_middle(self):
        code = textwrap.dedent(
            '''\
            for something in another:
                # more lines
                stuff = 'thing'

            for more in whatever:

                things = 'are'
                |cursor|

                here = 'there'

            for last in parts:
                |start|
                # more text

                # and more

                and_more = False
            '''
        )

        self.compare_next(code)

    def test_end(self):
        code = textwrap.dedent(
            '''\
            for something in another:
                # more lines
                stuff = 'thing'

            for more in whatever:

                things = 'are'

                here = 'there'

            for last in parts:
                |start|
                # more text

                |cursor|
                # and more

                and_more = False
            '''
        )

        self.compare_next(code)

    def test_expand(self):
        code = textwrap.dedent(
            '''\
            while False:
                |start|



                for something in another:
                    # more lines
                    stuff = 'thing'

                for more in whatever:

                    things = 'are'

                    here = 'there'

                for last in parts:
                    # more text

                    |cursor|
                    # and more

                    and_more = False
            '''
        )

        self.compare_next(code)


class NextRange(common.Common):

    '''A series of tests for skipping blocks to select other blocks.'''

    def test_skip_1(self):
        '''Skip the current block and move to the next block, instead.'''
        code = textwrap.dedent(
            '''
            for index, line in enumerate(self._get_reader_handle()):
                asdfasdfsdf = 'asdfsf'

                if clean and not line or all(not item for item in line):
                    |cursor|
                    continue

                |start|if encoding_enabled:
                    line = [item.decode(encoding) for item in line]|end|

                if _found_header:
                    _add_line(line, lines)
                    continue

                if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    _found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue



            if encoding_enabled:
                LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)
            ''')

        self.compare(code, count=2)

    def test_skip_2(self):
        '''Skip the current block and move to the next two blocks, instead.'''
        code = textwrap.dedent(
            '''
            for index, line in enumerate(self._get_reader_handle()):
                asdfasdfsdf = 'asdfsf'

                if clean and not line or all(not item for item in line):
                    |cursor|
                    continue

                if encoding_enabled:
                    line = [item.decode(encoding) for item in line]

                |start|if _found_header:
                    _add_line(line, lines)
                    continue|end|

                if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    _found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue



            if encoding_enabled:
                LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)
            ''')

        self.compare(code, count=3)

    def test_skip_out_of_blocks(self):
        '''Skip the current block and move to the next the last possible block.'''
        code = textwrap.dedent(
            '''
            for index, line in enumerate(self._get_reader_handle()):
                asdfasdfsdf = 'asdfsf'

                if clean and not line or all(not item for item in line):
                    |cursor|
                    continue

                if encoding_enabled:
                    line = [item.decode(encoding) for item in line]

                if _found_header:
                    _add_line(line, lines)
                    continue

                |start|if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    _found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue|end|



            if encoding_enabled:
                LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)
            ''')

        # `count` is just some number greater than the number of blocks
        self.compare(code, count=8)


class Bugs(common.Common):

    '''A series of tests to address bugs that were found in production.'''

    def test_start(self):
        code = textwrap.dedent(
            '''
            for asfdasdf in asfdasfdsfd:
                asdfasdf


                for asdfasdf in asdfsdf:
                    asdfasdf
                    |cursor|asdfasdffsd

                    json.dump([['asdfsfd', 'tttasfsd']], handler) ()

                for asdfasfd in asdfasfsd:
                    |start|
                    asdfassdf
                    asdfasdf

                    asdfsd

                try:
                    # whatever
                    pass
                except Exception:


                    pass

            while False:
                asdfasdf

                # asdfafassdf
                # asdfasdfsdf

                pass
            ''')

        self.compare_next(code)


    def test_middle(self):
        code = textwrap.dedent(
            '''
            for asfdasdf in asfdasfdsfd:
                asdfasdf


                for asdfasdf in asdfsdf:
                    asdfasdf
                    asdfasdffsd

                    json.dump([['asdfsfd', 'tttasfsd']], handler) ()

                for asdfasfd in asdfasfsd:
                    asdfassdf
                    |cursor|
                    asdfasdf

                    asdfsd

                try:
                    |start|
                    # whatever
                    pass
                except Exception:


                    pass

            while False:
                asdfasdf

                # asdfafassdf
                # asdfasdfsdf

                pass
            ''')

        self.compare_next(code)

    def test_end(self):
        code = textwrap.dedent(
            '''
            for asfdasdf in asfdasfdsfd:
                asdfasdf


                for asdfasdf in asdfsdf:
                    asdfasdf
                    asdfasdffsd

                    json.dump([['asdfsfd', 'tttasfsd']], handler) ()

                for asdfasfd in asdfasfsd:
                    asdfassdf
                    asdfasdf

                    asdfsd

                try:
                    # whatever
                    pass
                except Exception:


                    pass

            while False:
                |start|
                asdfasdf
                |cursor|

                # asdfafassdf
                # asdfasdfsdf

                pass
            ''')

        self.compare_next(code)

    def test_expand(self):
        code = textwrap.dedent(
            '''
            for asfdasdf in asfdasfdsfd:
                |start|
                asdfasdf


                for asdfasdf in asdfsdf:
                    asdfasdf
                    asdfasdffsd

                    json.dump([['asdfsfd', 'tttasfsd']], handler) ()

                for asdfasfd in asdfasfsd:
                    asdfassdf
                    asdfasdf

                    asdfsd

                try:
                    # whatever
                    |cursor|
                    pass
                except Exception:


                    pass

            while False:
                asdfasdf

                # asdfafassdf
                # asdfasdfsdf

                pass
            ''')

        self.compare_next(code)

    def test_next(self):
        code = textwrap.dedent(
            '''
            for asfdasdf in asfdasfdsfd:
                asdfasdf
                |cursor|


                for asdfasdf in asdfsdf:
                    asdfasdf
                    asdfasdffsd

                    json.dump([['asdfsfd', 'tttasfsd']], handler) ()

                for asdfasfd in asdfasfsd:
                    asdfassdf
                    asdfasdf

                    asdfsd

                try:
                    # whatever
                    pass
                except Exception:


                    pass

            while False:
                |start|
                asdfasdf

                # asdfafassdf
                # asdfasdfsdf

                pass
            ''')

    def test_out_of_block(self):
        code = textwrap.dedent(
            '''
            def _add_line(line, lines):
                """Add `line` directly into `lines` according to this instance's
                properties."""
                name = line[self.name_column_index]
                address = line[self.address_column_index]
                phone_column_index = line[self.phone_column_index]
                lines.append([name, phone_column_index, address])

            lines = []

            include_header = self.options.get("include_header", False)
            |cursor|clean = self.options.get("clean", True)
            _found_header = False

            encoding = self.options.get("encoding", "utf8")
            encoding_enabled = "encoding" in self.options and sys.version_info < (3, 0)
            if encoding_enabled:
                |start|LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)

            for index, line in enumerate(self._get_reader_handle()):
                if clean and not line or all(not item for item in line):
                    continue

                if encoding_enabled:
                    line = [item.decode(encoding) for item in line]

                if _found_header:
                    _add_line(line, lines)
                    continue

                if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    _found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue

            return lines
        ''')

        self.compare_next(code)

    def test_next_block_with_no_lines(self):
        code = textwrap.dedent(
            '''
            if encoding_enabled:
                |cursor|LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)


            for index, line in enumerate(self._get_reader_handle()):
                |start|if clean and not line or all(not item for item in line):
                    continue

                if encoding_enabled:
                    line = [item.decode(encoding) for item in line]

                if _found_header:
                    _add_line(line, lines)
                    continue

                if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    _found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue
            ''')

        self.compare_next(code)

    def test_expand_with_no_lines(self):
        code = textwrap.dedent(
            '''
            if encoding_enabled:
                LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)


            for index, line in enumerate(self._get_reader_handle()):
                |start|if clean and not line or all(not item for item in line):
                    continue

                if encoding_enabled:
                    line = [item.decode(encoding) for item in line]

                if _found_header:
                    _add_line(line, lines)
                    continue

                if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    |cursor|_found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue
            ''')

        self.compare_next(code)

    def test_case_001(self):
        code = textwrap.dedent(
            '''
            for index, line in enumerate(self._get_reader_handle()):
                |cursor|asdfasdfsdf = 'asdfsf'

                if clean and not line or all(not item for item in line):
                    continue

                if encoding_enabled:
                    line = [item.decode(encoding) for item in line]

                if _found_header:
                    _add_line(line, lines)
                    continue

                if self._is_header(line):
                    LOGGER.debug('Header found on line "%s"', index)
                    _found_header = True

                    if include_header:
                        _add_line(line, lines)

                    continue



            if encoding_enabled:
                |start|LOGGER.info('Reader encoding "%s" will be applied to all lines', encoding)
            ''')

        self.compare_next(code)
