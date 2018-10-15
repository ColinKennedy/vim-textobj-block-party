#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The main module which is used to find Python code-block boundary lines.'''

# IMPORT STANDARD LIBRARIES
try:
    # Python 2
    import __builtin__ as builtins
except ImportError:
    # Python 3
    import builtins
import keyword
import re

# IMPORT THIRD-PARTY LIBRARIES
from parso.python import tree
import parso

# IMPORT LOCAL LIBRARIES
from . import config


_ALL_BLOCK_CLASSES = (
    tree.ForStmt,
    tree.IfStmt,
    tree.TryStmt,
    tree.WhileStmt,
)
_BUILTIN_WORDS = set(dir(builtins) + keyword.kwlist)
_WORD_EXPRESSION = re.compile(r'\w+')


def _get_node_header(node):
    '''Get every line of the parso node that is a comment or whitespace.

    For some reason, parso node `start_pos` is the start of the statement,
    even though the node itself may contain comments or whitespace.

    Anyway, we get those lines by subtracting the "length" of the statement
    by its stored source code.

    So in this case "header" means "all the whitespace and comments before `node`".

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`): The node to get the header of.

    Returns:
        list[str]: The found header lines, if any.

    '''
    start = node.start_pos[0]
    end = node.end_pos[0]

    length = end - start
    return node.get_code().split('\n')[:-1 * (length + 1)]


def _get_defined_identifiers(node):
    '''set[str]: Find every identifier that the block created or uses.'''
    def _get_node_text(nodes):
        return set((node.value for node in nodes))

    names = set()

    if hasattr(node, 'get_test_nodes'):  # It may be a IfStmnt
        names = set()

        for node in node.get_test_nodes():
            try:
                names.add(node.value)
            except AttributeError:
                names.update(_get_node_identifiers(node, use_all=True))

        return names

    if isinstance(node, tree.ForStmt):
        test = node.get_testlist()

        try:
            return {test.value, }
        except AttributeError:
            return _get_node_identifiers(test, use_all=True)

    if hasattr(node, 'get_except_clause_tests'):
        names = node.get_except_clause_tests()

    return _get_node_text(names)


def _get_defined_node_identifiers(node, use_all=False):
    '''Find every identifier that the block created.

    For example, if a try-except block uses "ValueError" then this function
    will ignore "ValueError" because its a builtin name.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`):
            The node get identifiers for.
        use_all (`bool`, optional):
            If True, use the identifiers inside of the block.
            If False, only use the identifiers that the block defines.
            Default is False.

    Returns:
        set[str]: The found identifiers.

    '''
    return _get_node_identifiers(node, use_all=use_all) - _BUILTIN_WORDS


def _get_extra_end_lines(node, end):
    count = 0
    suffix = node.get_root_node().get_code().split('\n')[end + 1:]

    for line in suffix:
        if line:
            break

        count += 1

    return count


def _get_extra_start_lines(node, start):
    count = 0
    prefix = node.get_root_node().get_code().split('\n')[:start]

    for line in reversed(prefix):
        if line:
            break

        count += 1

    return count


def _get_nested_children(node, seen=None):
    '''Find every child node of the given `node`, recursively.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`):
            The node to get children of.
        seen (set[:class:`parso.python.tree.PythonBaseNode`]):
            The nodes that have already been checked.

    Yields:
        :class:`parso.python.tree.PythonBaseNode`: The found children.

    '''
    if not seen:
        seen = set()

    if not hasattr(node, 'children'):
        yield
        return

    for child in node.children:
        if child not in seen:
            seen.add(child)

            yield child

            for subchild in _get_nested_children(child):
                yield subchild


def _get_node_identifiers(node, use_all=False):
    '''Find every identifier that `node` defines or uses.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`):
            The node to get identifiers for.
        use_all (`bool`, optional):
            If True, use the identifiers inside of the block.
            If False, only use the identifiers that the block defines.
            Default is False.

    Returns:
        set[str]: Every identifier that the block created or uses.

    '''
    def _get_all_identifiers(node):
        '''set[str]: Find every identifier inside the node, recursively.'''
        identifiers = set()
        for child in _get_nested_children(node):
            if isinstance(child, tree.Name):
                identifiers.add(child.value)

        return identifiers

    if not use_all:
        return _get_defined_identifiers(node)

    return _get_all_identifiers(node)


def _get_previous_leaf_header(node):
    '''Get the code and header of the node prior to the given one.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode` or NoneType):
            The node to get the previous node's information from.

    Returns:
        list[str]: The source-code and whitespace/comments above the found node.

    '''
    all_lines = node.get_root_node().get_code().split('\n')
    previous_nodes = list(_get_previous_non_block_nodes(node))
    start = previous_nodes[-1].end_pos[0]
    end = previous_nodes[0].start_pos[0]
    previous_lines = all_lines[start - 1:end]
    return previous_lines


