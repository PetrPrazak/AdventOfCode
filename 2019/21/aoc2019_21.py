# https://adventofcode.com/2019/day/21
from __future__ import print_function
from pathlib import Path
from aoc import read_input_ints_separated
from aoc.intcode import IntCode


def send_data(proc, inp):
    """ send a text string to process """
    i = None
    for c in inp:
        i = proc.send(ord(c))
    return i


def read_output(proc):
    """read process output until input is requested"""
    return list(iter(lambda p=proc: next(p), IntCode.INPUT_REQUESTED))


def send_input_read_prompt(proc, inp):
    i = send_data(proc, inp)
    if i == IntCode.INPUT_REQUESTED:
        return i
    out = [i]
    out.extend(read_output(proc))
    return out


def print_out(out):
    print(''.join(map(chr, filter(lambda d: d< 256, out))))
    return out[-1]


def run_script(data, lines, run=False):
    proc = IntCode(data).run()
    out = read_output(proc)
    print_out(out)
    for line in lines:
        if not line: continue
        print(line)
        inp = line + "\n"
        out = send_input_read_prompt(proc, inp)
        if out != IntCode.INPUT_REQUESTED:
            print_out(out)
            break
    out = send_input_read_prompt(proc, "WALK\n" if not run else "RUN\n")
    return print_out(out)


script1 = """
NOT A J
NOT C T
AND D T
OR T J
"""

script2 = """
NOT B J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
"""

def process(data):
    # part 1
    result = run_script(data, script1.split("\n"))
    print("part 1:", result)
    # part 2
    result = run_script(data, script2.split("\n"), run=True)
    print("part 2:", result)


def main(file="input.txt"):
    data = read_input_ints_separated(Path(__file__).parent.joinpath(file))
    process(data)


if __name__ == "__main__":
    main()
