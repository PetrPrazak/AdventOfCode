# https://adventofcode.com/2018/day/4

from __future__ import print_function
from collections import defaultdict, Counter
import re


INPUT = "aoc2018_day04.txt"

time_regex = re.compile(r"\[(\d+)-(\d+)-(\d+)\s(\d+):(\d+)\]")
guard_regex = re.compile(r"#(\d+)")

with open(INPUT) as f:
    data = [x.strip() for x in f.readlines()]
    data.sort()

    active_guard = guard_id = sleeps_at = 0
    chart = defaultdict(list)
    for line in data:
        ts = time_regex.match(line)
        minute = int(ts.group(5))
        gr = guard_regex.search(line)
        if gr:
            guard_id = int(gr.group(1))
        if line.find("falls asleep") != -1:
            sleeps_at = minute
        elif line.find("wakes up") != -1:
            slept = minute - sleeps_at
            chart[guard_id].append((sleeps_at, minute))

    # part 1
    best = winner = 0
    for g, l in chart.items():
        total = sum([e-s for s,e in l])
        if total > best:
            best = total
            winner = g

    c = Counter()
    for (start,end) in chart[winner]:
        c += Counter(range(start,end))
    minute, count = c.most_common(1)[0]
    print(winner * minute)

    # part 2
    winner = win_minute = best = 0
    for g, l in chart.items():
        c = Counter()
        for (start, end) in l:
            c += Counter(range(start, end))
        minute, count = c.most_common(1)[0]
        if count > best:
            best = count
            win_minute = minute
            winner = g

    print(win_minute * winner)