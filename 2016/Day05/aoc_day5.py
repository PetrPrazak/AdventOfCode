
from __future__ import print_function
import md5


def solve(prefix):

    nums = 0
    password = "        "
    for i in range(100000000):
        dig = md5.new(prefix + str(i)).hexdigest()
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
