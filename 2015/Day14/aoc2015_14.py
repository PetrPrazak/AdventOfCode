# http://adventofcode.com/2015/day/14
from __future__ import print_function
from collections import defaultdict


def calc_distance(reindeer, in_time):
    name, speed, speed_time, rest_time = reindeer
    cycles, rem = divmod(in_time, speed_time + rest_time)
    return (cycles * speed_time + min(speed_time, rem)) * speed, name


def calc_race(data, in_time):
    return [calc_distance(reindeer, in_time) for reindeer in data]


def award_points(data, in_time, tally):
    race = calc_race(data, in_time)
    winner_distance = max(race)[0]
    # check for multiple winners
    winners = filter(lambda r: r[0] == winner_distance, race)
    for _, winner in winners:
        tally[winner] += 1


def process(data):
    # part 1
    race = calc_race(data, 2503)
    winning = max(race)
    print("Part 1:", winning[0])
    # part 2
    tally = defaultdict(int)
    for tick in range(1, 2503 + 1):
        award_points(data, tick, tally)
    winner = max(tally, key = lambda key: tally[key])
    print("Part 2:", tally[winner])


def parse(line):
    line = line.strip().split()
    name, speed, speed_time, rest_time = line[0], int(line[3]), int(line[6]), int(line[13])
    return name, speed, speed_time, rest_time


def load_data(fileobj):
    data = [parse(line) for line in fileobj]
    return data


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
