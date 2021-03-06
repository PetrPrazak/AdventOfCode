# https://adventofcode.com/2019/day/07

from __future__ import print_function
from itertools import permutations

INPUT = "aoc2019_07_input.txt"


TRACE = 0
TRACE_MEM = 0
DUMP_MEM = 0

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


def intcode_processor(mem, proc_id):
    def print_code(op, addr_mode, op_mem):
        instr = INSTRUCTIONS[op]
        params = instr["np"]
        print(instr["name"], end=" ")
        for p in range(params):
            if addr_mode[p]:
                print("%d" % op_mem[p], end="")
            else:
                print("[%d]" % op_mem[p], end="")
            if p < params - 1:
                print(", ", end="")
        print("")

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
            print("<%r> %03d" % (proc_id, pc), end=": ")
            print_code(op, addr_mode, mem[pc + 1:pc + params + 1])

        op_data = list(range(params))
        for p in range(params):
            op_data[p] = mem[pc + p + 1], addr_mode[p]
        return op, params, op_data

    def load_data(mem, op_data):
        param, addr_mode = op_data
        return mem[param] if addr_mode is 0 else param

    def get_addr(op_data):
        param, _ = op_data
        return param

    pc = 0
    out_mem = dict()
    # print("==START==", proc_id)
    while True:
        op, params, op_data = fetch_instruction(mem, pc)
        next_pc = pc + 1 + params

        if op == 1:  # ADD
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = op1 + op2
            if TRACE_MEM:
                print("<%r> %r + %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 2:  # MUL
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = op1 * op2
            if TRACE_MEM:
                print("<%r> %r * %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 3:  # INP
            res = get_addr(op_data[0])
            mem[res] = yield
            # print("INPUT[%d]" % proc_id, res, mem[res])
            if TRACE_MEM:
                print("<%r> %r" % (proc_id, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 4:  # OUT
            val = load_data(mem, op_data[0])
            if TRACE_MEM:
                print("<%r> OUT: %r" % (proc_id, val))
            # print("OUTPUT:", val)
            yield val

        elif op == 5:  # JNZ
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            if TRACE_MEM:
                print("<%r> %r != 0" % (proc_id, op1))
            if op1:
                if TRACE_MEM:
                    print("<%r> JUMP")
                next_pc = op2

        elif op == 6:  # JZE
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            if TRACE_MEM:
                print("<%r> %r == 0" % op1)
            if not op1:
                if TRACE_MEM:
                    print("<%r> JUMP")
                next_pc = op2

        elif op == 7:  # IFL
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = 1 if op1 < op2 else 0
            if TRACE_MEM:
                print("<%r> %r < %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 8:  # IFE
            op1, op2 = load_data(mem, op_data[0]), load_data(mem, op_data[1])
            res = get_addr(op_data[2])
            mem[res] = 1 if op1 == op2 else 0
            if TRACE_MEM:
                print("<%r> %r == %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 99:  # HLT
            raise StopIteration

        pc = next_pc


def sigle_run(mem, perm):
    last_out = 0
    amps = []
    for amp in list(perm):
        proc = intcode_processor(mem[:], amp)
        next(proc)  # for input
        proc.send(amp)
        amps.append(proc)
    for proc in amps:
        last_out = proc.send(last_out)
    return last_out


def part1(data):
    mem = list(map(int, data.split(',')))
    outs = [(sigle_run(mem, p), p) for p in permutations(range(0, 5))]
    print(max(outs))


def loop_run(mem, perm):
    amp_list = list(perm)
    context = []
    for amp in amp_list:
        proc = intcode_processor(mem[:], amp)
        next(proc)
        proc.send(amp)
        context.append(proc)

    last_out = 0
    while True:
        for amp in context:
            last_out = amp.send(last_out)
        try:
            for amp in context:
                next(amp)
        except StopIteration:
            break

    return last_out


def part2(data):
    mem = list(map(int, data.split(',')))
    outs = [(loop_run(mem, p), p) for p in permutations(range(5, 10))]
    print(max(outs))


def main():
    with open(INPUT) as f:
        data = f.readline()
        part1(data)
        part2(data)


if __name__ == "__main__":
    main()
