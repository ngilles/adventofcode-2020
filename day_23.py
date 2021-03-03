import abc
import operator as op
import re
from collections import defaultdict, deque
from functools import reduce
from itertools import chain, count
from os import read
from pprint import pprint
from typing import Awaitable, Deque

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

cups_order = [3, 2, 6, 5, 1, 9, 4, 7, 8]
# cups_order = [3, 8, 9, 1, 2, 5, 4, 6, 7]


class Cup:
    def __init__(self, id):
        self.id = id
        self.cw = None
        self.ccw = None

    def __repr__(self):
        return f"Cup({self.id})"


cups = [Cup(i) for i in chain(cups_order, range(10, 1_000_000 + 1))]
n_cups = len(cups)

for i in range(n_cups):
    cups[i].cw = cups[(i + 1) % n_cups]
    cups[i].ccw = cups[(i - 1) % n_cups]

cups[0:9] = list(sorted(cups[:9], key=lambda x: x.id))
print(cups[:20])


def print_cups(cup):
    cl = [cup]
    for _ in range(n_cups - 1):
        cup = cup.cw
        cl.append(cup)

    return "".join(str(c.id) for c in cl)


current_cup = cups[cups_order[0] - 1]
print_cups(current_cup)

seen = set()
for round in range(10_000_000):  # 100):
    if round % 100_000 == 0:
        print("round", round)
    splice = current_cup.cw
    next_cup = splice.cw.cw.cw
    current_cup.cw = next_cup
    next_cup.ccw = current_cup

    splice_ids = (splice.id, splice.cw.id, splice.cw.cw.id)
    # print(splice_ids)

    dest_id = ((current_cup.id - 1 - 1) % n_cups) + 1
    while dest_id in splice_ids:
        dest_id = ((dest_id - 1 - 1) % n_cups) + 1

    # print('dest cup', dest_id)
    dest_cup = cups[dest_id - 1]
    dest_next = dest_cup.cw

    dest_cup.cw = splice
    splice.ccw = dest_cup

    dest_next.ccw = splice.cw.cw
    splice.cw.cw.cw = dest_next

    # print_cups(current_cup)
    current_cup = current_cup.cw


# print(print_cups(current_cup))
while current_cup.id != 1:
    current_cup = current_cup.cw

print(current_cup, current_cup.cw, current_cup.cw.cw)
