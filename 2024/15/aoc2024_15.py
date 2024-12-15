# https://adventofcode.com/2024/day/15
from pathlib import Path
import time


def make_grid1(amap):
    grid, start = dict(), None
    for r, row in enumerate(amap):
        for c, cell in enumerate(row):
            if cell == '@':
                start = r, c
            grid[(r, c)] = cell
    return grid, start


def make_grid2(amap):
    grid, start = dict(), None
    for r, row in enumerate(amap):
        for c, cell in enumerate(row):
            cc = c * 2
            grid[(r, cc)] = cell
            if cell == '@':
                start = r, cc
                grid[(r, cc+1)] = '.'
            elif cell == '#':
                grid[(r, cc+1)] = '#'
            elif cell == '.':
                grid[(r, cc+1)] = '.'
            elif cell == 'O':
                grid[(r, cc)] = '['
                grid[(r, cc+1)] = ']'
    return grid, start


def print_grid(grid, height, width):
    for r in range(height):
        line = "".join(grid[(r, c)] for c in range(width))
        print(line)
    print()


def calcGPS(grid, box='O'):
    return sum(p*100+c for (p, c), v in grid.items() if v == box)


def direction(move):
    return [(0, 1), (0, -1), (-1, 0), (1, 0)]["><^v".index(move)]


def move_column(grid, pr, pc, dr, dc, end_r, end_c):
    while end_r != pr or end_c != pc:
        prev_r, prev_c = end_r - dr, end_c - dc
        grid[(end_r, end_c)] = grid[(prev_r, prev_c)]
        end_r, end_c = prev_r, prev_c
    grid[(pr, pc)] = '.'


def walk1(grid, start, moves):
    pr, pc = start
    for move in moves:
        dr, dc = direction(move)
        nr, nc = pr + dr, pc+dc
        cell = grid[(nr, nc)]
        if cell == '#':
            pass
        elif cell == 'O':
            while cell == 'O':
                nr, nc = nr + dr, nc + dc
                cell = grid[(nr, nc)]
            if cell == '.':
                move_column(grid, pr, pc, dr, dc, nr, nc)
                pr, pc = pr + dr, pc + dc
        elif cell == '.':
            grid[(pr, pc)] = '.'
            pr, pc = nr, nc
            grid[(pr, pc)] = '@'


def can_move_up_down(grid, pr, pc, dr):
    cell = grid[(pr, pc)]
    if cell == ']':
        pc += -1
    nr = pr + dr
    cell1 = grid.get((nr, pc), '#')
    cell2 = grid.get((nr, pc + 1), '#')
    if cell1 == '.' and cell2 == '.':
        return True
    if cell1 == '#' or cell2 == '#':
        return False
    if cell1 == '[':
        return can_move_up_down(grid, nr, pc, dr)
    else:
        ret = True
        if cell1 == ']':
            ret = can_move_up_down(grid, nr, pc-1, dr)
        else:
            assert cell1 == '.'
        if cell2 == '[':
            ret = ret and can_move_up_down(grid, nr, pc+1, dr)
        else:
            assert cell2 == '.'
        return ret


def move_up_down(grid, pr, pc, dr):
    cell = grid[(pr, pc)]
    pc += -1 if cell == ']' else 0  # orient on left side
    nr = pr + dr
    cell1 = grid.get((nr, pc), '#')
    cell2 = grid.get((nr, pc + 1), '#')
    if cell1 == '[':
        move_up_down(grid, nr, pc, dr)
    elif cell1 == ']':
        move_up_down(grid, nr, pc-1, dr)
    if cell2 == '[':
        move_up_down(grid, nr, pc+1, dr)
    assert cell in "[].", f"unexpected cell '{cell}'"
    assert grid[(nr, pc)] == '.' and grid[(nr, pc+1)] == '.'
    grid[(nr, pc)] = '['
    grid[(nr, pc+1)] = ']'
    grid[(pr, pc)] = '.'
    grid[(pr, pc+1)] = '.'


def walk2(grid, height, width, start, moves):
    pr, pc = start
    for move in moves:
        dr, dc = direction(move)
        nr, nc = pr + dr, pc+dc
        cell = grid[(nr, nc)]
        if cell == '#':
            pass
        elif cell == '[' or cell == ']':
            if dr == 0:
                while cell == '[' or cell == ']':
                    nr, nc = nr + dr, nc + dc
                    cell = grid[(nr, nc)]
                if cell == '.':
                    move_column(grid, pr, pc, dr, dc, nr, nc)
                    pr, pc = pr + dr, pc + dc
            else:
                if can_move_up_down(grid, nr, nc, dr):
                    move_up_down(grid, nr, nc, dr)
                    grid[(pr, pc)] = '.'
                    pr, pc = pr + dr, pc + dc
                    grid[(pr, pc)] = '@'

        elif cell == '.':
            grid[(pr, pc)] = '.'
            pr, pc = nr, nc
            grid[(pr, pc)] = '@'


def process(data):
    amap, moves = data
    height, width = len(amap), len(amap[0])
    # # part 1
    grid, start = make_grid1(amap)
    walk1(grid, start, moves)
    result = calcGPS(grid)
    print("part 1:", result)
    # part 2
    grid, start = make_grid2(amap)
    width *= 2
    walk2(grid, height, width, start, moves)
    result = calcGPS(grid, box='[')
    print("part 2:", result)


def load_data(fileobj):
    grid, moves = fileobj.read().split("\n\n")
    return list(grid.split('\n')), "".join(moves.split('\n'))


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
