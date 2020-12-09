import operator as op
import re
from collections import defaultdict, deque
from functools import reduce
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
        "35",
        "20",
        "15",
        "25",
        "47",
        "40",
        "62",
        "55",
        "65",
        "95",
        "102",
        "117",
        "150",
        "182",
        "127",
        "219",
        "299",
        "277",
        "309",
        "576",
    ]
)

#
# Basically we keep a "window" of the currently active values and their sums
# The values are kept in deque so we can push on one side and pop out the other
# Every time we add or remove a value, we compute its sum with all the other values
# in the window, and update the "set" of actively valid sums. A dict is used to
# act as a reference count (to handle different pairs giving the same sum).
#
class Xmas:
    def __init__(self, preamble_length):
        self._preamble_len = preamble_length
        self._sums = defaultdict(int)
        self._window = deque()

    def feed(self, value):
        if len(self._window) == self._preamble_len:
            if self._sums[value] == 0:
                return value

            d = self._window.popleft()
            for v in self._window:
                s = d + v
                self._sums[s] -= 1

        for o in self._window:
            s = o + value
            self._sums[s] += 1

        self._window.append(value)


#
# A variant on the classic "finding a subsequence" problem
# Here we are looking for a subsequence who's cumulative sum == target
# So we start with the two smallest elements, then we iterate:
#   if the sum is < target,
#       we increase the upper bound and include its value in the running cumulative sum
#   if the sum > targt, we went over
#       remove the lower index value from the cumulative sum and increase the index
# Not sure about the universality here of the algo, but this seems to work because:
# All values are + positive so adding a new value always increases the running sum and
# The values are in a semi-sorted (each value is necessarily a sum of the previous values)
def find_sum_seq(data, sum):
    i = 0
    j = 1
    cs = data[i] + data[j]

    while True:
        if cs == sum:
            return data[i : j + 1]

        if cs < sum:
            j += 1
            cs += data[j]
        elif cs > sum:
            cs -= data[i]
            i += 1
            if i == j:  # bump j so we always have at least 2 elements
                j += i
                cs += data[j]

    pass


with puzzle_input(9, example, False) as f:
    data = [int(e) for e in f.read().split()]
    xmas = Xmas(25)
    for v in data:
        breaking = xmas.feed(v)
        if breaking is not None:
            break

    print(breaking)  # part 1

    data.reverse()
    s = find_sum_seq(data, breaking)
    pprint(s)
    print(min(s) + max(s))  # part 2
