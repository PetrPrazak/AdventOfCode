# http://adventofcode.com/2016/day/9
from __future__ import print_function


def decompress(line, part=1):
    pos = 0
    end = len(line)
    total = 0
    while pos < end:
        c = line[pos]
        if c == '(':
            posx = line.find('x', pos + 1)
            count = int(line[pos+1:posx])
            pose = line.find(')', posx + 1)
            times = int(line[posx+1:pose])
            pos = pose + 1
            if part == 1:
                total += count * times
            else:
                cutword = line[pos:pos + count]
                total += decompress(cutword, part) * times
            pos += count
        else:
            total += 1
            pos += 1
    return total


def solve(line, part=1):
    print(f"Part {part}:", decompress(line, part))


def test():
    solve("A(2x2)BCD(2x2)EFG")
    solve("X(8x2)(3x3)ABCY")
    solve("(3x3)XYZ",2)
    solve("(27x12)(20x12)(13x14)(7x10)(1x12)A", 2)


def main(file):
    with open(file) as f:
        l = f.read().strip()
        solve(l, 1)
        solve(l, 2)


if __name__ == "__main__":
    main("input.txt")
