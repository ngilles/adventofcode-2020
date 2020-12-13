from utils import puzzle_input

example = "\n".join(
    [
        "F10",
        "N3",
        "F7",
        "R90",
        "F11",
    ]
)


with puzzle_input(12, example, False) as f:
    data = [e for e in f.read().split()]

    heading = 90
    dirs = {
        0: (0, -1),
        90: (1, 0),
        180: (0, 1),
        270: (-1, 0),
    }
    pos = 0, 0
    p2pos = 0, 0
    waypoint = 10, -1

    for l in data:
        cmd, value = l[0], int(l[1:])

        if cmd == "N":
            pos = pos[0], pos[1] - value
            waypoint = waypoint[0], waypoint[1] - value
        elif cmd == "S":
            pos = pos[0], pos[1] + value
            waypoint = waypoint[0], waypoint[1] + value
        elif cmd == "W":
            pos = pos[0] - value, pos[1]
            waypoint = waypoint[0] - value, waypoint[1]
        elif cmd == "E":
            pos = pos[0] + value, pos[1]
            waypoint = waypoint[0] + value, waypoint[1]
        elif cmd == "F":
            pos = pos[0] + dirs[heading][0] * value, pos[1] + dirs[heading][1] * value
            p2pos = p2pos[0] + waypoint[0] * value, p2pos[1] + waypoint[1] * value
        elif cmd == "R":
            heading = (heading + value) % 360
            for i in range(value // 90):
                waypoint = -waypoint[1], waypoint[0]
        elif cmd == "L":
            heading = (heading - value) % 360
            for i in range(value // 90):
                waypoint = waypoint[1], -waypoint[0]

    print(pos[0], pos[1], (abs(pos[0]) + abs(pos[1])))
    print(p2pos[0], p2pos[1], (abs(p2pos[0]) + abs(p2pos[1])))
