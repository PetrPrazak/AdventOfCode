# https://adventofcode.com/2016/day/21
from __future__ import print_function
from pathlib import Path
from collections import deque

cat = ''.join


def scramble(data, inp, expected=None, reverse=False, debug=False):
    buf = deque(inp)
    if reverse:
        data = reversed(data)
    out = [cat(buf)]
    for i, (instr, *op) in enumerate(data):
        if debug:
            print(cat(buf), instr, op, end=" ")
        if instr == "swap":
            if op[0] == "letter":
                p1, p2 = buf.index(op[1]), buf.index(op[4])
            elif op[0] == "position":
                p1, p2 = int(op[1]), int(op[4])
            else:
                raise ValueError(instr, op)
            buf[p1], buf[p2] = buf[p2], buf[p1]
        elif instr == "reverse":
            p1, p2 = int(op[1]), int(op[3])
            buf = list(buf) # deque can't do slice insertions
            buf[p1:p2+1] = reversed(buf[p1:p2+1])
            buf = deque(buf)
        elif instr == "rotate":
            if op[0] == "based":
                pos = buf.index(op[5])
                if reverse:
                    # found empirically using *test_rotate*
                    n = [-1, -1, 2, -2, 1, -3, 0, -4][pos]
                else:
                    n = 1 + pos + (pos >= 4)
            else:
                n = int(op[1]) * (1 if op[0] == "right" else -1)
                if reverse:
                    n = -n
            buf.rotate(n)
        elif instr == "move":
            p1, p2 = int(op[1]), int(op[4])
            if reverse:
                p1, p2 = p2, p1
            letter = buf[p1]
            del buf[p1]
            buf.insert(p2, letter)
        else:
            raise ValueError(instr)
        code = cat(buf)
        if debug:
            print(code)
        if expected:
            if code != expected[i+1]:
                raise RuntimeError(f"{code} should be {expected[i+i]}")
        out.append(code)
    return cat(buf), out


def process(data, inp):
    # part 1
    result, expected = scramble(data, inp)
    print("part 1:", result)
    # part 2
    assert result == "ghfacdbe"
    expected=list(reversed(expected))
    assert scramble(data, result, expected, reverse=True)[0] == inp
    result, _ = scramble(data, "fbgdceah", reverse=True)
    print("part 2:", result)


def test_rotate(ll):
    for l in ll:
        pos = ll.index(l)
        n = 1 + pos + (pos >= 4)
        dd = deque(ll)
        dd.rotate(n)
        print(l, dd.index(l), pos, dd)


def load_data(fileobj):
    return [line.strip().split() for line in fileobj.readlines()]


def main(file="input.txt", inp="abcdefgh"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        # test_rotate(inp)
        process(load_data(f), inp)


if __name__ == "__main__":
    # main("test.txt", "abcde")
    main()
