# https://adventofcode.com/2020/day/18
from __future__ import print_function
from collections import deque
from pprint import pprint
from enum import Enum
from string import whitespace, digits
import operator


class Token(Enum):
    NUM = 0
    LPAREN = 1
    RPAREN = 2
    OP = 3


def get_token(line):
    i = 0
    while i < len(line):
        while line[i] in whitespace:
            i += 1
        if i == len(line):
            break
        char = line[i]
        i += 1
        if char == '(':
            yield Token.LPAREN, None
        elif char == ')':
            yield Token.RPAREN, None
        elif char == '*':
            yield Token.OP, operator.mul
        elif char == '+':
            yield Token.OP, operator.add
        elif char in digits:
            # number
            j = i
            while j < len(line) and line[j] in digits:
                j += 1
            num = int(line[i-1:j])
            i = j
            yield Token.NUM, num
        else:
            assert False, f"unexpected char '{char}' at {i}: '{line[i:]}'"
    # required for the conversion to RPN
    yield Token.RPAREN, None


# precedence - map OP -> priority

def convert_to_postfix(lexer, precendence=None):
    out = []
    stack = deque()
    stack.append((Token.LPAREN, None))
    while stack:
        for token in lexer:
            kind, val = token
            if kind == Token.NUM:
                out.append(token)
            elif kind == Token.OP:
                while ((stacktoken := stack.pop())[0] == Token.OP
                       and (precendence is None
                            or precendence[stacktoken[1]] > precendence[val])):
                    out.append(stacktoken)
                stack.append(stacktoken)  # put back non-op
                stack.append(token)
            elif kind == Token.LPAREN:
                stack.append(token)
            elif kind == Token.RPAREN:
                while (token := stack.pop())[0] != Token.LPAREN:
                    out.append(token)
            else:
                assert False, f"Unexpected token {token}"
    return out


def print_postfix(tokens):
    for t in tokens:
        if t[0] == Token.NUM:
            print(t[1], end=' ')
        else:
            if t[1] == operator.add:
                print("+", end=" ")
            elif t[1] == operator.mul:
                print("*", end=" ")
    print()


def eval_rpn(tokens):
    pos = 0
    while len(tokens) > 1:
        while pos < len(tokens) and tokens[pos][0] == Token.NUM:
            pos += 1
        token, op = tokens[pos]
        assert token == Token.OP
        l, r = tokens[pos-2:pos]
        tokens[pos-2] = Token.NUM, op(l[1], r[1])
        del tokens[pos - 1:pos+1]
        pos -= 1
    return tokens[0][1]


def process(data):
    # part 1
    acc = sum(eval_rpn(convert_to_postfix(get_token(l))) for l in data)
    print("part 1:", acc)
    # part 2
    precendence = {operator.add: 1, operator.mul: 0}
    acc = sum(eval_rpn(convert_to_postfix(get_token(l), precendence))
              for l in data)
    print("part 2:", acc)


def load_data(fileobj):
    return [line.rstrip() for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