def _get_previous_non_block_nodes(node):
    '''Get every leaf before thie given `node` until a new Python block is found.'''
    previous = node.get_previous_leaf()

    while previous and not isinstance(previous, _ALL_BLOCK_CLASSES):
        yield previous
        previous = previous.get_previous_leaf()


def get_leaf(graph, row, column):
    '''Find the parso node that best matches the given row/column.

    Args:
        graph (:class:`parso.python.tree.Module`):
            The parsed Python code.
        row (int):
            The line which will be used to find the "closest" leaf.
            Any leaf whose starting line exceeds is value will be ignored.
            This value is base-1.
        column (int):
            The column position of the cursor in `row`. This value is base-0.

    Returns:
        :class:`parso.python.tree.PythonBaseNode` or NoneType: The found node.

    '''
    leaf = graph.get_leaf_for_position((row, column))

    if leaf:
        return leaf

    leaf = graph.get_first_leaf()
    previous = leaf

    while leaf:
        if leaf.start_pos[0] >= row:
            return previous

        previous = leaf
        leaf = leaf.get_next_leaf()


def get_nearest_class(code, row, column, classes=_ALL_BLOCK_CLASSES):
    '''Get the parso node that is closet to a given row.

    Args:
        code (str):
            The Python code to parse.
        row (int):
            The line which will be used to find the "closest" leaf.
            Any leaf whose starting line exceeds is value will be ignored.
            This value is base-0.
        column (int):
            The column position of the cursor in `row`. This value is base-0.
        classes (class or tuple[class]):
            The allowed parso types to search for.
            If no node matching one of these class types are found,
            None is returned instead. If no classes are given, the supported
            parso classes are used instead.

    Returns:
        :class:`parso.python.tree.PythonBaseNode` or NoneType: The found node.

    '''
    graph = parso.parse(code)

    leaf = get_leaf(graph, row, column)

    parent = leaf
    while parent:
        if isinstance(parent, classes):
            return parent

        parent = parent.parent


def get_block_name(node):
    '''Convert a parso node into a "block_party-friendly" block type.

    This block-type is used in a number of places, including configuration settings.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`): The node to get a block name of.

    Returns:
        str: The found block name, if any.

    '''
    blocks = {
        tree.ForStmt: 'for',
        tree.IfStmt: 'if',
        tree.TryStmt: 'try',
        tree.WhileStmt: 'while',
    }

    try:
        return blocks[node.__class__]
    except KeyError:
        return ''


def get_boundary(  # pylint: disable=too-many-arguments
        code,
        row,
        column,
        classes=_ALL_BLOCK_CLASSES,
        extra_lines=False,
        search=True,
        two_way=False,
        customize=True,
):
    '''Get the start and end row for the code block in some Python source code.

    Args:
        code (str):
            The Python code to parse.
        row (int):
            The line which will be used to find the "closest" leaf.
            Any leaf whose starting line exceeds is value will be ignored.
            This value is base-0.
        column (int):
            The column position of the cursor in `row`. This value is base-0.
        classes (class or tuple[class]):
            The allowed parso types to search for.
            If no node matching one of these class types are found,
            None is returned instead. If no classes are given, the supported
            parso classes are used instead.
        extra_lines (`bool`, optional):
            If True, after a match is found, add any neighboring newlines to the boundary.
            If False, leave the boundary alone.
            This is useful if you want to delete whitespace around a block.
            Default is False.
        search (`bool`, optional):
            If True, search for source-code lines (like variables) that are defined
            in the current Python block. If False, only search for non-source-code lines.
            Default is True.
        two_way (`bool`, optional):
            If True, search for whitespaces/comments/etc before and after the block.
            If False, only search up.
            Default is False.
        customize (`bool`, optional):
            If True, use the user's configuration while searching for extra lines.
            If False, ignore the user's configuration.
            Default is True.

    Returns:
        tuple[int, int]:
            The found boundary. If no boundary was found, return back (-1, -1).


    '''
    node = get_nearest_class(code, row, column, classes)
    block = get_block_name(node)

    if not block or not node:
        return (-1, -1)

    return get_expanded_boundary(
        node,
        extra_lines=extra_lines,
        search=search,
        two_way=two_way,
        customize=customize,
    )


