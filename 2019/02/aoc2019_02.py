# https://adventofcode.com/2019/day/02

from __future__ import print_function

INPUT = "aoc2019_02_input.txt"


def intcode_processor(mem):
    pc = 0
    while True:
        # print(mem)
        opcode = mem[pc]
        if opcode == 1:  # ADD
            op1, op2, res = mem[pc + 1], mem[pc + 2], mem[pc + 3]
            mem[res] = mem[op1] + mem[op2]
            pc += 4
        elif opcode == 2:  # MUL
            op1, op2, res = mem[pc + 1], mem[pc + 2], mem[pc + 3]
            mem[res] = mem[op1] * mem[op2]
            pc += 4
        elif opcode == 99:  # HLT
            break
        else:
            assert False, "Wrong opcode %r at pos %r" % (opcode, pc)
    return mem[0]


def execute_with_param(mem, noun, verb):
    testmem = mem[:]
    testmem[1] = noun
    testmem[2] = verb
    return intcode_processor(testmem)


# this is not pretty, but it only 10_000 iterations at max, so...
def search_params(mem, expected):
    for noun in range(100):
        for verb in range(100):
            result = execute_with_param(mem, noun, verb)
            if result == expected:
                return noun * 100 + verb
    return None


def process_data(data):
    mem = list(map(int, data.split(',')))
    return intcode_processor(mem)


def test():
    assert process_data("1,9,10,3,2,3,11,0,99,30,40,50") == 3500
    assert process_data("1,1,1,4,99,5,6,0,99") == 30


def main():
    with open(INPUT) as f:
        data = f.readline()
        mem = list(map(int, data.split(',')))
        result = execute_with_param(mem, 12, 2)
        print(result)  # part 1
        result = search_params(mem, 19690720)  # part 2
        print(result)


if __name__ == "__main__":
    main()
    # test()
