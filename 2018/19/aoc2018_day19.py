# https://adventofcode.com/2018/day/19

from __future__ import print_function
import re

INPUT = "aoc2018_day19.txt"
# INPUT = "test.txt"

# from day 16


def addr(regs, r1, r2, r3): regs[r3] = regs[r1] + regs[r2]


def addi(regs, r1, i, r3): regs[r3] = regs[r1] + i


def mulr(regs, r1, r2, r3): regs[r3] = regs[r1] * regs[r2]


def muli(regs, r1, i, r3): regs[r3] = regs[r1] * i


def banr(regs, r1, r2, r3): regs[r3] = regs[r1] & regs[r2]


def bani(regs, r1, i, r3): regs[r3] = regs[r1] & i


def borr(regs, r1, r2, r3): regs[r3] = regs[r1] | regs[r2]


def bori(regs, r1, i, r3): regs[r3] = regs[r1] | i


def setr(regs, r1, r2, r3): regs[r3] = regs[r1]


def seti(regs, i1, i, r3): regs[r3] = i1


def gtir(regs, i, r2, r3): regs[r3] = 1 if i > regs[r2] else 0


def gtri(regs, r1, i, r3): regs[r3] = 1 if regs[r1] > i else 0


def gtrr(regs, r1, r2, r3): regs[r3] = 1 if regs[r1] > regs[r2] else 0


def eqir(regs, i, r2, r3): regs[r3] = 1 if i == regs[r2] else 0


def eqri(regs, r1, i, r3): regs[r3] = 1 if regs[r1] == i else 0


def eqrr(regs, r1, r2, r3): regs[r3] = 1 if regs[r1] == regs[r2] else 0


instruction_set = {"addr": addr, "addi": addi,
                   "mulr": mulr, "muli": muli,
                   "banr": banr, "bani": bani,
                   "borr": borr, "bori": bori,
                   "setr": setr, "seti": seti,
                   "gtir": gtir, "gtri": gtri, "gtrr": gtrr,
                   "eqir": eqir, "eqri": eqri, "eqrr": eqrr}


def get_numbers(s):
    return list(map(int, re.findall(r"(\d+)", s)))


def run(ip_reg, program, regs):
    while 0 <= regs[ip_reg] < len(data):
        line = program[regs[ip_reg]]
        instr = line.split(' ')[0]
        args = get_numbers(line)
        instruction_set[instr](regs, *args)
        regs[ip_reg] += 1


def process(data):
    ip_reg = 0
    if data[0].startswith("#ip"):
        ip_reg = get_numbers(data[0])[0]
        del data[0]

    # part 1
    regs = [0] * 6
    run(ip_reg, data, regs)
    print(regs[0])

    # part 2 - impossible to run - 10^14 cycles !
    regs = [0] * 6
    regs[0] = 1
    run(ip_reg, data, regs)
    print(regs[0])


def main1():
    with open(INPUT) as f:
        data = [l.rstrip() for l in f.readlines()]
        process(data)


def program(A):
    D = 861
    if A == 1:
        D += 10550400
    A = 0
    for E in range(1, D + 1):
        if D % E == 0:
            A += E
    return A


def main2():
    print(program(0))
    print(program(1))


if __name__ == "__main__":
    main2()

"""
 Program analysis:
 
#ip 1
 regs = [1,0,0,0,0,0]

 0 addi 1 16 1  # ip = ip + 16 -> jmp 17
 1 seti 1 1 5   # r5 = 1
 2 seti 1 4 2   # r2 = 1
 3 mulr 5 2 3   # r3 = r5 * r2
 4 eqrr 3 4 3   # r3 = r3 == r4 [r3 = 0/1]
 5 addr 3 1 1   # ip = r3 + r1 -> if r3 == 0: jmp 6; else: jmp 7
 6 addi 1 1 1   # ip = ip + 1 -> jmp 8
 7 addr 5 0 0   # r0 += r5
 8 addi 2 1 2   # r2 += 1
 9 gtrr 2 4 3   # r3 = r2 > r4
10 addr 1 3 1   # ip = ip + r3 -> if r3 == 0: jmp 11; else: jmp 12
11 seti 2 7 1   # ip = 2 -> jmp 3
12 addi 5 1 5   # r5 += 1
13 gtrr 5 4 3   # r3 = r5 > r4
14 addr 3 1 1   # ip = ip + r3 -> if r3 == 0: jmp 15; else: jmp 16
15 seti 1 8 1   # ip = 1 -> jmp 2 
16 mulr 1 1 1   # ip == 16 -> ip = 256 -> exit
17 addi 4 2 4   # r4 += 2
18 mulr 4 4 4   # r4 *= r4
19 mulr 1 4 4   # r4 *= 19
20 muli 4 11 4  # r4 *= 11
21 addi 3 1 3   # r3 += 1
22 mulr 3 1 3   # r3 *= ip -> r3 *= 22
23 addi 3 3 3   # r3 += 3
24 addr 4 3 4   # r4 += r3
25 addr 1 0 1   # ip += r0 -> jmp r0 + 26
26 seti 0 3 1   # ip = r0 + 3 -> jmp r0 + 4
27 setr 1 1 3   # r3 = ip -> r3 = 27
28 mulr 3 1 3   # r3 *= ip -> r3 *= 28
29 addr 1 3 3   # r3 += ip -> r3 += 29
30 mulr 1 3 3   # r3 *= ip -> r3 *= 30
31 muli 3 14 3  # r3 *= 14
32 mulr 3 1 3   # r3 *= ip -> r3 *= 32
33 addr 4 3 4   # r4 += r3
34 seti 0 9 0   # r0 = 0
35 seti 0 4 1   # ip = 0 -> jmp 1


        A   B C D E
regs = [1,0,0,0,0,0]

D = 861
if A == 1: 
    D += 10551261
A = 0
for E in range(1,D+1):
    for B in range(1,D+1):
        C = E * B
        if C == D:
            A += E

"""
