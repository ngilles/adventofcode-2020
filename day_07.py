import operator as op
import re
from collections import deque
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
        "light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags.",
    ]
)

example2 = "\n".join(
    [
        "shiny gold bags contain 2 dark red bags.",
        "dark red bags contain 2 dark orange bags.",
        "dark orange bags contain 2 dark yellow bags.",
        "dark yellow bags contain 2 dark green bags.",
        "dark green bags contain 2 dark blue bags.",
        "dark blue bags contain 2 dark violet bags.",
        "dark violet bags contain no other bags.",
    ]
)


# Parsing Combinators
optional_whitespace = regex(r"\s*")
word = regex(r"\w+")
number = regex(r"\d+")

color_att = word
color = word
bag_term = string_from("bag", "bags")

bag = seq(color_att, whitespace >> color).map(tuple) << whitespace << bag_term

no_content = string("no other bags").map(lambda x: {})
content = (
    seq(number.map(int), whitespace >> bag)
    .map(lambda a: (a[1], a[0]))
    .sep_by(string(", "))
    .map(dict)
)
bag_contents = no_content | content

rule = seq(
    bag, whitespace >> string("contain") >> whitespace >> bag_contents
) << string(".")
rules = rule.sep_by(string("\n")).map(dict) << string("\n").optional()


def find_containers(mapping, bag):
    seen = set()
    visit = deque([bag])
    while visit:
        bag = visit.popleft()
        for c in mapping[bag]["contained_by"]:
            if c not in seen:
                seen.add(c)
                visit.append(c)

    return seen


# we added a 'total_bags' field to memoize results so we don't recompute in other branches
def count_children(mapping, bag):
    mbag = mapping[bag]
    if mbag["total_bags"] is None:
        mbag["total_bags"] = 1 + sum(
            count_children(mapping, child) * count
            for child, count in mbag["contains"].items()
        )
    return mbag["total_bags"]


with puzzle_input(7, example2, False) as f:
    data, remain = rules.parse_partial(f.read())
    # pprint(data)
    # print('\n\n\nremaining:', repr(remain))

    mapping = {
        k: {"contains": v, "contained_by": set(), "total_bags": None}
        for k, v in data.items()
    }
    for k, v in data.items():
        for c in v:
            mapping[c]["contained_by"].add(k)

    shiny_gold = ("shiny", "gold")

    print(len(find_containers(mapping, shiny_gold)))
    print(count_children(mapping, shiny_gold) - 1)  # -1: remove the top shiny gold bag
