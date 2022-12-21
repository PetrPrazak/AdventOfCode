# https://adventofcode.com/2022/day/21
from pathlib import Path
from operator import mul, add, floordiv, sub
import time

OP = {'*': mul, '+': add, '-': sub, '/': floordiv}
INV_OP = {'*': floordiv, '+': sub, '-': add, '/': mul}


def eval_monkeys(data):
    def monkey(m):
        args = data[m]
        if isinstance(args, int):
            return args
        else:
            return OP[args[1]](monkey(args[0]), monkey(args[2]))
    return monkey("root")


def reduce_monkeys(data):
    def monkey(m):
        args = data[m]
        if not isinstance(args, tuple):
            return args
        else:
            m1, m2 = monkey(args[0]), monkey(args[2])
            if isinstance(m1, int) and isinstance(m2, int):
                return OP[args[1]](m1, m2)
            else:
                return m1, args[1], m2
    data["humn"] = 'X'
    root_op = data["root"]
    left = monkey(root_op[0])
    right = monkey(root_op[2])
    return left, right


def solve(left, right):
    if isinstance(left, int):
        left, right = right, left
    while isinstance(left, tuple):
        arg1, op, arg2 = left
        if isinstance(arg2, int):
            left = arg1
            right = INV_OP[op](right, arg2)
        else:
            # '-' and '/' are not commutative!
            left = arg2
            if op == '-':
                right = arg1 - right
            elif op == '/':
                right = arg1 // right
            else:
                right = INV_OP[op](right, arg1)
    return right


def process(data):
    # part 1
    result = eval_monkeys(data)
    print("part 1:", result)
    # part 2
    result = solve(*reduce_monkeys(data))
    print("part 2:", result)


def parse_line(line):
    left, expr = line.split(': ')
    return left, int(expr) if expr[0].isdigit() else tuple(expr.split(' '))


def load_data(fileobj):
    return dict(parse_line(line.rstrip()) for line in fileobj.readlines())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    main("test.txt")
    main()
