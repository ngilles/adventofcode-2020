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
    whitespace,
)
from pyrsistent import PMap, PSet
from pyrsistent import m as M
from pyrsistent import s as S
from pyrsistent import v as V

from utils import puzzle_input

example = "\n".join(
    [
        "class: 1-3 or 5-7",
        "row: 6-11 or 33-44",
        "seat: 13-40 or 45-50",
        "",
        "your ticket:",
        "7,1,14",
        "",
        "nearby tickets:",
        "7,3,47",
        "40,4,50",
        "55,2,20",
        "38,6,12",
    ]
)

example2 = "\n".join(
    [
        "class: 0-1 or 4-19",
        "row: 0-5 or 8-19",
        "seat: 0-13 or 16-19",
        "",
        "your ticket:",
        "11,12,13",
        "",
        "nearby tickets:",
        "3,9,18",
        "15,1,5",
        "5,14,9",
        "",
    ]
)


# Parsing Combinators
optional_whitespace = regex(r"\s*")
word = regex(r"\w+")
number = regex(r"[-+]?\d+").map(int)

rule_name = (letter | match_item(" ")).at_least(1).map(lambda x: "".join(x))
range_ = seq(number, match_item("-") >> number).map(lambda x: range(x[0], x[1] + 1))
range_pair = seq(range_, whitespace >> string("or") >> whitespace >> range_)
rule = seq(rule_name, match_item(":") >> whitespace >> range_pair)
rules = rule.sep_by(match_item("\n")).map(dict)

fields = number.sep_by(match_item(","), min=1)
your_ticket = string("your ticket:\n") >> fields
nearby_tickets = string("nearby tickets:\n") >> fields.sep_by(match_item("\n"))

all_of_it = (
    seq(rules, string("\n\n") >> your_ticket, string("\n\n") >> nearby_tickets)
    << match_item("\n").optional()
)


with puzzle_input(16, example2, False) as field_values:
    data, remain = all_of_it.parse_partial(field_values.read())
    # print(data, repr(remain))
    print(repr(remain))

    all_ranges = list(chain.from_iterable(data[0].values()))
    # print(all_ranges)

    my_ticket = data[1]
    other_tickets = data[2]
    valid_tickets = []

    s = 0
    for ticket in other_tickets:
        valid = True
        for v in ticket:
            if not any(v in r for r in all_ranges):
                s += v
                valid = False
        if valid:
            valid_tickets.append(ticket)  # keeps these for part 2
    print(s)  # Part 1

    # Part 2

    # Find ticked fields are candidates for a field name
    candidates = [set() for i in my_ticket]
    for field_idx in range(len(my_ticket)):
        # Get all the values for the given field
        field_values = [t[field_idx] for t in valid_tickets]
        for field, ranges in data[0].items():
            # If the all fit in the ranges for a given field, mark as candidate
            if all(v in ranges[0] or v in ranges[1] for v in field_values):
                candidates[field_idx].add(field)

    # we want to eliminate as many items as possible early on
    # by ordering those with fewer possibilities first
    order = [i for i, v in sorted(enumerate(candidates), key=lambda x: len(x[1]))]

    def find_solutions(candidates, order, idx: int = 0, seen: PMap = M()):
        if idx == len(candidates):
            yield seen
        else:
            for candidate in candidates[order[idx]]:
                if candidate not in seen:
                    yield from find_solutions(
                        candidates, order, idx + 1, seen + M(**{candidate: order[idx]})
                    )

    field_mapping = next(find_solutions(candidates, order))
    departures = [
        my_ticket[v] for k, v in field_mapping.items() if k.startswith("departure")
    ]
    print(reduce(op.mul, departures))
