import operator as op
from functools import reduce

from utils import puzzle_input

example = "\n".join(
    [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]
)


with puzzle_input(3, example) as f:
    data = [list(l.strip()) for l in f.readlines()]


def slide(slope, direction, pos=(0, 0)):
    width = len(slope[0])
    trees = 0
    r, c = pos
    r_step, c_step = direction

    while r < len(slope):
        if slope[r][c] == "#":
            trees += 1

        r += r_step
        c = (c + c_step) % width
    return trees


print("trees:", slide(data, (1, 3)))

slopes = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1),
]

print("trees", reduce(op.mul, (slide(data, d) for d in slopes)))
