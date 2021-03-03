import abc
import operator as op
import re
from collections import defaultdict, deque
from functools import reduce
from itertools import chain
from pprint import pprint

from parsy import (
    any_char,
    char_from,
    digit,
    eof,
    generate,
    letter,
    match_item,
    peek,
    regex,
    seq,
    string,
    string_from,
    success,
    whitespace,
)
from pyrsistent import PMap, PSet, field
from pyrsistent import m as M
from pyrsistent import s as S
from pyrsistent import v as V

from utils import puzzle_input

example = "\n".join(
    [
        "1 + 2 * 3 + 4 * 5 + 6",  # 71
        "1 + (2 * 3) + (4 * (5 + 6))",  # 51
        "2 * 3 + (4 * 5)",  # 26
        "5 + (8 * 3 + 9 + 3 * 4 * 3)",  # 437.
        "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",  # 12240.
        "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",  # 13632
    ]
)

# AST
class AST(abc.ABC):
    @abc.abstractmethod
    def apply():
        pass


class BinOp:
    def __init__(self, left, op_, right):
        self._op_str = op_
        self._op = {"+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv}[op_]
        self._left = left
        self._right = right

    def apply(self):
        return self._op(self._left.apply(), self._right.apply())

    def __repr__(self):
        return f"({self._left} {self._op_str} {self._right})"


class Constant:
    def __init__(self, value):
        self._value = value

    def apply(self):
        return self._value

    def __repr__(self):
        return str(self._value)


# Parsing Combinators
# optional_whitespace = regex(r"\s*")
# word = regex(r"\w+")
# number = regex(r"[-+]?\d+").map(Constant)
# @generate
# def binop():
#     return (yield seq(simple, whitespace >> char_from('+-*/') << whitespace, expr))

# simple = number << whitespace| match_item('(') >> binop << match_item(')')
# expr = simple | binop

whitespace = regex(r"\s*")

# lexeme = lambda p: trace(p << whitespace)
lexeme = lambda p: p << whitespace


def trace(p):
    def mapper(v):
        print(repr(v))
        return v

    return p.map(mapper)


# lexical elements
int_ = lexeme(regex(r"\d+")).map(int).map(Constant)
float_ = lexeme(regex(r"\d+.\d+")).map(float).map(Constant)
plus = lexeme(string("+"))
minus = lexeme(string("-"))
lparen = lexeme(string("("))
rparen = lexeme(string(")"))
times = lexeme(string("*"))
div = lexeme(string("/"))

all_op = plus | minus | times | div
additive_op = plus | minus
multiplicative_op = times | div


@generate
def binop():
    left = yield simple
    # print('left', left)
    while True:
        op = yield all_op | success(None)
        #   print('binop', op)
        if not op:
            return left

        right = yield simple
        # print('right', right)
        left = BinOp(left, op, right)
        # print('left')


@generate
def additive():
    sum = yield simple
    while True:
        op = yield additive_op | success(None)
        if not op:
            return sum
        operand = yield simple
        sum = BinOp(sum, op, operand)


@generate
def multiplicative():
    prod = yield additive
    while True:
        op = yield multiplicative_op | success(None)
        if not op:
            return prod
        operand = yield additive
        prod = BinOp(prod, op, operand)


sign_op = plus | minus | success("+")


@generate
def number():
    sign = yield sign_op
    num = yield int_ | float_
    return num if sign == "+" else -num


simple = (lparen >> multiplicative << rparen) | number

expr = whitespace >> multiplicative

s = 0
with puzzle_input(18, example, False) as f:
    for l in f:
        e = expr.parse(l)
        s += e.apply()
        print(e, e.apply())

    print(s)
