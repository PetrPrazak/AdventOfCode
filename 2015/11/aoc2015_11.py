# http://adventofcode.com/2015/day/9
from __future__ import print_function
from string import ascii_lowercase


def pwd_inc(pwd):
    pwd_list = list(pwd)
    idx = len(pwd_list) - 1
    increment = True
    while idx >= 0:
        if increment:
            digit = pwd_list[idx]
            if digit == 'z':
                digit = 'a'
            else:
                digit = chr(ord(digit) + 1)
                increment = False
            pwd_list[idx] = digit
        idx -= 1
    return ''.join(pwd_list).rjust(8, 'a')


triplets = [ascii_lowercase[idx:idx+3]
            for idx in range(len(ascii_lowercase) - 2)]
pairs = [c * 2 for c in ascii_lowercase]


def pwd_valid(pwd):
    if 'i' in pwd or 'l' in pwd:
        return False
    valid = any(triplet in pwd for triplet in triplets)
    if not valid:
        return False
    pairs_count = sum(1 if pair in pwd else 0 for pair in pairs)
    return pairs_count > 1


def pwd_skip(pwd, letter):
    idx = pwd.find(letter)
    if idx == -1:
        return pwd
    pwd = pwd[:idx] + chr(ord(letter)+1)
    return pwd.ljust(8, 'a')


def get_next_pwd(pwd):
    while True:
        pwd = pwd_inc(pwd)
        if pwd_valid(pwd):
            return pwd
        pwd = pwd_skip(pwd, 'i')
        pwd = pwd_skip(pwd, 'l')


def process(pwd):
    print(pwd)
    next_pwd = get_next_pwd(pwd)
    print("Part 1:", next_pwd)
    next_pwd = get_next_pwd(next_pwd)
    print("Part 2:", next_pwd)


def test():
    process("abcdefgh")  # -> abcdffaa
    process("ghijklmn")  # -> ghjaabcc


def main():
    process("hepxcrrq")


if __name__ == "__main__":
    # test()
    main()
