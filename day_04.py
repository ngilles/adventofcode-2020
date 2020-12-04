import operator as op
import re
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
)

from utils import puzzle_input

example = "\n".join(
    [
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
        "byr:1937 iyr:2017 cid:147 hgt:183cm",
        "",
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
        "hcl:#cfa07d byr:1929",
        "",
        "hcl:#ae17e1 iyr:2013",
        "eyr:2024",
        "ecl:brn pid:760753108 byr:1931",
        "hgt:179cm",
        "",
        "hcl:#cfa07d eyr:2025 pid:166559648",
        "iyr:2011 ecl:brn hgt:59in",
        "",
    ]
)

eye_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
passport_validation = {
    "byr": lambda v: 1920 <= int(v) <= 2002,
    "iyr": lambda v: 2010 <= int(v) <= 2020,
    "eyr": lambda v: 2020 <= int(v) <= 2030,
    "hgt": lambda v: (
        (v.endswith("cm") and (150 <= int(v[:-2]) <= 193))
        or (v.endswith("in") and (59 <= int(v[:-2]) <= 76))
    ),
    "hcl": lambda v: re.match("^#([0-9a-f]){6}$", v) is not None,
    "ecl": lambda v: v in eye_colors,
    "pid": lambda v: re.match(r"^\d{9}$", v) is not None,
    "cid": lambda v: True,
}

_essential_keys = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    #'cid',
}

optional_whitespace = regex(r"\s*")

field_key = string_from(*passport_validation.keys()).desc("field key")
field_value = regex(r"[A-Za-z0-9#]+").desc("field value")
field = seq(field_key, string(":") >> field_value).map(tuple)
passport_end = eof | string_from("\n", "\n\n")


@generate
def passport():
    _fields = {}
    while True:
        fkey, fval = yield field
        _fields[fkey] = fval

        m = yield string_from(" ", "\n").optional()
        if m == "\n":
            n = yield peek(string("\n").optional())
            e = yield peek(eof.result(True).optional())
            if n == "\n" or e:
                break
        elif m is None:
            break

    return _fields


passports = passport.sep_by(string("\n").at_least(1))


def is_valid(p, extra_validation=None):
    valid = all(k in p for k in _essential_keys)

    if not valid:
        return False

    if extra_validation is not None:
        for k, v in p.items():
            if not extra_validation[k](v):
                return False

    return True


with puzzle_input(4, example, False) as f:
    data, remain = passports.parse_partial(f.read())
    print(repr(remain))  # so we can make sure we're not missing data

    print(sum(1 for p in data if is_valid(p)))
    print(sum(1 for p in data if is_valid(p, passport_validation)))
