"""
http://adventofcode.com/2017/day/8

--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
These instructions would be processed as follows:

Because a starts at 0, it is not greater than 1, and so b is not modified.
a is increased by 1 (to 1) because b is less than 5 (it is 0).
c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
c is increased by -20 (to -10) because c is equal to 10.
After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

Your puzzle answer was 2971.

--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much memory to allocate to these operations. For example, in the above instructions, the highest value ever held was 10 (in register c after the third instruction was evaluated).

Your puzzle answer was 4254.

Both parts of this puzzle are complete! They provide two gold stars: **

"""
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
            if op == ">":    cond = reg > val
            elif op == "<":  cond = reg < val
            elif op == "==": cond = reg == val
            elif op == "!=": cond = reg != val
            elif op == ">=": cond = reg >= val
            elif op == "<=": cond = reg <= val
            else:
                raise InputError(line, "Unknown condition operator")

        if cond:
            reg = parts[0]
            op = parts[1]
            val = int(parts[2])
            regval = regs[reg]
            if op == "inc":    regval += val
            elif op == "dec":  regval -= val
            else:
                raise InputError(line, "Unknown operator")
            regs[reg] = regval

            maxval = max(regval, maxval)

    print(max(regs.values()))
    print(maxval)


INPUT = "aoc_day8_input.txt"
# INPUT = "aoc_day8_input_test.txt"


if __name__ == "__main__":
    with open(INPUT) as f:
        lines = f.readlines()
        solve(lines)
