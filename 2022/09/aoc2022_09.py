# https://adventofcode.com/2022/day/9
from pathlib import Path


def sign(num):
    if num > 1:
        return 1
    if num < 1:
        return -1
    return 0


def move_tail(head, tail):
    dif = head - tail
    off_x, off_y = abs(dif.real), abs(dif.imag)
    if off_x < 2 and off_y < 2:
        return tail
    if off_x > 0:
        off_x -= 1
    if off_y > 0:
        off_y -= 1
    return complex(head.real - sign(dif.real) * off_x, head.imag - sign(dif.imag) * off_y)


def process_moves(data, size):
    directions = {'U': -1j, 'D': 1j, 'R': 1+0j, 'L': -1+0j}
    rope = [0j] * size
    tails = {rope[size-1]}
    for dir, amount in data:
        for _ in range(amount):
            rope[0] += directions[dir]
            for pos in range(size-1):
                rope[pos+1] = move_tail(rope[pos], rope[pos+1])
            tails.add(rope[size-1])
    return len(tails)


def process(data):
    # part 1
    result = process_moves(data, 2)
    print("part 1:", result)
    # part 2
    result = process_moves(data, 10)
    print("part 2:", result)


def parse_line(line):
    dir, amount = line.split()
    return dir, int(amount)


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    # main("test2.txt")
    main()
