import operator as op
import re
from collections import Counter, defaultdict, deque
from copy import deepcopy
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
        "L.LL.LL.LL",
        "LLLLLLL.LL",
        "L.L.L..L..",
        "LLLL.LL.LL",
        "L.LL.LL.LL",
        "L.LLLLL.LL",
        "..L.L.....",
        "LLLLLLLLLL",
        "L.LLLLLL.L",
        "L.LLLLL.LL",
    ]
)


def compute_neigbours(seats):
    nrows = len(seats)
    ncols = len(seats[0])

    neighbours = [[[] for c in range(ncols)] for r in range(ncols)]
    for i in range(nrows):
        for j in range(ncols):
            for ii in range(max(0, i - 1), min(i + 2, nrows)):
                for jj in range(max(0, j - 1), min(j + 2, ncols)):
                    if not (i == ii and j == jj) and seats[ii][jj] == "L":
                        neighbours[i][j].append((ii, jj))

    return neighbours


def compute_visible_neighbours(seats):
    directions = [
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
    ]

    nrows = len(seats)
    ncols = len(seats[0])

    neighbours = [[[] for c in range(ncols)] for r in range(ncols)]
    for i in range(nrows):
        for j in range(ncols):
            for d in directions:
                ii, jj = i + d[0], j + d[1]
                while 0 <= ii < nrows and 0 <= jj < ncols:
                    if seats[ii][jj] == "L":
                        neighbours[i][j].append((ii, jj))
                        break
                    ii, jj = ii + d[0], jj + d[1]

    return neighbours


def next_gen(seats, neighbours):
    nrows = len(seats)
    ncols = len(seats[0])

    new_seats = deepcopy(seats)  # [[None] * ncols for i in range(nrows)]
    change = False

    for i in range(nrows):
        for j in range(ncols):
            o = seats[i][j]
            n = sum(
                1 for ni, nj in neighbours[i][j] if seats[ni][nj] == "#"
            )  # occupied_seats(i, j)
            if o == "L" and n == 0:
                new_seats[i][j] = "#"
                change = True
            elif o == "#" and n >= 5:
                new_seats[i][j] = "L"
                change = True
            # else:
            #     new_seats[i][j] = o

    return change, new_seats


def print_seats(seats):
    for r in seats:
        print("".join(r))
        # print(r)
    print()


with puzzle_input(11, example, False) as f:
    data = [list(e) for e in f.read().split()]

    neighbours = compute_visible_neighbours(data)
    # print(neighbours)
    p = data
    c, n = next_gen(data, neighbours)
    # print_seats(data)
    # print_seats(n)
    # print(c)
    while c:
        c, n = next_gen(n, neighbours)
        # print_seats(n)

    print(sum(1 for r in n for s in r if s == "#"))
