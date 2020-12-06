import operator as op
from functools import reduce

from utils import puzzle_input

example = "\n".join(
    [
        "abc",
        "",
        "a",
        "b",
        "c",
        "",
        "ab",
        "ac",
        "",
        "a",
        "a",
        "a",
        "a",
        "",
        "b",
    ]
)


with puzzle_input(6, example, False) as f:
    groups = [[set(a) for a in g.split("\n")] for g in f.read().split("\n\n")]

    # Merge group answer, union ("anyone")
    per_group = [reduce(op.or_, g) for g in groups]
    print(sum(len(g) for g in per_group))

    # Merge group answers, intersection ("everyone")
    per_group = [reduce(op.and_, g) for g in groups]
    print(sum(len(g) for g in per_group))
