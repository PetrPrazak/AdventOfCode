# https://adventofcode.com/2020/day/15


def game(data, stop=2020):
    spoken = {n: i+1 for i, n in enumerate(data)}
    last = 0
    for turn in range(len(data)+1, stop):
        when = spoken.get(last, turn)
        spoken[last] = turn
        last = turn - when
    return last


def process(data):
    # part 1
    print(data)
    result = game(data)
    print("part 1:", result)
    # part 2
    result = game(data, 30000000)
    print("part 2:", result)


def load_data(line):
    return [int(l) for l in line.split(',')]


def main(line):
    process(load_data(line))


if __name__ == "__main__":
    main("2,3,1")
    main("16,11,15,0,1,7")
