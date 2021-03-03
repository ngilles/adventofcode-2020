import abc
import operator as op
import re
from collections import defaultdict, deque
from contextlib import suppress
from dataclasses import dataclass
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

example = """
"""

rfid_key = 8184785  # 5764801
door_key = 5293040  # 17807724

# example
# rfid_key = 5764801
# door_key = 17807724


def find_rounds(target, subject=7):
    derived = subject
    for i in count(2):
        derived = (derived * subject) % 20201227
        if derived == target:
            return i


def rounds(subject, rounds):
    value = subject
    for _ in range(rounds):
        value = (value * subject) % 20201227

    return value


rfid_rounds = find_rounds(rfid_key)
door_rounds = find_rounds(door_key)

print(rfid_rounds, door_rounds)

if rfid_rounds < door_rounds:
    print(rounds(door_key, rfid_rounds - 1))
else:
    print(rounds(rfid_key, door_rounds - 1))
