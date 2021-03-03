import abc
import operator as op
import re
import sys
from collections import defaultdict, deque
from functools import reduce
from itertools import chain
from pprint import pprint
from typing import Dict, Optional

import numpy as np

from utils import puzzle_input

example = "\n".join(
    [
        "Tile 2311:",
        "..##.#..#.",
        "##..#.....",
        "#...##..#.",
        "####.#...#",
        "##.##.###.",
        "##...#.###",
        ".#.#.#..##",
        "..#....#..",
        "###...#.#.",
        "..###..###",
        "",
        "Tile 1951:",
        "#.##...##.",
        "#.####...#",
        ".....#..##",
        "#...######",
        ".##.#....#",
        ".###.#####",
        "###.##.##.",
        ".###....#.",
        "..#.#..#.#",
        "#...##.#..",
        "",
        "Tile 1171:",
        "####...##.",
        "#..##.#..#",
        "##.#..#.#.",
        ".###.####.",
        "..###.####",
        ".##....##.",
        ".#...####.",
        "#.##.####.",
        "####..#...",
        ".....##...",
        "",
        "Tile 1427:",
        "###.##.#..",
        ".#..#.##..",
        ".#.##.#..#",
        "#.#.#.##.#",
        "....#...##",
        "...##..##.",
        "...#.#####",
        ".#.####.#.",
        "..#..###.#",
        "..##.#..#.",
        "",
        "Tile 1489:",
        "##.#.#....",
        "..##...#..",
        ".##..##...",
        "..#...#...",
        "#####...#.",
        "#..#.#.#.#",
        "...#.#.#..",
        "##.#...##.",
        "..##.##.##",
        "###.##.#..",
        "",
        "Tile 2473:",
        "#....####.",
        "#..#.##...",
        "#.##..#...",
        "######.#.#",
        ".#...#.#.#",
        ".#########",
        ".###.#..#.",
        "########.#",
        "##...##.#.",
        "..###.#.#.",
        "",
        "Tile 2971:",
        "..#.#....#",
        "#...###...",
        "#.#.###...",
        "##.##..#..",
        ".#####..##",
        ".#..####.#",
        "#..#.#..#.",
        "..####.###",
        "..#.#.###.",
        "...#.#.#.#",
        "",
        "Tile 2729:",
        "...#.#.#.#",
        "####.#....",
        "..#.#.....",
        "....#..#.#",
        ".##..##.#.",
        ".#.####...",
        "####.#.#..",
        "##.####...",
        "##..#.##..",
        "#.##...##.",
        "",
        "Tile 3079:",
        "#.#.#####.",
        ".#..######",
        "..#.......",
        "######....",
        "####.#..#.",
        ".#...#.##.",
        "#.#####.##",
        "..#.###...",
        "..#.......",
        "..#.###...",
    ]
)

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3

