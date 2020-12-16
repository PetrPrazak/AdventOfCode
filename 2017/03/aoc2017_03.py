# https://adventofcode.com/2017/day/3
from __future__ import print_function
import numpy
import math


def solve(num):
    print("Value =", num)
    root = math.sqrt(num)
    if root > math.floor(root):
        root += 1
    root = int(math.floor(root))
    if root % 2 == 0:
        root += 1
    radius = (root - 1)//2
    prev = root - 2
    index = num - (prev * prev)  # poradi na dane "kruznici"
    # vzdalenost na jedne strane ctverce
    indexl = (index + radius) % (root - 1)
    if indexl > radius:
        indexl = abs(indexl - radius)

    print("Path length:", indexl + radius)


def get_root(num):
    root = math.sqrt(num)
    if root > math.floor(root):
        root += 1
    root = math.floor(root)
    if root % 2 == 0:
        root += 1
    return int(root)


def coord(num):
    if num <= 1:
        return 0, 0

    root = get_root(num)
    radius = (root - 1)//2
    prev = root - 2
    index = num - (prev * prev)                # poradi na dane "kruznici"
    indexl = (index + radius) % (root - 1)     # vzdalenost na jedne strane ctverce
    indexl -= radius

    start = root - 1
    corners = [start, 2*start, 3*start, 4*start]

    if index <= corners[0]:
        x = radius
        y = index + radius - corners[0]
    elif index <= corners[1]:
        x = corners[1] - index - radius
        y = radius
    elif index < corners[2]:
        x = -radius
        y = corners[2] - index - radius
    else:
        x = index + radius - corners[3]
        y = -radius

    return x, y


def adj_simple(coord):
    x, y = coord
    return [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
            (x - 1, y),                 (x + 1, y),
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]


numpy.set_printoptions(threshold='nan')


def solve2(num, maxnum):
    root = get_root(num)
    arr = numpy.zeros((root+1, root+1), numpy.int32)
    radius = (root - 1)//2
    arr[radius][radius] = 1     # starting point
    for anum in range(2, num+1):
        crd = coord(anum)
        asum = sum(arr[radius + x][radius + y] for (x, y) in adj_simple(crd))
        i, j = crd
        arr[i + radius][j + radius] = asum
        if asum > maxnum:
            print(asum)
            break
    print(arr)


if __name__ == "__main__":
    # solve(10)
    # solve(12)
    # solve(1024)
    solve(277678)
    solve2(60, 277678)
