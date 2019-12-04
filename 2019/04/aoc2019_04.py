# https://adventofcode.com/2019/day/04

from __future__ import print_function
from collections import Counter


def filter_password1(num):
    digits = [int(d) for d in str(num)]
    prev = 0
    for d in digits:
        if d < prev:
            return False
        prev = d
    return len(set(digits)) < len(digits)


def filter_password2(num):
    digits = [int(d) for d in str(num)]
    prev = 0
    for d in digits:
        if d < prev:
            return False
        prev = d
    c = Counter(digits)
    if len(c.keys()) == len(digits):
        return False
    for (_, count) in c.items():
        if count is 2:
            return True
    return False


def test1():
    assert filter_password1(111111) is True
    assert filter_password1(223450) is False
    assert filter_password1(123789) is False


def test2():
    assert filter_password2(112233) is True
    assert filter_password2(123444) is False
    assert filter_password2(111122) is True


def main():
    # part 1
    count1 = count2 = 0
    for num in range(246540, 787419):
        if filter_password1(num):
            count1 += 1
        if filter_password2(num):
            count2 += 1
    print(count1)  # 1063
    print(count2)  # 686


if __name__ == "__main__":
    test1()
    test2()
    main()
