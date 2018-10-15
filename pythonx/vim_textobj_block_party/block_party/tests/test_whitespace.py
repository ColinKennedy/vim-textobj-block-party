#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Any test related to whitespace during the initial search for code in block_party.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from block_party import config

# IMPORT LOCAL LIBRARIES
from . import common


class BlockWhitespace(common.Common):

    '''All whitespace-related tests.'''

    @classmethod
    def setUpClass(cls):
        '''Allow whitespace during the initial search.'''
        super(BlockWhitespace, cls).setUpClass()
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

    def test_inline(self):
        '''Search for whitespace unsuccessfully because the block has no surrounding whitespace.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8
            |start|while True:
                thing = 8

                |cursor|
                if another:
                    pass|end|
            whatever = "asdfsaf"
            '''
        )

        self.compare(code, two_way=True)

    def test_single_empty(self):
        '''Find a single newline before and after the block.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8
            |start|
            while True:
                thing = 8

                |cursor|
                if another:
                    pass
            |end|
            whatever = "asdfsaf"
            '''
        )

        self.compare(code, two_way=True)

    def test_newlines(self):
        '''Find newlines before and after the block.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8
            |start|

            while True:
                thing = 8

                |cursor|
                if another:
                    pass

            |end|
            whatever = "asdfsaf"
            '''
        )

        self.compare(code, two_way=True)

    def test_multi(self):
        '''Find many newlines around the block.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8
            |start|


            while True:
                thing = 8

                |cursor|
                if another:
                    pass


            |end|
            whatever = "asdfsaf"
            '''
        )

        self.compare(code, two_way=True)
