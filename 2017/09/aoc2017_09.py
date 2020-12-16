# https://adventofcode.com/2017/day/9

def count_group(word):
    level = 0
    sum = 0
    ingarb = False
    pos = 0
    end = len(word)
    garb = 0
    while pos < end:
        c = word[pos]
        if c == '!':
            pos += 1
        else:
            if ingarb and c != '>':
                garb += 1
            if c == '<':
                ingarb = True
            elif c == '>':
                if ingarb:
                    ingarb = False
            elif c == "{":
                if not ingarb:
                    level += 1
                    sum += level
            elif c == '}':
                if not ingarb:
                    level -= 1

        pos += 1

    print(sum)
    print(garb)


if __name__ == "__main__":
    count_group('{{<!!>},{<!!>},{<!!>},{<!!>}}')
    with open("input.txt") as f:
        l = f.read()
        count_group(l)
