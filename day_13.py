import time

from utils import puzzle_input

example = "\n".join(
    [
        "939",
        "7,13,x,x,59,x,31,19",
        #'17,x,13,19',
        #'67,7,59,61',
        #'67,x,7,59,61',
        #'67,7,x,59,61',
        #'1789,37,47,1889',
    ]
)


with puzzle_input(13, example, False) as f:
    ts = int(f.readline().strip())
    data = [int(e) if e != "x" else None for e in f.readline().strip().split(",")]

    buses = [e for e in data if e is not None]
    mods = [ts % bus for bus in buses]
    wait = [bus - mod for bus, mod in zip(buses, mods)]

    min_wait = min(wait)
    bus_idx = wait.index(min_wait)
    bus = buses[bus_idx]
    print(bus * min_wait)  # Part 1

    # Part 2
    # Tried to make a smart guess, turns out I implemented a solution
    # to the chinese remainder theorem... looks like there are better
    # solutions
    remainders = [(bus - i) % bus for i, bus in enumerate(data) if bus is not None]
    print(remainders)
    s = buses[0]
    i = 1
    c = 0
    while i < len(buses):
        if c % buses[i] == remainders[i]:
            s *= buses[i]
            i += 1
        c += s
    print(c - s)
