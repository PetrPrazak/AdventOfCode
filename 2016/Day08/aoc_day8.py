"""

--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an implementation of two-factor authentication after a long game of requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a nearby desk). Then, it displays a code on a little screen, and you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken everything apart and figured out how it works. Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for the screen; these instructions are your puzzle input. The screen is 50 pixels wide and 6 pixels tall, all of which start off, and is capable of three somewhat peculiar operations:

rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall off the right end appear at the left end of the row.
rotate column x=A by B shifts all of the pixels in column A (0 is the left column) down by B pixels. Pixels that would fall off the bottom appear at the top of the column.
For example, here is a simple sequence on a smaller screen:

rect 3x2 creates a small rectangle in the top-left corner:

###....
###....
.......
rotate column x=1 by 1 rotates the second column down by one pixel:

#.#....
###....
.#.....
rotate row y=0 by 4 rotates the top row right by four pixels:

....#.#
###....
.#.....
rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap back to the top:

.#..#.#
#.#....
.#.....
As you can see, this display technology is extremely powerful, and will soon dominate the tiny-code-displaying-screen market. That's what the advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display: after you swipe your card, if the screen did work, how many pixels should be lit?

Your puzzle answer was 110.

--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the font it uses, each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?

Your puzzle answer was ZJHRKCPLYJ.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

from __future__ import print_function


def print_matrix(matrix, size):
    X, Y = size
    for y in range(Y):
        line = ""
        for x in range(X):
            line += "#" if matrix[(x,y)] else ' '
        print(line)
    print("")


def solve(lines, size):

    X, Y = size
    matrix = {}
    for x in range(X):
        for y in range(Y):
            matrix[(x, y)] = 0

    for line in lines:
        line = line.strip()
        parts = line.split()

        # rect 20x1
        if parts[0] == "rect":
            addr = parts[1].split('x')
            for x in range(int(addr[0])):
                for y in range(int(addr[1])):
                    matrix[x, y] = 1
        # rotate row y=4 by 20
        elif parts[1] == "row":
            row = int(parts[2][2:])
            offset = int(parts[4])
            for _ in range(offset):
                save = matrix[(X-1,row)]
                for x in reversed(range(X-1)):
                    matrix[((x + 1) % X, row)] = matrix[(x, row)]
                matrix[(0,row)] = save
        # rotate column x=47 by 1
        elif parts[1] == "column":
            col = int(parts[2][2:])
            offset = int(parts[4])
            for _ in range(offset):
                save = matrix[(col, Y - 1)]
                for y in reversed(range(Y-1)):
                    matrix[(col, (y + 1) % Y)] = matrix[(col, y)]
                matrix[(col, 0)] = save

    print_matrix(matrix, size)
    print(sum(matrix[x] for x in matrix))


# INPUT = "aoc_day8_test.txt"
INPUT = "aoc_day8_input.txt"

if __name__ == "__main__":
    with open(INPUT) as f:
       l = f.readlines()
    # solve(l,(7,3))
    solve(l,(50,6))
