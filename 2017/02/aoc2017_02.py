# https://adventofcode.com/2017/day/2

def solve(lines):
    total = 0
    for line in lines:
        table = line.split()
        numbers = list(map(int, table))
        amax = max(numbers)
        amin = min(numbers)
        total += amax - amin
    print("Total = ", total)


def solve2(lines):
    total = 0
    for line in lines:
        numbers = list(map(int, line.split()))
        numbers.sort(reverse=True)
        adiv = 0
        for i, num in enumerate(numbers):
            if adiv != 0:
                break
            dividers = numbers[i+1:]
            for div in dividers:
                (x, y) = divmod(num, div)
                if y == 0:
                    adiv = x
                    total += adiv
                    break
    print("Total =", total)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()
        print("Lines count =", len(lines))
        solve2(lines)
