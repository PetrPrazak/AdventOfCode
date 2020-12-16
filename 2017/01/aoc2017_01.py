# https://adventofcode.com/2017/day/1

def solve(line, step):
    sum = 0
    for i in range(len(line)):
        if line[i] == line[(i + step) % len(line)]:
            sum += int(line[i])
    print("Sum is", sum)


if __name__ == "__main__":
    with open("input.txt") as f:
        line = f.readline().strip()
        solve(line, 1)
        solve(line, len(line)//2)
