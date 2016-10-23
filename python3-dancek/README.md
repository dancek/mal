# MAL implementation in Python 3

This is my implementation of [MAL](https://github.com/kanaka/mal), a Clojure-inspired Lisp designed to be a learning tool. It's nothing fancy, but it passes the MAL test suite and has all the capabilities needed for a self-hosting MAL interpreter.

MAL is implemented in steps, so there are 11 different runnable scripts. The complete, final version is `stepA_mal.py`.

## Usage

```
# start a REPL
./run
# run a script
./run script.mal
```

Requires Python 3.5 (because PEP 448 style dictionary unpacking was used in the `assoc` implementation).

## Examples

```
$ ./run
Mal [python3-dancek]
user> (def! fact (fn* [n] (if (> n 1) (* n (fact (- n 1))) 1)))
#
user> (fact 15)
1307674368000
user> (def! fib (fn* (N) (if (= N 0) 1 (if (= N 1) 1 (+ (fib (- N 1)) (fib (- N 2)))))))
#
user> (fib 20)
10946
user> (defmacro! unless (fn* (pred a b) `(if ~pred ~b ~a)))
#
user> (unless false 1 2)
1
user> (macroexpand (unless false 1 2))
(if false 2 1)
```
