from types import *

def pr_str(tree, print_readably=True):
    return _tree_to_string(tree, print_readably)

def _tree_to_string(tree, print_readably):
    if isinstance(tree, MalList):
        return '(%s)' % _list_contents(tree, print_readably)
    elif isinstance(tree, MalVector):
        return '[%s]' % _list_contents(tree, print_readably)
    elif isinstance(tree, MalSymbol):
        return tree
    elif isinstance(tree, MalString):
        if print_readably:
            s = tree.replace('"', '\\"')
            return '"%s"' % s
        else:
            return '%s' % tree
    elif tree is None:
        return 'nil'
    elif tree is True:
        return 'true'
    elif tree is False:
        return 'false'
    elif isinstance(tree, int):
        return '%d' % tree
    elif callable(tree):
        # function
        return '#'
    else:
        return "UNHANDLED TYPE (%s): %s" % (type(tree), tree)

def _list_contents(lst, print_readably):
    items = [_tree_to_string(x, print_readably) for x in lst]
    return ' '.join(items)