opposite = {
    TOP: BOTTOM,
    BOTTOM: TOP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

rot_map = {
    (TOP, TOP): 0,
    (TOP, BOTTOM): 2,
    (TOP, LEFT): 1,
    (TOP, RIGHT): 3,
    (BOTTOM, TOP): 2,
    (BOTTOM, BOTTOM): 0,
    (BOTTOM, LEFT): 3,
    (BOTTOM, RIGHT): 1,
    (LEFT, TOP): 3,
    (LEFT, BOTTOM): 1,
    (LEFT, LEFT): 0,
    (LEFT, RIGHT): 2,
    (RIGHT, TOP): 1,
    (RIGHT, BOTTOM): 3,
    (RIGHT, LEFT): 2,
    (RIGHT, RIGHT): 0,
}
sea_monster_data = np.array(
    [
        list("                  # "),
        list("#    ##    ##    ###"),
        list(" #  #  #  #  #  #   "),
    ]
)

sea_monster_mask = sea_monster_data != "#"
sea_monster = np.ma.masked_array(sea_monster_data, mask=sea_monster_mask)


def edge_marker(s):
    f = sum(2 ** i for i, c in enumerate(s) if c == "#")
    b = sum(2 ** i for i, c in enumerate(reversed(s)) if c == "#")

    if f < b:
        return f
    else:
        return b


class Tile:
    def __init__(self, id, img):
        self._id = id
        self._img = np.array(
            [[c for c in r] for r in img]
        )  # ([[c == '#' for c in r] for r in img])
        self._edge_markers = [
            self.get_marker(TOP),
            self.get_marker(BOTTOM),
            self.get_marker(LEFT),
            self.get_marker(RIGHT),
        ]

        self.neighbours = set()
        self.neighbours_pos = [None, None, None, None]
        self.pos = None

    def rotate_marker_to(self, marker, dir):
        marker_dir = self._edge_markers.index(marker)
        for i in range(rot_map[(marker_dir, dir)]):
            self.rotate_ccw()

    def rotate_ccw(self):
        self._img = np.rot90(self._img)
        t, b, l, r = self._edge_markers
        self._edge_markers = [r, l, t, b]

    def flip_horizontally(self):
        self._img = np.flip(self._img, axis=0)
        t, b, l, r = self._edge_markers
        self._edge_markers = [b, t, l, r]

    def flip_vertically(self):
        self._img = np.flip(self._img, axis=1)
        t, b, l, r = self._edge_markers
        self._edge_markers = [t, b, r, l]

    def get_edge(self, edge):
        if edge == TOP:
            return self._img[0]
        elif edge == BOTTOM:
            return self._img[-1]
        elif edge == LEFT:
            return self._img[:, 0]
        elif edge == RIGHT:
            return self._img[:, -1]

    def get_marker(self, edge):
        return edge_marker(self.get_edge(edge))

    def print(self):
        print(self._img)

    def trimmed(self):
        return self._img[1:-1, 1:-1]


with puzzle_input(20, example, False) as f:
    tile_defs = f.read().strip().split("\n\n")

    tiles: Dict[int, Tile] = {}
    edges = defaultdict(set)

    for tile_def in tile_defs:
        lines = tile_def.split("\n")
        tile_id = int(lines[0].split()[1][:-1])
        img = lines[1:]

        tileobj = Tile(tile_id, img)
        tiles[tile_id] = Tile(tile_id, img)

    for tile_id, tile in tiles.items():
        for e in tile._edge_markers:
            edges[e].add(tile_id)

    for edge, edge_tiles in edges.items():
        if len(edge_tiles) == 2:
            t1, t2 = edge_tiles
            tiles[t1].neighbours.add(t2)
            tiles[t2].neighbours.add(t1)

    # find tiles with 2 neighbors:
    corners = [tile_id for tile_id, tile in tiles.items() if len(tile.neighbours) == 2]
    print(reduce(op.mul, corners))  # Part 1

    corner_tile_id = 1171
    # tiles[1171].flip_vertically()
    tiles[corner_tile_id].pos = (0, 0)

    tiles_to_visit = deque([tiles[corner_tile_id]])
    seen = set()

    def neighbour_from_edge(marker, tile_id) -> Optional[Tile]:
        neighbour_set = edges[marker] - {tile_id}
        if neighbour_set:
            return tiles[neighbour_set.pop()]
        else:
            return None

    while tiles_to_visit:
        tile = tiles_to_visit.popleft()
        tile_id = tile._id
        seen.add(tile)

        # Check top
        marker = tile.get_marker(TOP)
        neighbour = neighbour_from_edge(marker, tile_id)
        if neighbour is not None and neighbour not in seen:
            neighbour.rotate_marker_to(marker, BOTTOM)
            if any(tile.get_edge(TOP) != neighbour.get_edge(BOTTOM)):
                neighbour.flip_vertically()
            x, y = tile.pos
            neighbour.pos = (x, y - 1)
            tiles_to_visit.append(neighbour)

        # Check bottom
        marker = tile.get_marker(BOTTOM)
        neighbour = neighbour_from_edge(marker, tile_id)
        if neighbour is not None and neighbour not in seen:
            neighbour.rotate_marker_to(marker, TOP)

            if any(tile.get_edge(BOTTOM) != neighbour.get_edge(TOP)):
                neighbour.flip_vertically()

            x, y = tile.pos
            neighbour.pos = (x, y + 1)
            tiles_to_visit.append(neighbour)

        # Check left
        marker = tile.get_marker(LEFT)
        neighbour = neighbour_from_edge(marker, tile_id)
        if neighbour is not None and neighbour not in seen:
            neighbour.rotate_marker_to(marker, RIGHT)

            if any(tile.get_edge(LEFT) != neighbour.get_edge(RIGHT)):
                neighbour.flip_horizontally()

            x, y = tile.pos
            neighbour.pos = (x - 1, y)
            tiles_to_visit.append(neighbour)

        # Check right
        marker = tile.get_marker(RIGHT)
        neighbour = neighbour_from_edge(marker, tile_id)
        if neighbour is not None and neighbour not in seen:
            neighbour.rotate_marker_to(marker, LEFT)

            if any(tile.get_edge(RIGHT) != neighbour.get_edge(LEFT)):
                neighbour.flip_horizontally()

            x, y = tile.pos
            neighbour.pos = (x + 1, y)
            tiles_to_visit.append(neighbour)

    n = 12
    tl_x = min(tile.pos[0] for tile in tiles.values())
    tl_y = min(tile.pos[1] for tile in tiles.values())
    print(tl_x, tl_y)

    # renumber tiles
    for tile in tiles.values():
        x, y = tile.pos
        pos = x - tl_x, y - tl_y
        tile.pos = pos
        print(tile._id, tile.pos)

    tiles_pos = {tile.pos: tile for tile in tiles.values()}
    big_rows = [
        np.concatenate([tiles_pos[(i, r)].trimmed() for i in range(n)], axis=1)
        for r in range(n)
    ]
    big_img = np.concatenate(big_rows, axis=0)

    big_img = np.rot90(big_img)
    big_img = np.flip(big_img, axis=0)

    for r in big_img:
        print("".join(r))

    def print_array(na):
        for r in na:
            print("".join(r))

    def look_for_monsters(big_img):
        monsters = 0
        for r in range(n * 8 - 2):
            for c in range(n * 8 - 19):
                if (big_img[r : r + 3, c : c + 20] == sea_monster).all():
                    print("found monster!")
                    monsters += 1
                    for i in range(3):
                        for j in range(20):
                            if sea_monster[i, j]:
                                big_img[r + i, c + j] = "O"
        return monsters

    action = [None] + [np.rot90] * 3 + [np.flipud] + [np.rot90] * 3

    for act in action:
        if act is not None:
            big_img = act(big_img)

        m = look_for_monsters(big_img)
        if m:
            print("doner here")
            print(np.unique(big_img, return_counts=True))
            break
