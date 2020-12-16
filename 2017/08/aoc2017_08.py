# http://adventofcode.com/2017/day/8
from __future__ import print_function
from collections import defaultdict


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


def solve(lines):
    regs = defaultdict(int)
    maxval = 0
    for line in lines:
        parts = line.strip().split()
        cond = True
        if len(parts) > 3:
            reg = regs[parts[4]]
            op = parts[5]
            val = int(parts[6])
            if op == ">":
                cond = reg > val
            elif op == "<":
                cond = reg < val
            elif op == "==":
                cond = reg == val
            elif op == "!=":
                cond = reg != val
            elif op == ">=":
                cond = reg >= val
            elif op == "<=":
                cond = reg <= val
            else:
                raise InputError(line, "Unknown condition operator")

        if cond:
            reg = parts[0]
            op = parts[1]
            val = int(parts[2])
            regval = regs[reg]
            if op == "inc":
                regval += val
            elif op == "dec":
                regval -= val
            else:
                raise InputError(line, "Unknown operator")
            regs[reg] = regval

            maxval = max(regval, maxval)

    print(max(regs.values()))
    print(maxval)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()
        solve(lines)