def get_start(node, search=True, customize=True):
    '''Get the starting row of the Python block.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`):
            The node to get the starting line of.
        search (`bool`, optional):
            If True, search for source-code lines (like variables) that are defined
            in the current Python block. If False, only search for non-source-code lines.
            Default is True.
        customize (`bool`, optional):
            If True, use the user's configuration while searching for extra lines.
            If False, ignore the user's configuration.
            Default is True.

    Returns:
        int: The start of the boundary.

    '''
    start = node.start_pos[0] - 1  # `start_pos` starts at 1 minus 1 to get a 0-based index

    if not customize:
        return start

    header = _get_node_header(node)

    if search:
        # `search` requires more than just the header of the given `node` but
        # also the source-code and whitespace/commments of the next child node before it
        #
        header = _get_previous_leaf_header(node) + header

    identifiers = set()
    if search:
        greedy = config.allow_greedy()
        identifiers = _get_defined_node_identifiers(node, use_all=greedy)

    start -= scan_up(header, identifiers=identifiers, search=search)
    return start


def get_end(node, two_way=False, customize=True):
    '''Get the ending row of the Python block.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`):
            The node to get the ending line of.
        search (`bool`, optional):
            If True, search for source-code lines (like variables) that are defined
            in the current Python block. If False, only search for non-source-code lines.
            Default is True.
        two_way (`bool`, optional):
            If True, search for whitespaces/comments/etc before and after the block.
            If False, only search up.
            Default is False.
        customize (`bool`, optional):
            If True, use the user's configuration while searching for extra lines.
            If False, ignore the user's configuration.
            Default is True.

    Returns:
        int: The end of the boundary.

    '''
    leaf = node.get_next_leaf()

    # `end_pos` starts at 1 minus 1 to get a 0-based index
    # And then minus 1 again to get the correct line number
    #
    end = node.end_pos[0] - 2

    if not leaf:
        return end

    if not two_way:
        return end

    header = _get_node_header(leaf)

    offset = 0
    if customize:
        offset = scan_down(header, search=False, allow_comment=False)

    return end + offset


def get_expanded_boundary(
        node,
        extra_lines=False,
        search=True,
        two_way=False,
        customize=True,
):
    '''Get the boundary at or outside of the given Python block node.

    Args:
        node (:class:`parso.python.tree.PythonBaseNode`):
            The block to get the expanded boundary of.
        extra_lines (`bool`, optional):
            If True, after a match is found, add any neighboring newlines to the boundary.
            If False, leave the boundary alone.
            This is useful if you want to delete whitespace around a block.
            Default is False.
        search (`bool`, optional):
            If True, search for source-code lines (like variables) that are defined
            in the current Python block. If False, only search for non-source-code lines.
            Default is True.
        two_way (`bool`, optional):
            If True, search for whitespaces/comments/etc before and after the block.
            If False, only search up.
            Default is False.
        customize (`bool`, optional):
            If True, use the user's configuration while searching for extra lines.
            If False, ignore the user's configuration.
            Default is True.

    Returns:
        tuple[int, int]:
            The found boundary. This boundary will always contain the boundary
            of `node` but could possibly contain more lines than that, depending
            on the user's configuration and the other variables.

    '''
    start = get_start(node, search=search, customize=customize)
    end = get_end(node, two_way=two_way, customize=customize)

    if extra_lines:
        start -= _get_extra_start_lines(node, start)

    if two_way and extra_lines:
        end += _get_extra_end_lines(node, end)

    return (start, end)


def scan_down(lines, identifiers=None, search=True, allow_comment=True):
    '''Look through the given lines and count the number of "allowed" lines.

    An "allowed" line is a line that the user specified to track,
    like whitespace or comments or relevant source-code lines.

    Args:
        lines (iter[str]):
            The Python code to search through.
        search (`bool`, optional):
            If True, search for source-code lines (like variables) that are defined
            in the current Python block. If False, only search for non-source-code lines.
            Default is True.

    '''
    if not identifiers:
        identifiers = set()

    offset = 0
    comments_found = False

    for line in lines:
        line = line.strip()

        if not line and (comments_found or not config.allow_whitespace()):
            # Don't keep searching for whitespace if comments were found
            # or if the user's configuration has comment searching disabled
            #
            break

        if not allow_comment and line.startswith('#'):
            break
        elif allow_comment and line.startswith('#'):
            comments_found = True

            if not config.allow_comment():
                break
        elif line and search and config.allow_search():
            has_common_words = identifiers & set(_WORD_EXPRESSION.findall(line))

            if not has_common_words:
                break
        elif line and not config.allow_search():
            break

        offset += 1

    return offset


def scan_up(lines, identifiers=None, search=True):
    '''Look through the given lines and count the number of "allowed" lines.

    An "allowed" line is a line that the user specified to track,
    like whitespace or comments or relevant source-code lines.

    Args:
        lines (iter[str]):
            The Python code to search through.
        search (`bool`, optional):
            If True, search for source-code lines (like variables) that are defined
            in the current Python block. If False, only search for non-source-code lines.
            Default is True.

    '''
    if not identifiers:
        identifiers = set()

    return scan_down(reversed(lines), identifiers=identifiers, search=search)
