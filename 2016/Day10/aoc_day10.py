# http://adventofcode.com/2016/day/10
from __future__ import print_function
from collections import defaultdict
from math import prod


def set_bot_data(bots, outputs, bot, value):
    if not bot in bots:
        bots[bot] = {'p': None, "d": []}
    bots[bot]["d"].append(value)
    l = bots[bot]["d"]
    if len(l) == 2:
        bot_run(bots, outputs, bot)


def bot_run(bots, outputs, bot):
    prg = bots[bot]["p"]
    if prg:
        l = bots[bot]["d"]
        low, val = prg[0]
        if low == "bot":
            set_bot_data(bots, outputs, val, min(l))
        else:
            outputs[val] = min(l)
        high, val = prg[1]
        if high == "bot":
            set_bot_data(bots, outputs, val, max(l))
        else:
            outputs[val] = max(l)


def solve(lines):
    bots = defaultdict(dict)
    outputs = {}
    for part in lines:
        # value 11 goes to bot 124
        if part[0] == "value":
            value = int(part[1])
            bot = int(part[5])
            set_bot_data(bots, outputs, bot, value)
        # bot 153 gives low to bot 105 and high to bot 10
        # bot 12 gives low to output 4 and high to bot 125
        elif part[0] == "bot":
            bot = int(part[1])
            low_to = int(part[6])
            high_to = int(part[11])
            data = bots[bot]["d"] if bot in bots else []
            bots[bot] = {"p": [(part[5], low_to), (part[10], high_to)], "d": data}
            if len(data) == 2:
                bot_run(bots, outputs, bot)
        else:
            raise NotImplementedError(part)

    print("Part 1:", [k for k in bots
                      if 61 in bots[k]["d"] and 17 in bots[k]["d"]][0])
    print("Part 2:", prod([outputs[0], outputs[1], outputs[2]]))


def main(file):
    with open(file) as f:
        lines = [line.strip().split() for line in f.readlines()]
        solve(lines)


if __name__ == "__main__":
    main("aoc_day10_input.txt")
