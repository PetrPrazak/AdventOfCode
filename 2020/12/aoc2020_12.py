# https://adventofcode.com/2020/day/12
from __future__ import print_function

# N E S W
orientations = list("NESW")
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
# 0, R, RR, RRR==L
rotations = [(1, 1), (-1, 1), (-1, -1), (1, -1)]


def distance(x, y):
    return abs(x) + abs(y)


def move_pos(pos, value, dx, dy):
    x, y = pos
    return x + dx * value, y + dy * value


def rotate(order, value, bearing=0):
    if order == 'L':
        value = -value
    turn = value // 90
    return (bearing + turn) % 4


def move_ship(orders):
    bearing = 1  # east
    pos = 0, 0
    for order, value in orders:
        if order in ['R', 'L']:
            bearing = rotate(order, value, bearing)
        elif order == 'F':
            pos = move_pos(pos, value, *directions[bearing])
        else:
            pos = move_pos(pos, value, *directions[orientations.index(order)])
    return distance(*pos)


def rotate_waypoint(waypoint, turn):
    signx, signy = rotations[turn]
    x, y = waypoint
    if turn % 2 == 0:
        return x * signx, y * signy
    else:
        return y * signy, x * signx


def move_ship_waypoint(orders):
    shippos = 0, 0
    waypoint = 10, 1   # offset to the ship
    for order, value in orders:
        if order in ['R', 'L']:
            turn = rotate(order, value)
            waypoint = rotate_waypoint(waypoint, turn)
        elif order == 'F':
            shippos = move_pos(shippos, value, *waypoint)
        else:
            waypoint = move_pos(waypoint, value,
                                *directions[orientations.index(order)])
    return distance(*shippos)


def process(data):
    # part 1
    result = move_ship(data)
    print("part 1:", result)
    # part 2
    result = move_ship_waypoint(data)
    print("part 2:", result)


def parse_line(line):
    order = line[0]
    value = int(line[1:])
    return order, value


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
