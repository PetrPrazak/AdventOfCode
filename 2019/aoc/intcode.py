# https://adventofcode.com/2019/day/09

from __future__ import print_function
from collections import defaultdict
from enum import IntEnum

# public exports
__all__ = ['IntCode', 'single_run']


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


# argument options
ARG_READ = 0
ARG_WRITE = 1


class IntCode(object):
    TRACE = 0
    TRACE_MEM = 0
    DUMP_MEM = 0
    TRACE_IO = 0

    INSTRUCTIONS = {
        OpCode.ADD: (ARG_READ, ARG_READ, ARG_WRITE),
        OpCode.MUL: (ARG_READ, ARG_READ, ARG_WRITE),
        OpCode.INP: (ARG_WRITE,),
        OpCode.OUT: (ARG_READ,),
        OpCode.JNZ: (ARG_READ, ARG_READ),
        OpCode.JZE: (ARG_READ, ARG_READ),
        OpCode.IFL: (ARG_READ, ARG_READ, ARG_WRITE),
        OpCode.IFE: (ARG_READ, ARG_READ, ARG_WRITE),
        OpCode.INB: (ARG_READ,),
        OpCode.HLT: (),
    }

    INPUT_REQUESTED = "Input"

    def __init__(self, program, proc_id=0):
        self.program = program
        self.proc_id = proc_id
        self.mem = defaultdict(int, enumerate(self.program))
        self.pc = 0
        self.base = 0
        self.out_mem = dict()
        self.next_input = None

    @staticmethod
    def print_code(op, addr_mode, op_mem, data):
        params = len(IntCode.INSTRUCTIONS[op])
        line = str(op.name)
        for p in range(params):
            if addr_mode[p] == 1:
                format_str = " %d"
            elif addr_mode[p] == 2:
                format_str = " +(%d)"
            else:
                format_str = " [%d]"
            line += format_str % op_mem[p]
            if p < params - 1:
                line += ","
        print("%-30s; %r" % (line, data))

    def fetch_instruction(self):
        opcode = self.mem[self.pc]
        addr_mode = [(opcode // 100) % 10, (opcode // 1000) % 10, (opcode // 10000) % 10]
        try:
            op = OpCode(opcode % 100)
        except ValueError:
            print("Unknown opcode at", self.pc)
            raise

        params = IntCode.INSTRUCTIONS[op]
        param_count = len(params)
        op_data = [None] * param_count
        for p in range(param_count):
            arg = self.mem[self.pc + p + 1]
            if params[p] == ARG_READ:
                op_data[p] = self.load_data((arg, addr_mode[p]))
            else:  # ARG_WRITE
                op_data[p] = self.get_addr((arg, addr_mode[p]))

        if IntCode.TRACE:
            print("<%r> %03d" % (self.proc_id, self.pc), end=": ")
            op_params = [self.mem[a] for a in range(self.pc + 1, self.pc + param_count + 1)]
            IntCode.print_code(op, addr_mode, op_params, op_data)

        return op, op_data

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
        self.reset()
        while True:
            op, op_data = self.fetch_instruction()
            next_pc = self.pc + 1 + len(op_data)

            if op == OpCode.ADD:
                op1, op2, res = op_data
                self.mem[res] = op1 + op2
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r + %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.MUL:
                op1, op2, res = op_data
                self.mem[res] = op1 * op2
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r * %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.INP:
                res = op_data[0]
                val = self.next_input if self.next_input is not None else (yield IntCode.INPUT_REQUESTED)
                if IntCode.TRACE_IO:
                    self._trace_mem("INPUT: %r" % val)
                self.next_input = None
                if val is None:
                    raise ValueError("wrong input value")
                self.mem[res] = val
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.OUT:
                val = op_data[0]
                if IntCode.TRACE_IO:
                    self._trace_mem("OUTPUT: %r" % val)
                self.next_input = yield val

            elif op == OpCode.JNZ:
                op1, op2 = op_data
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r != 0" % op1)
                if op1:
                    next_pc = op2
                    if IntCode.TRACE_MEM:
                        self._trace_mem("JUMP")

            elif op == OpCode.JZE:
                op1, op2 = op_data
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r == 0" % op1)
                if not op1:
                    next_pc = op2
                    if IntCode.TRACE_MEM:
                        self._trace_mem("JUMP")

            elif op == OpCode.IFL:
                op1, op2, res = op_data
                self.mem[res] = 1 if op1 < op2 else 0
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r < %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.IFE:
                op1, op2, res = op_data
                self.mem[res] = 1 if op1 == op2 else 0
                if IntCode.TRACE_MEM:
                    self._trace_mem("%r == %r = %r" % (op1, op2, self.mem[res]))
                if IntCode.DUMP_MEM:
                    self._dump_mem(res)

            elif op == OpCode.INB:
                val = op_data[0]
                self.base += val
                if IntCode.TRACE_MEM:
                    self._trace_mem("BASE = %r" % self.base)

            elif op == OpCode.HLT:
                raise StopIteration

            self.pc = next_pc


def single_run(program, single_input=None):
    proc = IntCode(program).run()
    output = list()
    if single_input is not None:
        next(proc)
        output.append(proc.send(single_input))
    output.extend([out for out in proc])
    return output


if __name__ == "__main__":
    IntCode.TRACE = 1
    IntCode.TRACE_MEM = 0
    IntCode.DUMP_MEM = 0
    prog1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    out1 = single_run(prog1)
    print(prog1)
    print(out1)
    assert prog1 == out1
