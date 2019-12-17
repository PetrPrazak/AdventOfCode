# https://adventofcode.com/2019/day/17
from __future__ import print_function
import re
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *
from aoc.intcode import IntCode, single_run

INPUT = "aoc2019_17_input.txt"


def get_next_pos(pos, direction):
    dpos = [(0, -1), (1, 0), (0, 1), (-1, 0)][direction]
    return pos[0] + dpos[0], pos[1] + dpos[1]


def get_all_neighbors(pos):
    return [get_next_pos(pos, d) for d in range(4)]


def parse_map(mapa):
    grid = {(x, y): c for y, line in enumerate(mapa)
            for x, c in enumerate(line) if c != '.'}
    return grid


def list_to_str(intlist):
    return cat([chr(x) for x in intlist])


# @timeit
def load_grid(data):
    out = list_to_str(data).rstrip().split('\n')
    grid = parse_map(out)
    crossings = []
    for pos in grid:
        if grid[pos] == '.':
            continue
        nbrs = [n for n in get_all_neighbors(pos)
                if n in grid and grid[n] != '.']
        if len(nbrs) == 4:
            crossings.append(pos)
    return grid, crossings


def get_start_pos(grid):
    startpos = None
    for pos, c in grid.items():
        if c == '^':
            startpos = pos
            break
    return startpos


def walk_map(grid, start_pos, direction=0):
    out = []
    while True:
        where = [('R', (direction + 1) % 4), ('L', (direction + 3) % 4)]
        possible = [(pos, next_dir, turn) for turn, next_dir in where
                    for pos in [get_next_pos(start_pos, next_dir)] if pos in grid]
        if not possible:
            return out
        nextpos, direction, turn = possible[0]
        peek = get_next_pos(nextpos, direction)
        while peek in grid:
            nextpos = peek
            peek = get_next_pos(nextpos, direction)
        steps = max(abs(nextpos[0] - start_pos[0]), abs(nextpos[1] - start_pos[1]))
        cmd = f"{turn}{steps}"
        out.append(cmd)
        start_pos = nextpos


def find_substrings(path):
    func = dict()
    for sub in range(3):
        minlen = len(path)
        bestcmd = None
        for sublen in range(4, 20):
            substr = path[0:sublen]
            newpath = path.replace(substr, "")
            if len(newpath) < minlen:
                minlen = len(newpath)
                bestcmd = substr
        func[sub] = bestcmd
        path = path.replace(bestcmd, "")
    assert len(path) == 0
    return func


# send a string to processor
def send_data(proc, inp):
    i = None
    for c in inp:
        i = proc.send(ord(c))
    return i


# read process output until input is requested
def read_output(proc):
    out = [o for o in iter(lambda p=proc: next(p), IntCode.INPUT_REQUESTED)]
    return out


def split_commands(commands):
    inp = ''
    for i, cmd in enumerate(re.findall('([LR]\d+)', commands)):
        if i != 0:
            inp += ','
        inp += ','.join([cmd[0], cmd[1:]])
    inp += '\n'
    return inp


def send_input_read_prompt(proc, inp):
    out = [send_data(proc, inp)]
    out.extend(read_output(proc))
    return out


def program_robot(program, mainfunc, func):
    program[0] = 2
    proc = IntCode(program).run()

    out = read_output(proc)  # grid and prompt "Main:"
    inp = ','.join(list(mainfunc)) + '\n'
    out = send_input_read_prompt(proc, inp)  # Function A

    for s in range(3):
        # send functions
        inp = split_commands(func[s])
        send_input_read_prompt(proc, inp)  # Function [BC], Video feed?

    out = [send_data(proc, "n\n")]
    while True:
        try:
            out.append(next(proc))
        except StopIteration:
            break

    return out[-1]


def process(program):
    # part 1
    out = single_run(program)
    grid, crossings = load_grid(out)
    print(sum([x * y for x, y in crossings]))

    # part 2
    # find start
    startpos = get_start_pos(grid)
    commands = walk_map(grid, startpos)
    func = find_substrings(cat(commands))
    # replace occurences of functions in all commands
    mainfunc = cat(commands)
    for sub, cmd in func.items():
        mainfunc = mainfunc.replace(cmd, "ABC"[sub])

    ret = program_robot(program, mainfunc, func)
    print(ret)


def main():
    data = read_input_ints_separated(INPUT)
    process(data)


if __name__ == "__main__":
    main()
