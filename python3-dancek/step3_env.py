#!/usr/bin/env python3
import reader, printer
from types import *
from env import Env

repl_env = Env(None)
repl_env.set('+', lambda a,b: a+b)
repl_env.set('-', lambda a,b: a-b)
repl_env.set('*', lambda a,b: a*b)
repl_env.set('/', lambda a,b: int(a/b))

def READ(s):
    return reader.read_str(s)

def EVAL(ast, env):
    if isinstance(ast, MalList):
        if len(ast.content) == 0:
            return ast

        call = ast.content[0].content
        if call == 'def!':
            f_name, f_def = ast.content[1:]
            return env.set(f_name, EVAL(f_def, env))
        elif call == 'let*':
            let_env = Env(env)
            bindings = ast.content[1].content
            for i in range(0, len(bindings), 2):
                key = bindings[i]
                value = EVAL(bindings[i+1], let_env)
                let_env.set(key, value)
            return EVAL(ast.content[2], let_env)
        else:
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
        return env.get(ast.content)
    elif isinstance(ast, MalList):
        return list(map(lambda x: EVAL(x, env), ast.content))
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