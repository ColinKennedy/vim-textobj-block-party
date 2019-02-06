#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Test to make sure that user configuration settings work as-expected.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from block_party import config

# IMPORT LOCAL LIBRARIES
from . import common


class General(common.Common):

    '''A TestCase which makes sure that config options "mix" well together.'''

    def setUp(self):
        '''Reset the configuration to some reasonable default settings.'''
        super(General, self).setUp()
        config.reset()

    def tearDown(self):
        '''Reset the user's config after every test.'''
        super(General, self).tearDown()
        config.reset()

    def test_strict_search_001(self):
        '''Find source-code which is only defined at the block's definition.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: False)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            whatever = 'asdfafsd'

            |start|# some comment
            # more
            #

            another = ['asdf', 'ttt']

            for item in another:
                whatever = item

                # more lines|cursor|

                print('still going')
            |end|
            lastly = 'done'
            '''
        )

        self.compare(code, two_way=True, extra_lines=False, search=True)

    def test_strict_search_001b(self):
        '''Find source-code which is only defined at the block's definition.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: False)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            whatever = 'asdfafsd'

            |start|# some comment
            # more
            #

            another = ['asdf', 'ttt']

            for index, item in enumerate(another):
                whatever = item

                # more lines|cursor|

                print('still going')
            |end|
            lastly = 'done'
            '''
        )

        self.compare(code, two_way=True, extra_lines=False, search=True)

    def test_strict_search_002(self):
        '''Find source-code which is only defined at the block's definition.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: False)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            whatever = 'asdfafsd'

            # some comment
            # more
            #
            another = 'asdf'
            |start|


            try:
                pass
            except ValueError:
                another = 'ttt'
                pass|cursor|
            else:
                pass
            |end|
            lastly = 'done'
            '''
        )

        self.compare(code, two_way=True, extra_lines=False, search=True)

    def test_strict_search_002b(self):
        '''Find source-code which is only defined at the block's definition.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: False)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            whatever = 'asdfafsd'

            # some comment
            # more
            #
            another = 'asdf'
            |start|

            my_exceptions_list = (ValueError, TypeError)

            try:
                pass
            except my_exceptions_list:
                another = 'ttt'
                pass|cursor|
            else:
                pass
            |end|
            lastly = 'done'
            '''
        )

        self.compare(code, two_way=True, extra_lines=False, search=True)

    def test_strict_search_003(self):
        '''Find source-code which is only defined at the block's definition.'''
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.GREEDY_KEY, lambda: False)
        config.register_setting(config.SEARCH_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            whatever = 'asdfafsd'

            |start|# some comment
            # more
            #

            another = ['asdf', 'ttt']


            if False:
                |cursor|
                pass
            elif another:
                print('asdf')
            |end|
            lastly = 'done'
            '''
        )

        self.compare(code, two_way=True, extra_lines=False, search=True)


class BlocksExtraLinesOff(common.Common):

    '''Test to make sure that block_party find the right lines when extra_lines is off.'''

    def test_config_off(self):
        '''Get only the block.'''
        config.reset()
        config.register_setting(config.COMMENT_KEY, lambda: False)
        config.register_setting(config.WHITESPACE_KEY, lambda: False)

        code = textwrap.dedent(
            '''\

            thing = 8


            #


            |start|if False:
                pass
                |cursor|
            else:
                # info here
                # and there


                print('asdds')|end|

            # asdfasdf



            print('asdf')
            '''
        )

        self.compare(code, two_way=True, extra_lines=False)

    def test_config_on(self):
        '''Get only the block including comments and whitespace.'''
        config.reset()
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            thing = 8


            |start|#


            if False:
                pass
                |cursor|
            else:
                # info here
                # and there


                print('asdds')
            |end|
            # asdfasdf



            print('asdf')
            '''
        )

        self.compare(code, two_way=True, extra_lines=False)


class BlocksExtraLinesOn(common.Common):

    '''Test to make sure extra lines scan properly.'''

    def setUp(self):
        '''Reset the configuration to some reasonable default settings.'''
        super(BlocksExtraLinesOn, self).setUp()
        config.reset()
        config.register_setting(config.COMMENT_KEY, lambda: False)
        config.register_setting(config.WHITESPACE_KEY, lambda: False)

    def tearDown(self):
        '''Reset the user's config after every test.'''
        super(BlocksExtraLinesOn, self).tearDown()
        config.reset()

    def test_config_off_001(self):
        '''Check for newlines around a block.'''
        code = textwrap.dedent(
            '''\

            thing = 8

            # asdfasdfasdf
            # asdfasdfasdf
            #
            |start|


            if False:
                pass
                |cursor|
            else:
                # info here
                # and there


                print('asdds')


            |end|
            print('asdf')
            '''
        )

        self.compare(code, two_way=True, extra_lines=True)

    def test_config_off_002(self):
        '''Check for newlines around a block but stop before comments.'''
        code = textwrap.dedent(
            '''\

            thing = 8
            #
            |start|


            if False:
                pass
                |cursor|
            else:
                # info here
                # and there


                print('asdds')


            |end|
            print('asdf')
            '''
        )

        self.compare(code, two_way=True, extra_lines=True)

    def test_config_on(self):
        '''Check for newlines around a block including comments.'''
        config.reset()
        config.register_setting(config.COMMENT_KEY, lambda: True)
        config.register_setting(config.WHITESPACE_KEY, lambda: True)

        code = textwrap.dedent(
            '''\

            thing = 8
            |start|

            #


            if False:
                pass
                |cursor|
            else:
                # info here
                # and there


                print('asdds')

            |end|
            # asdfasdf


            print('asdf')
            '''
        )

        self.compare(code, two_way=True, extra_lines=True)
