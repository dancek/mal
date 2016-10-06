#!/usr/bin/env python3

import readline
import sys

import reader, printer
from types import *
from env import Env
from core import ns

repl_env = Env(None)
repl_env.set('eval', lambda ast: EVAL(ast, repl_env))
for name, f in ns.items():
    repl_env.set(name, f)

def is_pair(ast):
    return isinstance(ast, list) and len(ast) > 0

def quasiquote(ast):
    if not is_pair(ast):
        return MalList([MalSymbol('quote'), ast])
    elif ast[0] == 'unquote':
        return ast[1]
    elif is_pair(ast[0]) and ast[0][0] == 'splice-unquote':
        return MalList([MalSymbol('concat'), ast[0][1], quasiquote(ast[1:])])
    else:
        return MalList([MalSymbol('cons'), quasiquote(ast[0]), quasiquote(ast[1:])])

def READ(s):
    return reader.read_str(s)

def EVAL(ast, env):
    while True: # allow tail call optimization (TCO)
        if isinstance(ast, MalList):
            if len(ast) == 0:
                return ast

            call = ast[0]

            if call == 'def!':
                f_name, f_def, *others = ast[1:]
                if others:
                    print('UNEXPECTED: %s' % ast)
                return env.set(f_name, EVAL(f_def, env))

            elif call == 'let*':
                let_env = Env(env)
                bindings = ast[1]
                for i in range(0, len(bindings), 2):
                    key = bindings[i]
                    value = EVAL(bindings[i+1], let_env)
                    let_env.set(key, value)
                # TCO
                ast = ast[2]
                env = let_env
                continue

            elif call == 'do':
                list(map(lambda x: EVAL(x, env), ast[1:-2])) # force evaluation using list
                # TCO
                ast = ast[-1]
                continue

            elif call == 'if':
                test = EVAL(ast[1], env)
                if test is None or test is False:
                    if (len(ast) < 4):
                        return None
                    # TCO
                    ast = ast[3]
                else:
                    # TCO
                    ast = ast[2]
                continue

            elif call == 'fn*':
                binds = ast[1]
                fn_body = ast[2]
                def fn(*params):
                    fn_env = Env(env, binds, params)
                    return EVAL(fn_body, fn_env)
                return MalFunction(fn_body, binds, env, fn)

            elif call == 'quote':
                return ast[1]

            elif call == 'quasiquote':
                ast = quasiquote(ast[1])
                continue

            else:
                f, *args = eval_ast(ast, env)
                if isinstance(f, MalFunction):
                    # TCO
                    ast = f.ast
                    env = Env(f.env, f.params, args)
                    continue
                return f(*args)

        else:
            return eval_ast(ast, env)


def PRINT(s):
    return printer.pr_str(s)

def rep(s):
    try:
        return PRINT(EVAL(READ(s), repl_env))
    except CommentException:
        return

def eval_ast(ast, env):
    if isinstance(ast, MalSymbol):
        return env.get(ast)
    elif isinstance(ast, MalList):
        return MalList(map(lambda x: EVAL(x, env), ast))
    elif isinstance(ast, MalVector):
        return MalVector(map(lambda x: EVAL(x, env), ast))
    elif isinstance(ast, MalHashmap):
        return MalHashmap({k: EVAL(v, env) for k,v in ast.items()})
    else:
        return ast

def main():
    rep("(def! not (fn* (a) (if a false true)))")
    rep("(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \")\")))))")

    if len(sys.argv) > 1:
        filename, *argv = sys.argv[1:]
        print(argv)
        if argv:
            repl_env.set("*ARGV*", argv)
        rep('(load-file "%s")' % filename)
        sys.exit(0)

    while True:
        i = input('user> ')
        try:
            o = rep(i)
            print(o)
        except MalException as e:
            print(e)

if (__name__ == '__main__'):
    main()