# http://adventofcode.com/2016/day/5
from __future__ import print_function
from hashlib import md5


def solve(prefix):
    nums = 0
    password = "        "
    for i in range(100000000):
        dig = md5((prefix + str(i)).encode('ascii')).hexdigest()
        if dig[:5] == '00000':
            if '0' <= dig[5] < '8':
                pos = int(dig[5])
                if password[pos] == ' ':
                    password = password[:pos] + dig[6] + password[pos+1:]
                    print('>' + password + '<')
                    nums += 1
                    if nums == 8:
                        break
    print(password)


if __name__ == "__main__":
    # solve('abc')
    solve('wtnhxymk')
