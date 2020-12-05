# http://adventofcode.com/2015/day/9
from __future__ import print_function


def look_and_say(seq):
    s = ""
    idx = 0
    end = len(seq)
    while idx < end:
        cnt = 1
        digit = seq[idx]
        idx += 1
        while idx < end and seq[idx] == digit:
            cnt += 1
            idx += 1
        s += f"{cnt}{digit}"
    return s


def process(seq):
    # part 1
    print(seq)
    s = seq
    for _ in range(40):
        s = look_and_say(s)
    print("Part 1:", len(s))
    s = seq
    for _ in range(50):
        s = look_and_say(s)
    print("Part 2:", len(s))


def test():
    process("111221")


def main():
    process("1113222113")


if __name__ == "__main__":
    # test()
    main()
