from types import *

def pr_str(tree, print_readably=True):
    return _tree_to_string(tree, print_readably)

def _tree_to_string(tree, print_readably):
    if isinstance(tree, MalList):
        return '(%s)' % _list_contents(tree, print_readably)
    elif isinstance(tree, MalVector):
        return '[%s]' % _list_contents(tree, print_readably)
    elif isinstance(tree, MalHashmap):
        return '{%s}' % _dict_contents(tree, print_readably)
    elif isinstance(tree, MalSymbol):
        return tree
    elif isinstance(tree, MalKeyword):
        return tree
    elif isinstance(tree, str): # mostly MalString
        if print_readably:
            s = tree \
                .replace('\\', '\\\\') \
                .replace('\n', '\\n') \
                .replace('"', '\\"')
            return '"%s"' % s
        else:
            return '%s' % tree
    elif isinstance(tree, MalAtom):
        return "(atom %s)" % tree.target
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
    elif isinstance(tree, MalException):
        return _tree_to_string(tree.description, print_readably)
    else:
        return "UNHANDLED TYPE (%s): %s" % (type(tree), tree)

def _list_contents(lst, print_readably):
    items = [_tree_to_string(x, print_readably) for x in lst]
    return ' '.join(items)

def _dict_contents(dct, print_readably):
    items = ['%s %s' % (_tree_to_string(k, print_readably), _tree_to_string(v, print_readably)) for k,v in dct.items()]
    return ' '.join(items)