# https://adventofcode.com/2019/day/11

from __future__ import print_function
from collections import defaultdict
from enum import IntEnum, Enum

INPUT = "aoc2019_11_input.txt"


class OpCode(IntEnum):
    ADD = 1
    MUL = 2
    INP = 3
    OUT = 4
    JNZ = 5
    JZE = 6
    IFL = 7
    IFE = 8
    INB = 9
    HLT = 99


class IntCode(object):
    TRACE = 0
    TRACE_MEM = 0
    DUMP_MEM = 0

    INSTRUCTIONS = {
        OpCode.ADD: 3,
        OpCode.MUL: 3,
        OpCode.INP: 1,
        OpCode.OUT: 1,
        OpCode.JNZ: 2,
        OpCode.JZE: 2,
        OpCode.IFL: 3,
        OpCode.IFE: 3,
        OpCode.INB: 1,
        OpCode.HLT: 0,
    }

    def __init__(self, program, proc_id=0):
        self.program = program
        self.proc_id = proc_id
        self.mem = defaultdict(int, enumerate(self.program))
        self.pc = 0
        self.base = 0
        self.out_mem = dict()
        self.next_input = None

    @staticmethod
    def print_code(op, addr_mode, op_mem):
        params = IntCode.INSTRUCTIONS[op]
        print(op.name, end=" ")
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

    def fetch_instruction(self):
        opcode = self.mem[self.pc]
        addr_mode = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
        try:
            op = OpCode(opcode % 100)
        except ValueError:
            print("Unknown opcode at", self.pc)
            raise

        params = IntCode.INSTRUCTIONS[op]
        if IntCode.TRACE:
            print("<%r> %03d" % (self.proc_id, self.pc), end=": ")
            op_params = [self.mem[a] for a in range(self.pc + 1, self.pc + params + 1)]
            IntCode.print_code(op, addr_mode, op_params)

        op_data = list(range(params))
        for p in range(params):
            op_data[p] = self.mem[self.pc + p + 1], addr_mode[p]
        return op, params, op_data

    def load_data(self, op_data):
        param, addr_mode = op_data
        if addr_mode == 0:
            val = self.mem[param]
        elif addr_mode == 1:
            val = param
        elif addr_mode == 2:
            val = self.mem[param + self.base]
        else:
            assert False, "Invalid address mode"
        return val

    def get_addr(self, op_data):
        param, addr_mode = op_data
        if addr_mode == 0:
            return param
        elif addr_mode == 2:
            return param + self.base
        else:
            assert False, "Invalid address mode"

    def reset(self):
        self.mem = defaultdict(int, enumerate(self.program))
        self.pc = 0
        self.base = 0
        self.out_mem = dict()
        self.next_input = None

    def _dump_mem(self, addr):
        self.out_mem[addr] = self.mem[addr]
        print("<%r>" % self.proc_id, self.out_mem)

    def _trace_mem(self, data):
        print("<%r>" % self.proc_id, data)

    def run(self):
        while True:
            op, params, op_data = self.fetch_instruction()
            next_pc = self.pc + 1 + params

            if op == OpCode.ADD:
                op1 = self.load_data(op_data[0])
                op2 = self.load_data(op_data[1])
                res = self.get_addr(op_data[2])
                self.mem[res] = op1 + op2
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r + %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.MUL:
                op1 = self.load_data(op_data[0])
                op2 = self.load_data(op_data[1])
                res = self.get_addr(op_data[2])
                self.mem[res] = op1 * op2
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r * %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.INP:
                res = self.get_addr(op_data[0])
                val = self.next_input if self.next_input is not None else (yield)
                if val is None:
                    raise ValueError("wrong input value")
                self.mem[res] = val
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r" % self.mem[res])
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.OUT:
                val = self.load_data(op_data[0])
                if IntCode.TRACE_MEM:
                    self._trace_mem("OUT: %r" % val)
                self.next_input = yield val

            elif op == OpCode.JNZ:
                op1 = self.load_data(op_data[0])
                op2 = self.load_data(op_data[1])
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r != 0" % op1)
                if op1:
                    next_pc = op2
                    if IntCode.TRACE_MEM:
                        self._trace_mem("JUMP")

            elif op == OpCode.JZE:
                op1 = self.load_data(op_data[0])
                op2 = self.load_data(op_data[1])
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r == 0" % op1)
                if not op1:
                    next_pc = op2
                    if IntCode.TRACE_MEM:
                        self._trace_mem("JUMP")

            elif op == OpCode.IFL:
                op1 = self.load_data(op_data[0])
                op2 = self.load_data(op_data[1])
                res = self.get_addr(op_data[2])
                self.mem[res] = 1 if op1 < op2 else 0
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r < %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.IFE:
                op1 = self.load_data(op_data[0])
                op2 = self.load_data(op_data[1])
                res = self.get_addr(op_data[2])
                self.mem[res] = 1 if op1 == op2 else 0
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r == %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.INB:
                val = self.load_data(op_data[0])
                self.base += val
                if IntCode.TRACE_MEM:
                    self._trace_mem("BASE = %r" % self.base)

            elif op == OpCode.HLT:
                raise StopIteration

            self.pc = next_pc


def single_run(program, single_input):
    proc = IntCode(program).run()
    next(proc)
    out = proc.send(single_input)
    output = [out]
    for out in proc:
        output.append(out)
    return out


###################################################################


def read_input_line(filename):
    with open(filename) as f:
        data = f.readline().rstrip()
        return data


def read_input_ints(filename):
    ints = list(map(int, read_input_line(filename)))
    return ints


def read_input_ints_separated(filename, sep=','):
    ints = list(map(int, read_input_line(filename).split(sep)))
    return ints


###################################################################

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn_left(self):
        return Direction((self.value + 3) % 4)

    def turn_right(self):
        return Direction((self.value + 1) % 4)

    def step(self):
        return [(0, -1), (1, 0), (0, 1), (-1, 0)][self.value]


def process(program, panels):
    proc = IntCode(program).run()
    next(proc)

    d = Direction.UP
    pos = (0, 0)
    while True:
        try:
            panels[pos] = proc.send(panels[pos])
            new_dir = next(proc)
            if new_dir == 0:
                d = d.turn_left()
            else:
                d = d.turn_right()
            step = d.step()
            pos = pos[0] + step[0], pos[1] + step[1]
        except StopIteration:
            break


def print_panels(panels):
    coords = list(panels.keys())
    min_x = min(coords)[0]
    min_y = min(coords, key=lambda k: k[1])[1]
    max_x = max(coords)[0]
    max_y = max(coords, key=lambda k: k[1])[1]
    for line in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            pos = col, line
            pixel = '#' if pos in panels and panels[pos] == 1 else ' '
            print(pixel, sep="", end="")
        print("")


def main():
    program = read_input_ints_separated(INPUT)
    # part 1
    panels = defaultdict(int)
    process(program, panels)
    print(len(panels.keys()))  # 2041
    # part 2
    panels = defaultdict(int)
    panels[(0, 0)] = 1
    process(program, panels)
    print_panels(panels)  # ZRZPKEZR


if __name__ == "__main__":
    main()
