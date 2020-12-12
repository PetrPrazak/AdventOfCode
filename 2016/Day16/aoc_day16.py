# http://adventofcode.com/2016/day/16
from __future__ import print_function


def next_gen(line):
    return line + "0" + ''.join("0" if c == "1" else "1" for c in reversed(line))


def gen(line, maxlen):
    while True:
        line = next_gen(line)
        if len(line) >= maxlen:
            return line[:maxlen]


def get_checksum(line):
    while len(line) > 1:
        checksum = ''.join("1" if line[i] == line[i+1] else "0"
                           for i in range(0, len(line)-1, 2))
        if len(checksum) % 2 == 1:
            return checksum
        else:
            line = checksum
    return line


def solve(data):
    # part 1
    result = get_checksum(gen(data, 272))
    print("Part 1:", result)
    # part 2
    result = get_checksum(gen(data, 35651584))
    print("Part 2:", result)


def main():
    solve('11011110011011101')


if __name__ == "__main__":
    main()