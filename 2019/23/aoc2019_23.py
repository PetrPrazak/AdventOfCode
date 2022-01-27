# https://adventofcode.com/2019/day/23
from __future__ import print_function
from collections import deque
from pathlib import Path
from aoc import read_input_ints_separated
from aoc.intcode import IntCode


def network_is_idle(output):
    return all(not q or q[0] == IntCode.INPUT_REQUESTED for q in output)


def cycle_network(network, output, part1=True):
    nat = None
    last_sent = None
    while True:
        for i, proc in enumerate(network):
            if output[i]:
                val = output[i].popleft()
            else:
                val = next(proc)
            if val == IntCode.INPUT_REQUESTED:
                if not part1 and i == 0 and nat and network_is_idle(output):
                    output[i].append(nat)
                    x, y = nat
                    if y == last_sent:
                        return y
                    last_sent = y
                    nat = None
                if output[i]:
                    x, y = output[i].popleft()
                    val = proc.send(x)
                    assert val == IntCode.INPUT_REQUESTED
                    val = proc.send(y)
                else:
                    val = proc.send(-1)
            elif type(val) is tuple:
                x, y = val
                val = proc.send(x)
                assert val == IntCode.INPUT_REQUESTED
                val = proc.send(y)

            if val == IntCode.INPUT_REQUESTED:
                output[i].appendleft(val)
            else:
                addr, x, y = val, next(proc), next(proc)
                if addr == 255:
                    if part1:
                        return y
                    else:
                        nat = x, y
                else:
                    output[addr].append((x, y))


def init_proc(network):
    output = [deque() for _ in range(len(network))]
    for i, proc in enumerate(network):
        _ = next(proc)
        output[i].append(proc.send(i))
    return output


def build_network(data):
    network = [IntCode(data, i).run() for i in range(50)]
    output = init_proc(network)
    return network, output


def process(data):
    # part 1
    result = cycle_network(*build_network(data))
    print("part 1:", result)
    # part 2
    result = cycle_network(*build_network(data), part1=False)
    print("part 2:", result)


def main(file="input.txt"):
    data = read_input_ints_separated(Path(__file__).parent.joinpath(file))
    process(data)


if __name__ == "__main__":
    main()
