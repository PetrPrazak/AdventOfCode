# https://adventofcode.com/2022/day/17
from pathlib import Path
from collections import defaultdict
import time


PIECE_1 = [(0, 0), (1, 0), (2, 0), (3, 0)]
PIECE_2 = [(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)]
PIECE_3 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
PIECE_4 = [(0, 0), (0, 1), (0, 2), (0, 3)]
PIECE_5 = [(0, 0), (1, 0), (0, 1), (1, 1)]

# shape, height
PIECES = [(PIECE_1, 1), (PIECE_2, 3), (PIECE_3, 3), (PIECE_4, 4), (PIECE_5, 2)]


def drop_piece():
    while True:
        yield from enumerate(PIECES)


def flow(stream):
    while True:
        for m, j in enumerate(stream):
            yield m, -1 if j == '<' else 1


def is_free(chamber, x, y):
    return 0 <= x < 7 and y >= 0 and (x, y) not in chamber


def piece_can_fit(chamber, piece, pos_x, pos_y):
    return all(is_free(chamber, pos_x + x, pos_y + y) for x, y in piece)


def place_piece(chamber,  piece, px, py):
    chamber.update({(px+x, py+y) for x, y in piece})


def print_chamber(chamber):
    max_y = max(y for _, y in chamber)
    for row in range(max_y, -1, -1):
        print('|', end='')
        print(''.join('#' if (x, row) in chamber else ' ' for x in range(7)), end='')
        print('|')
    print(f"+{'-'*7}+")


def play(stream, max_pieces=2022):
    max_level = 0
    pieces_count = 0
    chamber = set()
    gen_piece = drop_piece()
    gen_jet = flow(stream)
    seen = defaultdict(list)
    while pieces_count < min(max_pieces, 10000):
        piece, (shape, piece_height) = next(gen_piece)
        pieces_count += 1
        last_pos = pos = 2, max_level + 3
        while True:
            # 1. check horiz. movement
            move, horiz = next(gen_jet)
            pos = pos[0] + horiz, pos[1]
            if not piece_can_fit(chamber, shape, *pos):
                pos = last_pos
            last_pos = pos
            # 2. try to drop
            pos = pos[0], pos[1] - 1
            if not piece_can_fit(chamber, shape, *pos):
                break
            last_pos = pos

        place_piece(chamber, shape, *last_pos)
        max_level = max(max_level, last_pos[1] + piece_height)
        if max_level > 20:
            state = make_state(chamber, max_level-1)
            key = (state, move, piece)
            seen[key].append((pieces_count, max_level))
            if len(seen[key]) > 1:
                p1, h1 = seen[key][-2]
                p2, h2 = seen[key][-1]
                cycle = p2 - p1
                quot, rem = divmod(max_pieces - p1, cycle)
                if rem == 0:
                    return quot * (h2 - h1) + h1
    return max_level


def row_bits(chamber, row):
    s = 0
    for col in range(7):
        s |= int((col, row) in chamber)
        s <<= 1
    return s


def make_state(chamber, level):
    state = tuple(row_bits(chamber, row)
                  for row in range(level, level - 21, -1))
    return state


def process(data):
    # part 1
    result = play(data, 2022)
    print("part 1:", result)
    # part 2
    part2_pieces = 1_000_000_000_000
    result = play(data, part2_pieces)
    print("part 2:", result)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(f.read())
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    main("test.txt")
    main()
