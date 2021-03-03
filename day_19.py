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

example0 = "\n".join(
    [
        "0: 1 2",
        '1: "a"',
        "2: 1 3 | 3 1",
        '3: "b"',
        "",
        "aab",
        "aba",
        "aaa",
        "abb",
    ]
)

example = "\n".join(
    [
        "0: 4 1 5",
        "1: 2 3 | 3 2",
        "2: 4 4 | 5 5",
        "3: 4 5 | 5 4",
        '4: "a"',
        '5: "b"',
        "",
        "ababbb",
        "bababa",
        "abbbab",
        "aaabbb",
        "aaaabbb",
    ]
)

example2 = "\n".join(
    [
        "42: 9 14 | 10 1",
        "9: 14 27 | 1 26",
        "10: 23 14 | 28 1",
        '1: "a"',
        "11: 42 31",
        "5: 1 14 | 15 1",
        "19: 14 1 | 14 14",
        "12: 24 14 | 19 1",
        "16: 15 1 | 14 14",
        "31: 14 17 | 1 13",
        "6: 14 14 | 1 14",
        "2: 1 24 | 14 4",
        "0: 8 11",
        "13: 14 3 | 1 12",
        "15: 1 | 14",
        "17: 14 2 | 1 7",
        "23: 25 1 | 22 14",
        "28: 16 1",
        "4: 1 1",
        "20: 14 14 | 1 15",
        "3: 5 14 | 16 1",
        "27: 1 6 | 14 18",
        '14: "b"',
        "21: 14 1 | 1 14",
        "25: 1 1 | 1 14",
        "22: 14 14",
        "8: 42",
        "26: 14 22 | 1 20",
        "18: 15 15",
        "7: 14 5 | 1 21",
        "24: 14 1",
        "",
        "abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa",
        "bbabbbbaabaabba",
        "babbbbaabbbbbabbbbbbaabaaabaaa",
        "aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
        "bbbbbbbaaaabbbbaaabbabaaa",
        "bbbababbbbaaaaaaaabbababaaababaabab",
        "ababaaaaaabaaab",
        "ababaaaaabbbaba",
        "baabbaaaabbaaaababbaababb",
        "abbbbabbbbaaaababbbbbbaaaababb",
        "aaaaabbaabaaaaababaa",
        "aaaabbaaaabbaaa",
        "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
        "babaaabbbaaabaababbaabababaaab",
        "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba",
    ]
)


# def apply_rule(rules, rid, input, pos=0):
#     if pos == len(input):
#         return True

#     for alt in rules[rid]:
#         for seq in alt:
#             if seq.startswith('"'):


def trace(fn):
    def wrapper(rules, rid, msg, pos=0):
        v = fn(rules, rid, msg, pos)
        print(f"{fn.__name__}(..., {rid}, ...,{pos}) -> {v}")
        return v

    return wrapper


# @trace
def apply_rule(rules, rid, msg, pos=0, depth=0):
    print("  " * depth, "match_rule", rid, "@", pos)

    rule = rules[rid]
    if pos >= len(msg):
        return False, 0
        # raise Exception('too far')

    if isinstance(rule, str):
        if msg[pos] == rule:
            print("  " * depth, f"matched {rid}")
            return True, 1
        else:
            return False, 0
    else:
        for alt in rule:
            print("  " * depth, f"trying {alt} @ {pos}")
            valid = True
            consumed = 0
            for sr in alt:
                v, c = apply_rule(rules, sr, msg, pos + consumed, depth + 1)
                print("  " * depth, f"{sr} matched {v}, {c}")
                valid &= v
                consumed += c
                if not v:
                    break
            else:
                print("  " * depth, f"{alt} matched {valid}, {consumed}")
                return valid, consumed
        else:
            return False, 0


def compile_rule(rules, rid, depth=0, max_depth=20):
    if depth == max_depth:
        return ""

    rule = rules[rid]

    if isinstance(rule, str):
        return rule
    else:
        alts = []
        for alt in rule:
            v = [compile_rule(rules, r, depth + 1) for r in alt]
            # print(v)
            alts.append("(" + "".join(v) + ")")
        return "(" + "|".join(alts) + ")"


def parse_rule(r):
    if r.startswith('"'):
        return r[1:2]
    else:
        return [list(map(int, e.split())) for e in r.split("|")]


with puzzle_input(19, example2, False) as f:
    rules_def, messages = f.read().split("\n\n")
    rules = {}
    for rule_line in rules_def.split("\n"):
        rule_id, rule_def = rule_line.split(":")
        rule_id = int(rule_id)
        rules[rule_id] = parse_rule(rule_def.strip())

    # Part 2
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    base = compile_rule(rules, 0)
    re_base = re.compile("^" + base + "$")

    # print(rules)
    # print(base)

    # print(sum(1 for msg in messages.split('\n') if re_base.match(msg) is not None))
    good = 0
    for msg in messages.strip().split("\n"):
        print("testing:", msg)
        m = re_base.match(msg)
        if m is not None:
            good += 1

    #     print(v, c, len(msg))
    #     if v and c == len(msg):
    #         good += 1

    print(good)
