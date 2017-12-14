from __future__ import print_function

"""
http://adventofcode.com/2016/day/3

--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side. For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

Your puzzle answer was 982.

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?

Your puzzle answer was 1826.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

def is_triangle(triangle):
    return triangle[0] + triangle[1] > triangle[2]


def solve(lines):
    sum = 0
    for line in lines:
        triangle = sorted(int(x) for x in line.split())
        if is_triangle(triangle):
            sum += 1
    print(sum)


def solve2(lines):
    sum = 0
    for i in range(0,len(lines),3):
        line1 = [int(x) for x in lines[i].split()]
        line2 = [int(x) for x in lines[i+1].split()]
        line3 = [int(x) for x in lines[i+2].split()]
        for t in range(0,3):
            triangle = sorted([line1[t],line2[t],line3[t]])
            if is_triangle(triangle):
                sum += 1
    print(sum)


if __name__ == "__main__":
    with open("day3_input.txt") as f:
        lines = f.readlines()
        solve(lines)
        solve2(lines)
 