# https://adventofcode.com/2019/day/05

from __future__ import print_function

INPUT = "aoc2019_05_input.txt"
TRACE = 1
TRACE_MEM = 1

# np - number of parameters
INSTRUCTIONS = \
    {1: {"np": 3, "name": "ADD"},
     2: {"np": 3, "name": "MUL"},
     3: {"np": 1, "name": "INP"},
     4: {"np": 1, "name": "OUT"},
     5: {"np": 2, "name": "JNZ"},
     6: {"np": 2, "name": "JZE"},
     7: {"np": 3, "name": "IFL"},
     8: {"np": 3, "name": "IFE"},
     99: {"np": 0, "name": "HLT"},
     }


def intcode_processor(mem, input_data):

    def print_code(op, addr_mode, op_mem):
        params = INSTRUCTIONS[op]["np"]
        print(INSTRUCTIONS[op]["name"], end=" ")
        for p in range(params):
            if addr_mode[p]:
                print("#", end="")
            end = "\n" if p == params - 1 else ", "
            print(op_mem[p], end=end)

    def fetch_instruction(mem, pc):
        opcode = mem[pc]
        addr_mode = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
        op = opcode % 100
        try:
            params = INSTRUCTIONS[op]["np"]
        except KeyError:
            print("Unknown opcode %r at %r" % (op, pc))
            raise

        if TRACE:
            print("%03d" % pc, end=": ")
            print_code(op, addr_mode, mem[pc + 1:pc + params + 1])

        op_data = list(range(params))
        for p in range(params):
            op_data[p] = mem[pc + p + 1], addr_mode[p]
        return op, op_data

    def load_data(mem, op_data):
        param, addr_mode = op_data
        return mem[param] if addr_mode is 0 else param

    def get_addr(op_data):
        param, _ = op_data
        return param

    pc = 0
    next_pc = 0
    while True:
        op, op_data = fetch_instruction(mem, pc)
        next_pc = pc + INSTRUCTIONS[op]["np"] + 1
        if op == 1:  # ADD
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = op1 + op2
            if TRACE_MEM:
                print(">%r + %r = %r" % (op1, op2, mem[res]))

        elif op == 2:  # MUL
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = op1 * op2
            if TRACE_MEM:
                print(">%r * %r = %r" % (op1, op2, mem[res]))

        elif op == 3:  # STORE INPUT
            res = get_addr(op_data[0])
            mem[res] = input_data
            if TRACE_MEM:
                print(">%r" % mem[res])

        elif op == 4:  # OUTPUT
            val = load_data(mem, op_data[0])
            print("OUT:", val)

        elif op == 5:  # JNZ
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            if TRACE_MEM:
                print(">%r != 0" % op1)
            if op1:
                if TRACE_MEM:
                    print(">JUMP")
                next_pc = op2

        elif op == 6:  # JZ
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            if TRACE_MEM:
                print(">%r == 0" % op1)
            if not op1:
                if TRACE_MEM:
                    print(">JUMP")
                next_pc = op2

        elif op == 7:  # LESS
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = 1 if op1 < op2 else 0
            if TRACE_MEM:
                print(">%r < %r = %r" %(op1, op2, mem[res]))

        elif op == 8:  # EQUAL
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = 1 if op1 == op2 else 0
            if TRACE_MEM:
                print(">%r == %r = %r" % (op1, op2, mem[res]))

        elif op == 99:  # HLT
            break

        pc = next_pc

    return mem[0]


def process_data(data, inp):
    # print(data)
    mem = list(map(int, data.split(',')))
    return intcode_processor(mem, inp)


def test():
    process_data("3,0,4,0,99", 88)
    process_data("1002,4,3,4,33", 0)
    process_data("3,9,8,9,10,9,4,9,99,-1,8", 8)
    process_data("3,9,8,9,10,9,4,9,99,-1,8", 0)


def test2():
    process_data("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
                 "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,"
                 "104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", 50)


def main():
    with open(INPUT) as f:
        data = f.readline()
        # process_data(data, 1) # OUT: 15314507
        process_data(data, 5) # OUT: 652726


if __name__ == "__main__":
    # test()
    # test2()
    main()
