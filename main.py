import re
import sys
from collections import deque

import infix_to_postfix_api

var_dict = {}
operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '^': lambda a, b: a ** b
}


def main():
    expression = input().strip()
    while True:
        if is_command(expression):
            command = commands.get(expression)
            command() if command is not None else print('Unknown command')
        elif '=' in expression:
            try:
                pair = expression.replace(' ', '').split('=')
                if len(pair) != 2:
                    raise ValueError
                upd_dict_with_var(pair[0], pair[1])
            except KeyError:
                print('Unknown variable')
            except NameError:
                print('Invalid identifier')
            except ValueError:
                print('Invalid assignment')
        elif len(expression) > 0:
            try:
                postfix_queue = infix_to_postfix_api.parse(expression)
                print(calc_postfix_queue(postfix_queue))
            except (ArithmeticError, ValueError, IndexError) as err:
                print('Invalid expression')
                print(err)
            except (KeyError, NameError):
                print('Unknown variable')
        expression = input()


def solve(expression: str, **variables):
    if variables:
        var_dict.update(variables)
    return calc_postfix_queue(infix_to_postfix_api.parse(expression))


def calc_postfix_queue(queue: deque):
    stack = deque()
    i = 0
    while queue:
        elem = queue.popleft()
        if i == 166:
            i = i
        if elem not in infix_to_postfix_api.OPERATORS:
            if is_var(elem):
                if elem in var_dict:
                    elem = var_dict[elem]
                else:
                    raise NameError
            stack.append(float(elem))
        else:
            b = stack.pop()
            a = stack.pop()
            var = operations[elem](a, b)
            stack.append(var)
        i += 1
    result = stack.pop()
    if result is complex or float:  # may produce complex numbers
        return result
    elif result // 1 == result:
        return int(result)  # return as int if it has no fraction


def upd_dict_with_var(key: str, value):
    if not is_var(key):
        raise NameError
    if is_var(value):  # in case there is var to var assignment
        value = var_dict[value]
    else:  # no need in float type without fractional part
        value = int(value) if float(value) == int(value) else float(value)
    var_dict[key] = value


def is_var(var: str):  # check if variable name isn't empty and consists of latin letters only
    return False if len(var) == 0 or not re.compile("^[a-zA-Z]+$").search(var) else True


def is_command(expression_: str):
    return True if expression_ and expression_.strip()[0] == '/' else False


def exit_():
    print('Bye!')
    sys.exit()


commands = {
    '/exit': exit_,
    '/help': lambda: print('''
This program calculates math expressions

Available operands:
    - integer numbers
    - floating numbers
    - variables (variable must be declared before using)

Available operators:
    '+' - addition
    '-' - subtraction
    '*' - multiplication
    '/' - division
    '^' - exponentiation

Available commands:
    '/exit' - stops program running
    '/help' - shows manual

Variable declaration syntax:
    variable_name = number
    - variable_name must consist of english letters only
    - variable_name is case sensitive
    - number may be an integer or a float number

Other syntax peculiarities:
    - calculation is insensitive to tabs and spaces in expression
    - multiple '+' and '-' signs between operations are supported
''')
}


if __name__ == '__main__':
    main()
