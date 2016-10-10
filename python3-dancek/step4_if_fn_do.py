#!/usr/bin/env python3

import readline

import reader, printer
from types import *
from env import Env
from core import ns

repl_env = Env(None)
for name, f in ns.items():
    repl_env.set(name, f)

def READ(s):
    return reader.read_str(s)

def EVAL(ast, env):
    if isinstance(ast, MalList):
        if len(ast) == 0:
            return ast

        call = ast[0]

        if call == 'def!':
            f_name, f_def = ast[1:]
            return env.set(f_name, EVAL(f_def, env))

        elif call == 'let*':
            let_env = Env(env)
            bindings = ast[1]
            for i in range(0, len(bindings), 2):
                key = bindings[i]
                value = EVAL(bindings[i+1], let_env)
                let_env.set(key, value)
            return EVAL(ast[2], let_env)

        elif call == 'do':
            return list(map(lambda x: EVAL(x, env), ast[1:]))[-1]

        elif call == 'if':
            test = EVAL(ast[1], env)
            if test is None or test is False:
                if (len(ast) < 4):
                    return None
                return EVAL(ast[3], env)
            else:
                return EVAL(ast[2], env)

        elif call == 'fn*':
            binds = ast[1]
            fn_body = ast[2]
            def fn(*params):
                fn_env = Env(env, binds, params)
                return EVAL(fn_body, fn_env)
            return fn

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
        return env.get(ast)
    elif isinstance(ast, MalList):
        return MalList(map(lambda x: EVAL(x, env), ast))
    elif isinstance(ast, MalVector):
        return MalVector(map(lambda x: EVAL(x, env), ast))
    else:
        return ast

def main():
    rep("(def! not (fn* (a) (if a false true)))")

    while True:
        i = input('user> ')
        try:
            o = rep(i)
            print(o)
        except MalException as e:
            print(e)

if (__name__ == '__main__'):
    main()