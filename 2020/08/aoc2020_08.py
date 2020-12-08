# https://adventofcode.com/2020/day/8
from __future__ import print_function


# return accumulator and flag if terminated correctly
def run(data, flip_nop_ip=None):
    ip, acc = 0, 0
    ips = set()
    prog_size = len(data)
    while ip not in ips:
        if ip >= prog_size:
            return acc, True
        ips.add(ip)
        op, val = data[ip]
        if op == "acc":
            acc += val
            ip += 1
        elif op == "nop":
            ip += val if flip_nop_ip == ip else 1
        elif op == "jmp":
            ip += 1 if flip_nop_ip == ip else val
    return acc, False


def patch_and_run(data):
    for pos in range(len(data)):
        if data[pos][0] in ["jmp", "nop"]:
            acc, flag = run(data, pos)
            if flag:
                return acc
    return None


def process(data):
    # pprint(data)
    # part 1
    result = run(data)
    print("part 1:", result[0])
    # part 2
    result = patch_and_run(data)
    print("part 2:", result)


def parse_line(line):
    op, val = line.split()
    return op, int(val)


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
