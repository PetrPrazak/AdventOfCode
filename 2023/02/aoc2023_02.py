# https://adventofcode.com/2023/day/2
from pathlib import Path
import time

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def process(data):
    # part 1
    total = total2 = 0
    for game, sets in data:
        goodgame = True
        max_blue = max_green = max_red = 0
        for s in sets:
            for cube in s:
                count, color = cube.split(' ')
                count = int(count)
                if color == 'red':
                    max_red = max(max_red, count)
                    if count > MAX_RED:
                        goodgame = False
                elif color == 'blue':
                    max_blue = max(max_blue, count)
                    if count > MAX_BLUE:
                        goodgame = False
                elif color == 'green':
                    max_green = max(max_green, count)
                    if count > MAX_GREEN:
                        goodgame = False
                else:
                    assert ("Wrong color")
        if goodgame:
            total += game
        total2 += max_red * max_green * max_blue

    print("part 1:", total)
    # part 2
    print("part 2:", total2)


def parse_line(line):
    game, sets = line.split(': ')
    game = int(game.split(' ')[1])
    sets = [tuple(s.split(', ')) for s in sets.split('; ')]
    return game, sets


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
