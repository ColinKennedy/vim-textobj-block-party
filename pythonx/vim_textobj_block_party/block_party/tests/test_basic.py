#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A module for very simple use cases of block_party.'''

# IMPORT STANDARD LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from . import common


class Blocks(common.Common):

    '''Simple block tests.'''

    def test_while(self):
        '''Test a while-loop.'''
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

        self.compare(code)

    def test_with(self):
        '''Test a with block.'''
        code = textwrap.dedent(
            '''\
            something = 9

            |start|with open('/tmp/something', 'w') as file_:
                file_.write('asdfd')

                |cursor|

                more = 'stuff'|end|

            and_more_lines = ['asdf']
            '''
        )

        self.compare(code)

    def test_for(self):
        '''Test a for-loop.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|for _ in range(10):

                thing = 8

                |cursor|

                if another:
                    pass
            else:
                thing = 9|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)

    def test_try_001(self):
        '''Test a try-block.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|try:
                thing = 8
            except Exception:
                pass
                |cursor|
                pass
            except ValueError:
                another = '1232'
            else:
                # adfasdf adf
                # asdfasfdasdf

                pass
            finally:
                thing = (None,)
                if another:
                    pass|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)

    def test_try_002(self):
        '''Test a try-block.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 8

            |start|try:
                |cursor|
                thing = 8
            except Exception:
                pass
                pass
            except ValueError:
                another = '1232'
            else:
                # adfasdf adf
                # asdfasfdasdf

                pass
            finally:
                thing = (None,)
                if another:
                    pass|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)

    def test_if(self):
        '''Test a if-block.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 10

            |start|if False:
                thing = 8
            elif False:

                |cursor|
                pass
            elif True:
                another = '1232'

            else:
                # adfasdf adf
                # asdfasfdasdf

                pass|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)

    def test_nested(self):
        '''Test multiple, nested blocks.'''
        code = textwrap.dedent(
            '''\
            # info
            #
            another = 10

            |start|while False:
                |cursor|if False:
                    thing = 8
                elif False:

                    pass
                elif True:
                    another = '1232'

                else:
                    # adfasdf adf
                    # asdfasfdasdf

                    pass

                #thing
                whatever = "asdfsdf"|end|

            whatever = "asdfsaf"
            '''
        )

        self.compare(code)
