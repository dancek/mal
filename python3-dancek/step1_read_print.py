#!/usr/bin/env python3
import reader, printer
from types import MalException

def READ(s):
    return reader.read_str(s)

def EVAL(s):
    return s

def PRINT(s):
    return printer.pr_str(s)

def rep(s):
    return PRINT(EVAL(READ(s)))

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