#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''All comment tests, using block_party.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from block_party import config

# IMPORT LOCAL LIBRARIES
from . import common


class Blocks(common.Common):

    '''A class that tests for comments, using block_party.'''

    @classmethod
    def setUpClass(cls):
        '''Change the user's settings to include comments.'''
        super(Blocks, cls).setUpClass()
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: False)

    def test_single_empty(self):
        '''Get a single comment line, even if it is empty.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|#
            while True:
                thing = 8

                |cursor|
                if another:
                    pass|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)

    def test_single(self):
        '''Get a single comment line.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|#asdfasdfasdf asdf a ft =as dfas dsdf
            while True:
                thing = 8

                |cursor|
                if another:
                    pass|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)

    def test_multi_001(self):
        '''Get a block of comment lines.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|# tt ka la l;fj al;
            # asdfasdf
            while True:
                thing = 8

                |cursor|
                if another:
                    pass|end|

            # asdfasdf

            whatever = "asdfsaf"
            '''
        )

        self.compare(code, two_way=True)

    def test_multi_002(self):
        '''Get a block of comment lines.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|# tt ka la l;fj al;
            # asdfasdf
            #
            while True:
                thing = 8

                |cursor|
                if another:
                    pass|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)
