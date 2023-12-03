# https://adventofcode.com/2023/day/3
from pathlib import Path
from collections import defaultdict
import time


def is_symbol(c):
    return not c.isdigit() and c != '.'


def scan_symbol(data, row, col1, col2):
    def check_row(row, symbols):
        adjrow = data[row][startcol:endcol+1]
        symbols += [(c, (row, startcol + i))
                    for i, c in enumerate(adjrow) if is_symbol(c)]

    def check_col(col, symbols):
        c = data[row][col]
        if is_symbol(c):
            symbols += [(c, (row, col))]

    maxrow, maxcol = len(data), len(data[0])
    startcol = col1 - 1 if col1 > 0 else col1
    endcol = col2 + 1 if col2 < maxcol - 1 else col2
    symbols = []
    if row > 0:
        check_row(row-1, symbols)
    if row < maxrow - 1:
        check_row(row+1, symbols)
    if startcol < col1:
        check_col(startcol, symbols)
    if endcol > col2:
        check_col(endcol, symbols)
    return symbols


def find_nums(data):
    def process_number(pos, col):
        if symbols := scan_symbol(data, *pos, col):
            digits.append(num)
            for s in symbols:
                symbol_nums[s].append(num)

    symbol_nums = defaultdict(list)
    digits = []
    for row, line in enumerate(data):
        digit_pos, num = None, 0
        for col, c in enumerate(line):
            if c.isdigit():
                if not digit_pos:
                    digit_pos = row, col
                num *= 10
                num += int(c)
            else:
                if digit_pos:
                    process_number(digit_pos, col-1)
                    digit_pos = None
                num = 0
        # end of line check
        if digit_pos:
            process_number(digit_pos, col)

    return digits, symbol_nums


def process(data):
    # part 1
    numbers, symbol_map = find_nums(data)
    print("part 1:", sum(numbers))

    # part 2
    result = sum(nums[0] * nums[1]
                 for symbol, nums in symbol_map.items() if symbol[0] == '*' and len(nums) == 2)
    print("part 2:", result)


def load_data(fileobj):
    return [line.rstrip() for line in fileobj.readlines()]


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
