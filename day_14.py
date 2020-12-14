import operator as op
import re
from collections import deque
from functools import reduce
from itertools import combinations, count
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
    whitespace,
)

from utils import puzzle_input

example = "\n".join(
    [
        "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
        "mem[8] = 11",
        "mem[7] = 101",
        "mem[8] = 0",
    ]
)

example2 = "\n".join(
    [
        "mask = 000000000000000000000000000000X1001X",
        "mem[42] = 100",
        "mask = 00000000000000000000000000000000X0XX",
        "mem[26] = 1",
    ]
)


def build_mask(mask_chars):
    mask_and = 0
    mask_or = 0

    for i, v in zip(count(), reversed(mask_chars)):
        if v == "X":
            mask_and |= 1 << i
        else:
            mask_or |= int(v) << i

    return mask_and, mask_or


# Parsing Combinators
optional_whitespace = regex(r"\s*")
word = regex(r"\w+")
number = regex(r"[-+]?\d+").map(int)

mask_inst = seq(
    string("mask"),
    whitespace
    >> match_item("=")
    >> whitespace
    >> char_from("X01").at_least(1).map(build_mask),
)
mem_inst = seq(
    string("mem"),
    match_item("[") >> number << match_item("]"),
    whitespace >> match_item("=") >> whitespace >> number,
)
instruction = mask_inst | mem_inst
program = instruction.sep_by(string("\n")) << string("\n").optional()


with puzzle_input(14, example2, False) as f:
    data, remain = program.parse_partial(f.read())
    # pprint(data)
    print("\n\n\nremaining:", repr(remain))

    # pprint(data)

    # Part 1
    # not sure how many addresses we need, probably sparse, we never read (defaultdict would help then)
    mem = dict()
    mask_and, mask_or = 2 ** 36 - 1, 0  # default mask get everything

    for cmd, *ops in data:
        if cmd == "mask":
            mask_and, mask_or = ops[0]

        elif cmd == "mem":
            mem_addr, value = ops
            v = (value & mask_and) | mask_or
            mem[mem_addr] = (value & mask_and) | mask_or

    print(sum(mem.values()))

    # Part 2
    mem = dict()
    mask_and, mask_or = 2 ** 36 - 1, 0

    def mem_addrs(mask_and: int, mask_or: int, addr: int):
        # mask the address with the mask, and floatings (X) set to 0
        base = (addr | (mask_and | mask_or)) & ~mask_and
        # computer powers of the floatings
        x_powers = [2 ** i for i in range(mask_and.bit_length()) if 2 ** i & mask_and]

        # build adress of all possible addresses by mixing in all the combinations of the floating bits
        addrs = []
        for i in range(len(x_powers) + 1):
            for c in combinations(x_powers, i):
                addrs.append(reduce(op.or_, c, base))

        return addrs

    for cmd, *ops in data:
        if cmd == "mask":
            mask_and, mask_or = ops[0]

        elif cmd == "mem":
            mem_addr, value = ops
            for ma in mem_addrs(mask_and, mask_or, mem_addr):
                mem[ma] = value

    print(sum(mem.values()))
