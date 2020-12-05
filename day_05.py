from utils import puzzle_input

example = "\n".join(
    [
        "FBFBBFFRLR",
        "BFFFBBFRRR",
        "FFFBBBFRRR",
        "BBFFBBFRLL",
    ]
)


def parse_seat_id(l):
    return sum(2 ** i for i, v in enumerate(reversed(l)) if v in "BR")


def find_gap(l):
    # return the missing number in a gap
    gaps = [a + 1 for a, b in zip(poss, poss[1:]) if b - a == 2]
    return gaps[0]


with puzzle_input(5, example, False) as f:
    data = [l.strip() for l in f]
    poss = [parse_seat_id(l) for l in data]
    poss.sort()

    # results
    print(poss[-1])
    print(find_gap(poss))
