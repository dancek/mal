#!/usr/bin/env python3
import reader, printer
from types import *

repl_env = {'+': lambda a,b: a+b,
            '-': lambda a,b: a-b,
            '*': lambda a,b: a*b,
            '/': lambda a,b: int(a/b)}

def READ(s):
    return reader.read_str(s)

def EVAL(ast, env):
    if isinstance(ast, MalList):
        if len(ast) == 0:
            return ast
        f, *args = eval_ast(ast, env)
        return f(*args)
    else:
        return eval_ast(ast, env)

def PRINT(s):
    return printer.pr_str(s)

def rep(s):
    return PRINT(EVAL(READ(s), repl_env))

def eval_ast(ast, env):
    if isinstance(ast, MalSymbol):
        if ast in env:
            return env[ast]
        else:
            raise MalException("%s not defined" % ast)
    elif isinstance(ast, MalList):
        return map(lambda x: EVAL(x, env), ast)
    elif isinstance(ast, MalVector):
        return MalVector(map(lambda x: EVAL(x, env), ast))
    elif isinstance(ast, MalHashmap):
        return MalHashmap({k: EVAL(v, env) for k,v in ast.items()})
    else:
        return ast

def main():
    while True:
        i = input('user> ')
        try:
            o = rep(i)
            print(o)
        except MalException as e:
            print(e)

if (__name__ == '__main__'):
    main()