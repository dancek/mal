from types import *

def pr_str(tree):
    return _tree_to_string(tree)

def _tree_to_string(tree):
    if isinstance(tree, MalList):
        items = [_tree_to_string(x) for x in tree.content]
        return '(%s)' % ' '.join(items)
    elif isinstance(tree, MalSymbol):
        return tree.content
    elif isinstance(tree, MalString):
        return '"%s"' % tree.content
    elif isinstance(tree, int):
        return '%d' % tree