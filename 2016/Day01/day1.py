"""
-- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
R5, L5, R5, R3 leaves you 12 blocks away.
How many blocks away is Easter Bunny HQ?

Your puzzle answer was 353.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?

Your puzzle answer was 152.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

from __future__ import print_function

def get_new_dir(code, direction):
    if  code == "R":
        direction += 1
        if direction == 4: 
            direction = 0
    else:
        direction -= 1
        if direction == -1: 
            direction = 3
    return direction


def get_new_pos(pos, direction, steps):
    x, y = pos
    if direction == 0:
        y += steps
    elif direction == 1:
        x += steps
    elif direction == 2:
        y -= steps
    else: # dir 3
        x -= steps
    return (x,y)

def get_all_new_pos(pos, direction, steps):
    x, y = pos

    positions = list()
    for step in range(1,steps+1):
        if direction == 0:
            y += 1
        elif direction == 1:
            x += 1
        elif direction == 2:
            y -= 1
        else: # dir 3
            x -= 1
        positions.append((x,y))
    return positions


def solve(line, part):
    codes = line.split(",")
    direction = 0  # 0 North 1 East 2 South 3 West
    visits = {}
    pos = (0,0)
    count = 0
    visits[pos] = count
    for code in codes:
        code = code.strip()
        instr = code[0]
        steps = int(code[1:])
        direction = get_new_dir(instr[0], direction)
        if part == 1:
            pos = get_new_pos(pos, direction, steps)
        else:
            count += 1
            listpos = get_all_new_pos(pos, direction, steps)
            for apos in listpos:                
                if apos in visits:
                    print("Been here before: ", apos)
                    x,y = apos
                    print("Distance to center:", abs(x) + abs(y))
                    return
                visits[apos] = count
            pos = listpos[-1]

    x,y = pos
    print("Distance to center:", abs(x) + abs(y))


if __name__ == "__main__":
    with open("day1_input.txt") as f:
        line = f.readline().strip()
        solve(line,1)
        solve(line,2)
