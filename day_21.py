import abc
import operator as op
import re
from collections import defaultdict, deque
from functools import reduce
from itertools import chain
from os import read
from pprint import pprint
from typing import Awaitable

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

example = "\n".join(
    [
        "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
        "trh fvjkl sbzzf mxmxvkd (contains dairy)",
        "sqjhc fvjkl (contains soy)",
        "sqjhc mxmxvkd sbzzf (contains fish)",
    ]
)


ingredient = regex(r"\w+")
allergen = regex(r"\w+")

ingredient_list = ingredient.sep_by(match_item(" ")).map(set)
allergen_list = (
    string("contains") >> whitespace >> allergen.sep_by(string(", ")).map(set)
)

ingredients_line = seq(
    ingredient_list, whitespace >> match_item("(") >> allergen_list << match_item(")")
).map(tuple)
ingredients_lines = (
    ingredients_line.sep_by(match_item("\n")) << match_item("\n").optional()
)

with puzzle_input(21, example, False) as f:
    data = ingredients_lines.parse(f.read())
    # print(data)

    ingredients = reduce(op.or_, (i[0] for i in data))
    allergens = reduce(op.or_, (i[1] for i in data))
    print(allergens)
    allergen_candidate = defaultdict(set)

    for a in allergens:
        allergen_candidate[a] = reduce(op.and_, (il for il, al in data if a in al))

    all_candidates = reduce(op.or_, allergen_candidate.values())
    print(allergen_candidate)

    allergen_free = ingredients - all_candidates

    # Part 1
    print(sum(sum(1 for il, al in data if a in il) for a in allergen_free))

    order = [i for i, v in sorted(allergen_candidate.items(), key=lambda x: len(x[1]))]

    def find_solutions(candidates, order, idx: int = 0, seen: PMap = M()):
        print(candidates, idx, order, seen)
        if idx == len(candidates):
            yield seen
        else:
            for candidate in candidates[order[idx]]:
                if candidate not in seen:
                    yield from find_solutions(
                        candidates, order, idx + 1, seen + M(**{candidate: order[idx]})
                    )
                else:
                    print("candidate already seen")

    allergen_mapping = next(find_solutions(allergen_candidate, order))
    print(allergen_mapping)

    print(",".join(i for i, a in sorted(allergen_mapping.items(), key=lambda x: x[1])))
