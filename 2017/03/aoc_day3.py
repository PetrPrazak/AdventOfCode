"""

--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while
spiraling outward. For example, the first few squares are allocated like this:

37  36  35  34  33  32  31
38  17  16  15  14  13  30
39  18   5   4   3  12  29
40  19   6   1   2  11  28
41  20   7   8   9  10  27
42  21  22  23  24  25  26
43  44  45  46  47  48  49 50

   floor(sqrt(x))^2

 1, 9,25,49,81,121
 1, 3, 5, 7, 9, 11
 0, 1, 2, 3, 4,  5


 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
 3, 0, 1, 2, 3, 0, 1, 2, 3,  0,  1,  2,  3,  0,  1,  2
 1, 0, 1, 2, 1, 0, 1, 2, 1,  0,  1,  2,  1,  0,  1,  2


index = index % 4
index -= radius // 2
index = abs(index)




While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the
location of the only access port for this memory system) by programs that can only move up, down, left,
or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle input is 277678.



"""
from __future__ import print_function
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
    index = num - (prev * prev) # poradi na dane "kruznici"
    indexl = (index + radius) % (root - 1)     # vzdalenost na jedne strane ctverce
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
    x,y = coord
    return [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
            (x - 1, y),                 (x + 1, y), 
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]


import numpy
numpy.set_printoptions(threshold='nan')


def solve2(num, maxnum):
    root = get_root(num)
    arr = numpy.zeros((root+1, root+1), numpy.int32 )
    radius = (root - 1)//2
    arr[radius][radius] = 1     # starting point
    for anum in range(2,num+1):
        crd = coord(anum)
        asum = sum(arr[radius + x][radius + y] for (x,y) in adj_simple(crd))
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
