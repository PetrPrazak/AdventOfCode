# http://adventofcode.com/2017/day/25
from __future__ import print_function
from collections import defaultdict
from time import time

# A = 0, B = 1...
# (next_state, new val, direction)
states = [[(1, 1, 1), (1, 0, -1)],
          [(2, 1, -1), (4, 0, 1)],
          [(4, 1, 1), (3, 0, -1)],
          [(0, 1, -1), (0, 1, -1)],
          [(0, 0, 1), (5, 0, 1)],
          [(4, 1, 1), (0, 1, 1)]]


def solve():
    tape = defaultdict(int)
    state = 0  # 'A'
    pos = 0
    for _ in range(12861455):
        val = tape[pos]
        state, val, off = states[state][val]
        tape[pos] = val
        pos += off

    checksum = 0
    for i in tape.values():
        checksum += i

    print(checksum, len(tape))


def main():
    start = time()
    solve()
    end = time()
    print("Solved in {:.4f} s".format(end - start))


if __name__ == "__main__":
    main()
