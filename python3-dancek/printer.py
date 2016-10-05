from types import *

def pr_str(tree):
    return _tree_to_string(tree)

def _tree_to_string(tree):
    if isinstance(tree, MalList):
        return '(%s)' % _list_contents(tree)
    elif isinstance(tree, MalVector):
        return '[%s]' % _list_contents(tree)
    elif isinstance(tree, MalSymbol):
        return tree
    elif isinstance(tree, MalString):
        return '"%s"' % tree
    elif tree is None:
        return 'nil'
    elif tree is True:
        return 'true'
    elif tree is False:
        return 'false'
    elif isinstance(tree, int):
        return '%d' % tree

def _list_contents(lst):
    items = [_tree_to_string(x) for x in lst]
    return ' '.join(items)