#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module for any bugs that were found while using block_party.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from block_party import config

# IMPORT LOCAL LIBRARIES
from . import common


class TooManyLines(common.Common):

    '''A series of tests for any time block_party grabbed more lines than expected.'''

    def setUp(self):
        '''Reset the stored settings before each test runs.'''
        super(TooManyLines, self).setUp()
        config.reset()

    def test_case_001(self):
        '''Test that block_party does not grab the entire Python function.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\
            def main():
                import argparse

                asdfadsf

                while True:
                    foobar = 8
                    # more docs

                    |start|# asdfasdfasdf
                    # asdfasdfdfsdfsdfa as asf dsd f  fd
                    items = 'asdfsd'



                    for asdfsdf in items:

                        # whatever,
                        asdfsa

                        |cursor|

                        if True:
                            # pasdfasfd

                            pass
                            # asdfafd
                        elif ting:
                            pass
                    else:
                        thing|end|

                    # asdfadsffdasd
                    # asdfsdfkk,w
                    more = 'asdf'

                argparse.ArgumentParser()
            '''
        )

        self.compare(code, search=True)

    def test_case_002(self):
        '''Test that block_party does not grab the entire Python function.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: True)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\
            def main():
                import argparse

                tttttt.asdfasdsdf(yyyyyyy)
                |start|whatever = 8

                while True:
                    whatever = 'asdfsfd'



                    # info here
                    # another bit
                    |cursor|items = 'asdfsd'
                    aaaaa = 'tt'

                    for foo in items:

                        # whatever,
                        asdfsa

                        if True:
                            # pasdfasfd

                            pass
                            # asdfafd
                        elif ting:
                            pass

                        # asdfasdf

                    else:
                        thing


                    # asdfadsffdasd
                    # asdfsdfkk,w
                    more = 'asdf'

                |end|
                #asdfasdf
                argparse.ArgumentParser()
            '''
        )

        self.compare(code, two_way=True, search=True)

    def test_case_003(self):
        '''Test that block_party does not grab the entire Python function.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\
            def main():
                import argparse

                tttttt.asdfasdsdf(yyyyyyy)
                whatever = 8

                while True:
                    whatever = 'asdfsfd'



                    # info here
                    # another bit
                    items = 'asdfsd'
                    aaaaa = 'tt'
                    |start|


                    for foo in items:

                        # whatever,
                        |cursor|asdfsa

                        if True:
                            # pasdfasfd

                            pass
                            # asdfafd
                        elif ting:
                            pass

                        # asdfasdf

                    else:
                        thing

                    |end|
                    # asdfadsffdasd
                    # asdfsdfkk,w
                    more = 'asdf'

                #asdfasdf
                argparse.ArgumentParser()
            '''
        )

        self.compare(code, two_way=True, search=True)

    def test_case_004(self):
        '''Test that block_party does not grab the entire Python function.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\
            def main():
                import argparse

                tttttt.asdfasdsdf(yyyyyyy)
                |start|whatever = 8


                while True:
                    whatever = 'asdfsfd'



                    # info here
                    # another bit
                    items = 'asdfsd'
                    |cursor|aaaaa = 'tt'


                    for foo in items:

                        # whatever,
                        asdfsa

                        if True:
                            # pasdfasfd

                            pass
                            # asdfafd
                        elif ting:
                            pass

                        # asdfasdf

                    else:
                        thing


                    # asdfadsffdasd
                    # asdfsdfkk,w
                    more = 'asdf'

                |end|
                #asdfasdf
                argparse.ArgumentParser()
            '''
        )

        self.compare(code, extra_lines=True, two_way=True, search=True)

    def test_if_python_node(self):
        '''Test so that callable objects in Python still "find" identifiers correctly.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: False)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\
            stuff = 10


            |start|# asdfasdf
            #asdfsdf
            #
            another = 8

            if hasattr(another, 'foo'):
                pass
            else:
                |cursor|
                thing = 0
                print('asdfsd')

            |end|
            more_items = True
            '''
        )

        self.compare(code, extra_lines=False, two_way=True, search=True)


class BadLines(common.Common):
    def test_no_source_or_previous_node(self):
        '''Find source-code which is defined within the Python block.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: True)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            |start|# some comment
            # more
            #

            for item in another:
                whatever = item
                |cursor|
                # more lines

                print('still going')
            |end|
            lastly = 'done'
            '''
        )

        self.compare(code, two_way=True, extra_lines=False, search=True)

    def test_previous_node(self):
        '''Find source-code which is defined within the Python block.'''
        config.register_setting(config.WHITESPACE_KEY, lambda: False)

        code = textwrap.dedent(
            '''\

            |start|if False:

                pass
                |cursor|
                # 'asdfasfdasdf'
            else:
                print('asfasdf')|end|

            '''
        )

        self.compare(code, search=False)
