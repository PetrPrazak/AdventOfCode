# http://adventofcode.com/2015/day/7
from __future__ import print_function


# bitwise operatios in 16 bits
def clip(val): return val & 65535
def and_op(x, y): return clip(x & y)
def or_op(x, y): return clip(x | y)
def lshift_op(x, y): return clip(x << y)
def rshift_op(x, y): return clip(x >> y)
def not_op(x): return clip(~x)


def run_emulator(outputs, signal):
    """
    Continually evaluate all rules until all wire values stop changing
    """
    signal_changed = True
    while signal_changed:
        signal_changed = False
        for out, rule in outputs.items():
            sources, op = rule
            signaled_wires = set(signal.keys())
            required_wires = set([w for w in sources if not w.isdigit()])
            if not (required_wires.issubset(signaled_wires)):
                # not all required wires have a signal value
                continue
            values = [int(x) if x.isdigit() else signal[x] for x in sources]
            newvalue = op(*values)
            if newvalue != signal.get(out):
                signal[out] = newvalue
                signal_changed = True


def process(data):
    # part 1
    starts, outputs = data
    signal = dict(starts)
    run_emulator(outputs, signal)
    print("part 1:", signal['a'])
    # part 2
    new_signal = dict(starts)
    new_signal['b'] = signal['a']
    run_emulator(outputs, new_signal)
    print("part 2:", new_signal['a'])


def parse_line(line):
    rule = line.strip().split(' -> ')
    return rule


def load_data(fileobj):
    outputs = dict()
    starts = []
    rules = [parse_line(line) for line in fileobj]
    for rule in rules:
        inp, out = rule
        if inp.isdigit():
            starts.append((out, int(inp)))
        else:
            parts = inp.split()
            if len(parts) == 1:
                source = ([inp], lambda x: x)
            elif len(parts) == 2:
                assert parts[0] == "NOT"
                source = ([parts[1]], not_op)
            elif len(parts) == 3:
                cmd = parts[1]
                if cmd == "LSHIFT":
                    op = lshift_op
                elif cmd == "RSHIFT":
                    op = rshift_op
                elif cmd == "AND":
                    op = and_op
                elif cmd == "OR":
                    op = or_op
                else:
                    assert False, f"Unknown command {rule}"
                source = ([parts[0], parts[2]], op)
            outputs[out] = source
    return starts, outputs


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
