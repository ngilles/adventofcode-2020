import abc
import operator as op
import re
from collections import defaultdict, deque
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

example = ""


def play_game(player1: Deque, player2: Deque):
    for turn in count():
        print(player1)
        print(player2)
        print()

        if len(player1) == 0 or len(player2) == 0:
            winning_player = player1 if len(player2) == 0 else player2
            winning_hand = player1 if len(player2) == 0 else player2
            score = sum((i + 1) * c for i, c in enumerate(reversed(winning)))
            return turn, winning_player, winning_hand, score

        p1 = player1.popleft()
        p2 = player2.popleft()

        if p1 > p2:
            player1.append(p1)
            player1.append(p2)
        else:
            player2.append(p2)
            player2.append(p1)


def play_recursive_game(player1: Deque, player2: Deque, game=count(1)):
    seen_games = set()
    game_num = next(game)
    print(f"=== Game {game_num} ===")

    for turn in count(1):
        cg = (tuple(player1), tuple(player2))
        if cg in seen_games:
            return turn, 1, player1, 0

        seen_games.add(cg)

        print(f"-- Round {turn} (Game {game_num}) --")
        print(player1)
        print(player2)

        p1 = player1.popleft()
        p2 = player2.popleft()

        if len(player1) >= p1 and len(player2) >= p2:
            print("Playing sub-game to determing winner...")
            # recurse
            sub_p1 = player1.copy()
            sub_p2 = player2.copy()

            while len(sub_p1) > p1:
                sub_p1.pop()

            while len(sub_p2) > p2:
                sub_p2.pop()

            _, winner, _, _ = play_recursive_game(sub_p1, sub_p2, game)
        else:
            if p1 > p2:
                winner = 1
            else:
                winner = 2

        print(f"Player {winner} wins round {turn} of {game_num}")
        if winner == 1:
            player1.append(p1)
            player1.append(p2)
        else:
            player2.append(p2)
            player2.append(p1)

        if len(player1) == 0 or len(player2) == 0:
            winning_player = 1 if len(player2) == 0 else 2
            winning_hand = player1 if len(player2) == 0 else player2
            score = sum((i + 1) * c for i, c in enumerate(reversed(winning_hand)))
            return turn, winning_player, winning_hand, score

        print()


with puzzle_input(21, example, False) as f:
    player1 = deque(
        [
            31,
            33,
            27,
            43,
            29,
            25,
            36,
            11,
            15,
            5,
            14,
            34,
            7,
            18,
            26,
            41,
            19,
            45,
            12,
            1,
            8,
            35,
            44,
            30,
            50,
        ]
    )

    player2 = deque(
        [
            42,
            40,
            6,
            17,
            3,
            16,
            22,
            23,
            32,
            21,
            24,
            46,
            49,
            48,
            38,
            47,
            13,
            9,
            39,
            20,
            10,
            2,
            37,
            28,
            4,
        ]
    )

    # player1 = deque([9,2,6,3,1])
    # player2 = deque([5,8,4,7,10])

    print(play_recursive_game(deque(player1), deque(player2)))
