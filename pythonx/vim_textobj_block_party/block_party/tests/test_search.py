#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Any test that is related to inspecting Python source-code.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from block_party import config

# IMPORT LOCAL LIBRARIES
from . import common


class Blocks(common.Common):

    '''A series of tests for finding lines that are related to the current block.'''

    def setUp(self):
        '''Reset the user's config before every test.'''
        super(Blocks, self).setUp()
        config.reset()

    def test_search_off(self):
        '''Run a test without searching.'''
        code = textwrap.dedent(
            '''\
            items = [x for x in whatever]
            |start|for index in items:

                print('running')

                # foobar

                |cursor|
                print('index {}'.format(index))|end|

            last = 'bit is here'
            '''
        )

        self.compare(code)

    def test_search_whitespace(self):
        '''Run a test with searching and whitespace allowed.'''
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\
            items = [x for x in whatever]
            |start|

            for index in items:

                print('running')

                # foobar

                |cursor|
                print('index {}'.format(index))|end|

            last = 'bit is here'
            '''
        )

        self.compare(code, search=True)
