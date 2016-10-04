#!/usr/bin/env python3

def READ(s):
    return s

def EVAL(s):
    return s

def PRINT(s):
    return s

def rep(s):
    return PRINT(EVAL(READ(s)))

def main():
    while True:
        i = input('user> ')
        o = rep(i)
        print(o)

if (__name__ == '__main__'):
    main()