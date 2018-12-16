# https://adventofcode.com/2018/day/13

from __future__ import print_function

INPUT = "aoc2018_day13.txt"
# INPUT = "test2.txt"

cat = ''.join

cart_init = {
    'v': (2, '|'),
    '^': (0, '|'),
    '<': (3, '-'),
    '>': (1, '-')
}

next_position = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0)
}


def make_turn(orient, turn):
    orient = (orient + [3, 0, 1][turn]) % 4
    turn = (turn + 1) % 3
    return orient, turn


def stay(orient, turn):
    return orient, turn


def turn_left(orient, turn):
    return (orient + 3) % 4, turn


def turn_right(orient, turn):
    return (orient + 1) % 4, turn


movement_rules = {
    (0, '|'): stay, (0, '/'): turn_right, (0, '\\'): turn_left, (0, '+'): make_turn,
    (1, '-'): stay, (1, '\\'): turn_right, (1, '/'): turn_left, (1, '+'): make_turn,
    (2, '|'): stay, (2, '/'): turn_right, (2, '\\'): turn_left, (2, '+'): make_turn,
    (3, '-'): stay, (3, '\\'): turn_right, (3, '/'): turn_left, (3, '+'): make_turn,
}


def init_carts(track):
    init_cart_positions = {}
    for y, row in enumerate(track):
        for x, c in enumerate(row):
            if c in cart_init:
                orient, replace = cart_init[c]
                row[x] = replace
                init_cart_positions[(y, x)] = (orient, 0)
    return init_cart_positions


def move_carts(track, cart_positions, part):
    new_positions = cart_positions.copy()
    collided = False

    carts = sorted(cart_positions.keys())
    for y, x in carts:
        if (y, x) not in new_positions:
            # cart was already removed in crash
            continue
        orient, turn = cart_positions[(y, x)]
        dx, dy = next_position[orient]
        newx, newy = x + dx, y + dy
        # cart will move so remove it at current position
        del new_positions[(y, x)]
        if (newy, newx) in new_positions:
            print("Collision at %d,%d" % (newx, newy))
            # part 1
            if part == 1:
                collided = True
                break
            else:
                # part 2
                del new_positions[(newy, newx)]
                continue

        path = track[newy][newx]
        movement = movement_rules[(orient, path)]
        # add cart at new position
        new_positions[(newy, newx)] = movement(orient, turn)

    return new_positions, collided


def process(track):
    init_cart_positions = init_carts(track)
    for part in range(1, 3):
        print("# Part", part)
        cart_positions = init_cart_positions
        collided = False
        it = 0
        while not collided:
            it += 1
            cart_positions, collided = move_carts(track, cart_positions, part)
            if len(cart_positions) < 2:
                print(cart_positions)
                break


with open(INPUT) as f:
    data = [list(l.rstrip()) for l in f.readlines()]
    process(data)
