import operator as op
import re
from collections import defaultdict, deque
from functools import reduce
from itertools import combinations, count, islice
from pprint import pprint

from utils import puzzle_input

example = "\n".join(
    [
        "0,3,6",
    ]
)


with puzzle_input(15, example, False) as f:
    data = [int(l) for l in f.readline().strip().split(",")]

    mem_pos = defaultdict(lambda: deque(maxlen=2))
    mem_count = defaultdict(int)

    def memory_game_iter(starting_numbers):
        # store position of previously seen number, except the last of the seed starting
        mem_lastpos = {n: i + 1 for i, n in enumerate(starting_numbers[:-1])}
        yield from starting_numbers
        next_spoken = starting_numbers[-1]
        i = len(starting_numbers)
        while True:
            prev = next_spoken
            if next_spoken in mem_lastpos:
                next_spoken = i - mem_lastpos[next_spoken]
            else:
                next_spoken = 0
            mem_lastpos[prev] = i
            yield next_spoken
            i += 1

    def memory_game_dict(starting_numbers, until):
        # store position of previously seen number, except the last of the seed starting
        # offset by 1 to make the loop code simpler
        mem_lastpos = {n: i + 1 for i, n in enumerate(starting_numbers[:-1])}
        next_spoken = starting_numbers[-1]
        for i in range(len(starting_numbers), until):
            prev = next_spoken
            if next_spoken in mem_lastpos:
                next_spoken = i - mem_lastpos[next_spoken]
            else:
                next_spoken = 0
            mem_lastpos[prev] = i

        return next_spoken

    def memory_game_list(starting_numbers, until):
        mem_lastpos = [-1] * until
        # store position of previously seen number, except the last of the seed starting
        # offset by 1 to make the loop code simpler
        for i, n in enumerate(starting_numbers[:-1]):
            mem_lastpos[n] = i + 1

        next_spoken = starting_numbers[-1]
        for i in range(len(starting_numbers), until):
            prev = next_spoken
            if mem_lastpos[next_spoken] != -1:
                next_spoken = i - mem_lastpos[next_spoken]
            else:
                next_spoken = 0
            mem_lastpos[prev] = i

        return next_spoken


# mg = memory_game(data)
n = 30_000_000
# print(list(islice(mg, 2020)))
# print(list(islice(mg, n-1, n)))
# print(memory_game(data, 2020))
# print(memory_game_dict(data, 30_000_000))
print(memory_game_list(data, 2020))
print(memory_game_list(data, 30_000_000))
