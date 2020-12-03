import timeit
from functools import partial

from utils import puzzle_input

with puzzle_input(2) as f:
    data = [l.strip() for l in f.readlines()]


def parse_password(l: str):
    rule, password = l.split(":")
    password = password.strip()
    counts, char = rule.split(" ")
    lower, upper = counts.split("-")
    upper = int(upper)
    lower = int(lower)
    return (char, (lower, upper)), password


def validate_password_sled(rule, password: str):
    char, (lower, upper) = rule
    chars = password.count(char)
    valid = lower <= chars <= upper
    return valid


def validate_password_toboggan(rule, password: str):
    char, (lower, upper) = rule
    valid = (password[lower - 1] == char) ^ (password[upper - 1] == char)
    return valid


parsed_data = [parse_password(l.strip()) for l in data]

print(sum(1 for p in parsed_data if validate_password_sled(*p)))
print(sum(1 for p in parsed_data if validate_password_toboggan(*p)))
