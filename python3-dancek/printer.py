from types import *

def pr_str(tree):
    return _tree_to_string(tree)

def _tree_to_string(tree):
    if isinstance(tree, MalList):
        return '(%s)' % _list_contents(tree.content)
    elif isinstance(tree, MalVector):
        return '[%s]' % _list_contents(tree.content)
    elif isinstance(tree, MalSymbol):
        return tree.content
    elif isinstance(tree, MalString):
        return '"%s"' % tree.content
    elif isinstance(tree, int):
        return '%d' % tree
    elif isinstance(tree, MalNil):
        return 'nil'
    elif isinstance(tree, MalBoolean):
        return 'true' if tree.content else 'false'

def _list_contents(lst):
    items = [_tree_to_string(x) for x in lst]
    return ' '.join(items)