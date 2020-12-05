# http://adventofcode.com/2015/day/8
from __future__ import print_function


def is_hex_char(s):
    return s.isdigit() or s in 'abcdef'


def unescape(line):
    s = ""
    iterline = iter(line)
    for c in iterline:
        if c == '\\':
            c = next(iterline)
            if c == 'x':
                h1 = next(iterline)
                h2 = next(iterline)
                if is_hex_char(h1) and is_hex_char(h2):
                    c = chr(int(h1+h2, 16))
                else:
                    s += "\\x" + h1 + h2
                    continue
        s += c
    if s[0] == '"':
        s = s[1:]
    if s[-1] == '"':
        s = s[:-1]
    return s


def escape(line):
    s = '"'
    for c in line:
        if c in '\\"':
            s += '\\'
        s += c
    s += '"'
    return s


def process(data):
    # part 1
    total = sum(len(d) for d in data)
    unquoted = sum(len(unescape(line)) for line in data)
    # print(total, unquoted)
    print("part 1", total - unquoted)
    # part 2
    quoted = sum(len(escape(line)) for line in data)
    # print(total, quoted)
    print("part 2", quoted - total)


def load_data(fileobj):
    data = [line.strip() for line in fileobj]
    return data


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
