# https://adventofcode.com/2022/day/8
from pathlib import Path


def make_visibility_map(grid):
    visible = set()
    size_y, size_x = len(grid), len(grid[0])

    def scan_horizontally(range_x, range_y, ):
        for j in range_y:
            prev = -1
            for i in range_x:
                tree = grid[j][i]
                if tree > prev:
                    visible.add((j, i))
                if tree == 9:
                    break
                prev = max(tree, prev)

    def scan_vertically(range_x, range_y):
        for i in range_x:
            prev = -1
            for j in range_y:
                tree = grid[j][i]
                if tree > prev:
                    visible.add((j, i))
                if tree == 9:
                    break
                prev = max(tree, prev)

    scan_horizontally(range(size_x), range(size_y))
    scan_horizontally(range(size_x-1, -1, -1), range(size_y))
    scan_vertically(range(size_x), range(size_y))
    scan_vertically(range(size_x), range(size_y-1, -1, -1))

    return visible


def scenic_score(grid):
    score = dict()
    size_y, size_x = len(grid), len(grid[0])

    def seen_horizontally(tree, j, range_x):
        seen = 0
        for x in range_x:
            seen += 1
            if grid[j][x] >= tree:
                break
        return seen

    def seen_vertically(tree, i, range_y):
        seen = 0
        for y in range_y:
            seen += 1
            if grid[y][i] >= tree:
                break
        return seen

    # trees on the edges have score 0
    for j in range(1, size_y-1):
        for i in range(1, size_x-1):
            tree = grid[j][i]
            tree_score = seen_horizontally(tree, j, range(i+1, size_x))
            tree_score *= seen_horizontally(tree, j, range(i-1, -1, -1))
            tree_score *= seen_vertically(tree, i, range(j+1, size_y))
            tree_score *= seen_vertically(tree, i, range(j-1, -1, -1))
            score[(j, i)] = tree_score
    return score


def process(data):
    # part 1
    map = make_visibility_map(data)
    result = len(map)
    print("part 1:", result)
    # part 2
    seen = scenic_score(data)
    result = max(seen.values())
    print("part 2:", result)


def parse_line(line):
    return list(map(int, line.rstrip()))


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
