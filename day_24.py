import abc
import operator as op
import re
from collections import defaultdict, deque
from contextlib import suppress
from dataclasses import dataclass
from functools import reduce
from itertools import chain, count
from os import read
from pprint import pprint
from typing import Awaitable, Deque

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

example = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""


@dataclass(frozen=True)
class HexCubePosition:
    x: int
    y: int
    z: int

    def __add__(self, o):
        return HexCubePosition(
            self.x + o.x,
            self.y + o.y,
            self.z + o.z,
        )


cube_nav = {
    "ne": HexCubePosition(+1, 0, -1),
    "e": HexCubePosition(+1, -1, 0),
    "se": HexCubePosition(0, -1, +1),
    "sw": HexCubePosition(-1, 0, +1),
    "w": HexCubePosition(-1, +1, 0),
    "nw": HexCubePosition(0, +1, -1),
}


def split_nav(s):
    nav_it = iter(s)
    with suppress(StopIteration):
        while True:
            d = next(nav_it)
            if d in "sn":
                d += next(nav_it)
            yield d


def neighbours(t):
    return {t + n for n in cube_nav.values()}


start_pos = HexCubePosition(0, 0, 0)

tiles = set()
with puzzle_input(24, example, False) as data:
    for l in data.read().strip().split("\n"):
        # print(list(split_nav(l.strip())))
        tile = reduce(op.add, [cube_nav[n] for n in split_nav(l.strip())], start_pos)
        if tile in tiles:
            tiles.remove(tile)
        else:
            tiles.add(tile)

print(len(tiles))

for day in range(100):
    tiles_to_check = set(chain.from_iterable(neighbours(t) for t in tiles))
    new_tiles = set()
    for tile in tiles_to_check:
        ns = neighbours(tile)
        black_neighbours = ns & tiles
        # print('checking', tile, tile in tiles, len(ns), len(black_neighbours))
        if tile in tiles:  # is black
            if 0 < len(black_neighbours) <= 2:
                new_tiles.add(tile)
        else:  # is white
            if len(black_neighbours) == 2:
                new_tiles.add(tile)

    print(len(new_tiles))
    tiles = new_tiles
