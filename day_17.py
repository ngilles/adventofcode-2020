import operator as op
import re
from collections import defaultdict, deque
from functools import reduce
from itertools import chain, product
from pprint import pprint

from pyrsistent import PMap, PSet
from pyrsistent import m as M
from pyrsistent import s as S
from pyrsistent import v as V

from utils import puzzle_input

example = "\n".join(
    [
        ".#.",
        "..#",
        "###",
    ]
)


with puzzle_input(17, example, False) as f:
    data = f.read().strip().split("\n")

    def parse_cores(data, dims):
        cc_core = set()  # track the active cores, sparse, in 3d and 4d

        for y, r in enumerate(data):
            for x, c in enumerate(r):
                if c == "#":
                    cc_core.add((x, y) + tuple([0] * (dims - 2)))

        return cc_core

    def get_neighbours(pos, dims):
        for n in product(range(-1, 2), repeat=dims):
            if any(d != 0 for d in n):
                yield tuple(p + d for p, d in zip(pos, n))

    def cycle_core(cores, dims):
        cores_unchecked = cores.copy()
        cores_checked = set()
        new_state = set()

        while cores_unchecked:
            for core in cores_unchecked.copy():
                cores_unchecked.remove(core)
                if core not in cores_checked:
                    cores_checked.add(core)
                    neighbours = list(get_neighbours(core, dims))
                    active_neighbours = sum(1 for n in neighbours if n in cores)
                    if core in cores and active_neighbours in (2, 3):
                        new_state.add(core)

                    elif core not in core and active_neighbours == 3:
                        new_state.add(core)

                    # Add neighbours to check list only if we were part of the orignal active cores
                    if core in cores:
                        for n in neighbours:
                            if n not in cores_checked:
                                cores_unchecked.add(n)

        return new_state

    # Part 1
    cc_core = parse_cores(data, 3)
    for i in range(6):
        cc_core = cycle_core(cc_core, 3)
    print(len(cc_core))

    # Part 2
    cc_core = parse_cores(data, 4)
    for i in range(6):
        cc_core = cycle_core(cc_core, 4)
    print(len(cc_core))
