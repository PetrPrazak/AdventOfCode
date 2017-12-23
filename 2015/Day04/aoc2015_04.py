"""
http://adventofcode.com/2015/day/4
"""
from __future__ import print_function
from hashlib import md5

inputdata = "iwrupvqb"

try:
    xrange
except NameError:
    xrange = range


def find_first_md5_zeros(zeros):
    prefix = "0" * zeros
    for i in xrange(100000000):
        data = inputdata + str(i)
        s = md5(data.encode('ascii')).hexdigest()
        if s[:zeros] == prefix:
            return i

    return 0


def main():
    print(find_first_md5_zeros(5))
    print(find_first_md5_zeros(6))


if __name__ == "__main__":
    main()
