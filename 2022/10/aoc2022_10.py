# https://adventofcode.com/2022/day/10
from pathlib import Path


def execute_program(data):
    X, values_x = 1, []
    for line in data:
        instr, *arg = line.split()
        values_x.append(X)
        if instr == "addx":
            values_x.append(X) # takes two cycles
            X += int(arg[0])
    values_x.append(X)
    return values_x


def process_signal(signal):
    video_map = [[' '] * 40 for _ in range(6)]
    for y in range(6):
        line, line_offset = video_map[y], 40 * y
        for x in range(40):
            sprite_pos = signal[line_offset + x]
            if sprite_pos-1 <= x <= sprite_pos+1:
                line[x] = '#'
    return video_map


def print_screen(video_map):
    for line in video_map:
        print(''.join(line))


def process(data):
    # part 1
    signal = execute_program(data)
    result = sum(cycle * signal[cycle-1] for cycle in range(20, 221, 40))
    # result = 0
    print("part 1:", result)
    # part 2
    video_map = process_signal(signal)
    print("part 2:")
    print_screen(video_map)


def load_data(fileobj):
    return [line.strip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
