import operator as op
import re
from collections import Counter, defaultdict, deque
from functools import reduce
from itertools import tee
from pprint import pprint

from parsy import (
    any_char,
    char_from,
    digit,
    eof,
    generate,
    letter,
    peek,
    regex,
    seq,
    string,
    string_from,
    whitespace,
)

from utils import puzzle_input

example = "\n".join(
    [
        "16",
        "10",
        "15",
        "5",
        "1",
        "11",
        "7",
        "19",
        "6",
        "12",
        "4",
    ]
)

example2 = "\n".join(
    [
        "28",
        "33",
        "18",
        "42",
        "31",
        "14",
        "46",
        "20",
        "48",
        "47",
        "24",
        "23",
        "49",
        "45",
        "19",
        "38",
        "39",
        "11",
        "1",
        "32",
        "25",
        "35",
        "8",
        "17",
        "7",
        "9",
        "4",
        "2",
        "34",
        "10",
        "3",
    ]
)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


with puzzle_input(10, example2, False) as f:
    data = [int(e) for e in f.read().split()]

    full = deque([0])  # start from dead battery
    builtin = max(data) + 3  # built in jotlage adapter
    full.extend(sorted(data))  # sorted? simplest way they can all be arranged
    builtin = max(data) + 3  # built in jotlage adapter
    full.append(builtin)

    jumps = [b - a for a, b in pairwise(full)]
    jolt_jumps = Counter(jumps)
    print(jolt_jumps[1] * jolt_jumps[3])  # Part 1

    # Part 2
    # DFS works for examples, and gives the paths... but for real inputs...
    # build adjacency, n^2? beurk but makes implementing the loop next much simpler
    adj = {}
    for v in full:
        adj[v] = {o for o in full if 1 <= (o - v) <= 3}

    def count_paths(adj, full):
        counts = {v: 0 for v in full}
        counts[0] = 1
        for v in full:
            for a in adj[v]:
                counts[a] += counts[v]

        return counts

    print(count_paths(adj, full))
