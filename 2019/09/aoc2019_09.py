# https://adventofcode.com/2019/day/09

from __future__ import print_function
from collections import defaultdict

INPUT = "aoc2019_09_input.txt"

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
     9: {"np": 1, "name": "INB"},
     99: {"np": 0, "name": "HLT"},
     }


def intcode_processor(initmem, proc_id):
    def print_code(op, addr_mode, op_mem):
        instr = INSTRUCTIONS[op]
        params = instr["np"]
        print(instr["name"], end=" ")
        for p in range(params):
            if addr_mode[p] == 1:
                print("%d" % op_mem[p], end="")
            elif addr_mode[p] == 2:
                print("+(%d)" % op_mem[p], end="")
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
            print_code(op, addr_mode, [mem[a] for a in range(pc + 1, pc + params + 1)])

        op_data = list(range(params))
        for p in range(params):
            op_data[p] = mem[pc + p + 1], addr_mode[p]
        return op, params, op_data

    def load_data(mem, base, op_data):
        param, addr_mode = op_data
        if addr_mode == 0:
            val = mem[param]
        elif addr_mode == 1:
            val = param
        else:
            val = mem[param + base]
        return val

    def get_addr(op_data, base):
        param, addr_mode = op_data
        if addr_mode == 0:
            return param
        elif addr_mode == 2:
            return param + base
        else:
            assert False

    mem = defaultdict(int, enumerate(initmem))
    pc = 0
    base = 0
    out_mem = dict()
    while True:
        op, params, op_data = fetch_instruction(mem, pc)
        next_pc = pc + 1 + params

        if op == 1:  # ADD
            op1, op2 = load_data(mem, base, op_data[0]), load_data(mem, base, op_data[1])
            res = get_addr(op_data[2], base)
            mem[res] = op1 + op2
            if TRACE_MEM:
                print("<%r> %r + %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 2:  # MUL
            op1, op2 = load_data(mem, base, op_data[0]), load_data(mem, base, op_data[1])
            res = get_addr(op_data[2], base)
            mem[res] = op1 * op2
            if TRACE_MEM:
                print("<%r> %r * %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 3:  # INP
            res = get_addr(op_data[0], base)
            mem[res] = yield
            # print("INPUT[%d]" % proc_id, res, mem[res])
            if TRACE_MEM:
                print("<%r> %r" % (proc_id, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 4:  # OUT
            val = load_data(mem, base, op_data[0])
            if TRACE_MEM:
                print("<%r> OUT: %r" % (proc_id, val))
            # print("OUTPUT:", val)
            yield val

        elif op == 5:  # JNZ
            op1, op2 = load_data(mem, base, op_data[0]), load_data(mem, base, op_data[1])
            if TRACE_MEM:
                print("<%r> %r != 0" % (proc_id, op1))
            if op1:
                if TRACE_MEM:
                    print("<%r> JUMP" % proc_id)
                next_pc = op2

        elif op == 6:  # JZE
            op1, op2 = load_data(mem, base, op_data[0]), load_data(mem, base, op_data[1])
            if TRACE_MEM:
                print("<%r> %r == 0" % (proc_id, op1))
            if not op1:
                if TRACE_MEM:
                    print("<%r> JUMP" % proc_id)
                next_pc = op2

        elif op == 7:  # IFL
            op1, op2 = load_data(mem, base, op_data[0]), load_data(mem, base, op_data[1])
            res = get_addr(op_data[2], base)
            mem[res] = 1 if op1 < op2 else 0
            if TRACE_MEM:
                print("<%r> %r < %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 8:  # IFE
            op1, op2 = load_data(mem, base, op_data[0]), load_data(mem, base, op_data[1])
            res = get_addr(op_data[2], base)
            mem[res] = 1 if op1 == op2 else 0
            if TRACE_MEM:
                print("<%r> %r == %r = %r" % (proc_id, op1, op2, mem[res]))
            if DUMP_MEM:
                out_mem[res] = mem[res]
                print("<%r>" % proc_id, out_mem)

        elif op == 9:  # INB
            val = load_data(mem, base, op_data[0])
            base += val
            if TRACE_MEM:
                print("<%r> BASE =" % proc_id, base)

        elif op == 99:  # HLT
            raise StopIteration

        pc = next_pc


def run(data, inp):
    mem = list(map(int, data.split(',')))
    proc = intcode_processor(mem, 0)
    next(proc)
    out = proc.send(inp)
    print(out)
    for out in proc:
        print(out)


def main():
    with open(INPUT) as f:
        data = f.readline()
        run(data, 1)
        run(data, 2)


if __name__ == "__main__":
    main()
