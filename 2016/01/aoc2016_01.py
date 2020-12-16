# https://adventofcode.com/2015/day/1
from __future__ import print_function

# 0 North 1 East 2 South 3 West
directions = [
    # direction, dif_x, dif_y
    (0, 0, 1),
    (1, 1, 0),
    (2, 0, -1),
    (3, -1, 0)
]


def get_new_dir(is_right, direction):
    return directions[(direction + (1 if is_right else -1)) % 4][0]


def get_new_pos(pos, direction, steps):
    x, y = pos
    _, difx, dify = directions[direction]
    return x + difx * steps, y + dify * steps


def distance(x, y):
    return abs(x) + abs(y)


def get_all_new_pos(pos, direction, steps):
    return [get_new_pos(pos, direction, step) for step in range(1, steps+1)]


def solve(codes, part):
    direction = 0
    visits = {}
    pos = 0, 0
    count = 0
    visits[pos] = count
    for code in codes:
        is_right, steps = code
        direction = get_new_dir(is_right, direction)
        if part == 1:
            pos = get_new_pos(pos, direction, steps)
        else:
            count += 1
            listpos = get_all_new_pos(pos, direction, steps)
            for apos in listpos:
                if apos in visits:
                    print("Been here before:", apos)
                    print("Distance to center:", distance(*apos))
                    return
                visits[apos] = count
            pos = listpos[-1]
    print("Distance to center:", distance(*pos))


def main(file):
    with open(file) as f:
        codes = [(code[0] == 'R', int(code[1:]))
                 for code in f.readline().strip().split(', ')]
        solve(codes, 1)
        solve(codes, 2)


if __name__ == "__main__":
    main("input.txt")
