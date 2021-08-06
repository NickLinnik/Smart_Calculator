import re
from collections import deque

OPERATORS = {'+', '-', '*', '/', '(', ')', '^'}
MULT_DIV_EXP_L_PARENTHESIS = {'*', '/', '^', '('}
PLUS_AND_MINUS = {'+', '-'}


def parse(expression: str):
    clean_expression = get_expression_with_single_operators(expression)
    infix_queue = get_infix_queue(clean_expression)
    stack = deque()
    queue_postfix = deque()
    PRIORITY = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
    while infix_queue:
        elem = infix_queue.popleft()
        if elem not in OPERATORS:
            queue_postfix.append(elem)
        elif elem == '(':
            stack.append(elem)
        elif elem == ')':
            while stack and stack[-1] != '(':
                queue_postfix.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and PRIORITY[elem] <= PRIORITY[stack[-1]]:
                queue_postfix.append(stack.pop())
            stack.append(elem)

    while stack:
        elem = stack.pop()
        if elem == '(':
            raise ArithmeticError
        queue_postfix.append(elem)
    return queue_postfix


def get_infix_queue(expression: str):
    expression_list = re.split('([+\\-*/^()])', expression)  # split by operators
    expression_list = [x for x in expression_list if x != '']
    size = len(expression_list)
    i = 0
    while i < size:
        if expression_list[i] == '(' and expression_list[i + 1] in PLUS_AND_MINUS and expression_list[i + 2] == '(':
            expression_list[i + 1:i + 2] = ['-1', '*']
            size = len(expression_list)
        elif expression_list[i] in MULT_DIV_EXP_L_PARENTHESIS and expression_list[i + 1] in PLUS_AND_MINUS:
            expression_list[i + 2] = expression_list[i + 1] + expression_list[i + 2]
            del expression_list[i + 1]
            size = len(expression_list)
        i += 1
    queue = deque(expression_list)  # get rid of the empty elements
    if queue[0] == '-':  # '-' might be the first element, it should be a part of the first operand then
        queue[1] = '-' + queue[1]
        queue.remove('-')
    return queue


# get rid of all whitespaces and additional operators to get strict sequence of operands and operators
def get_expression_with_single_operators(old_expression: str):
    if re.search('\\d+(.\\d+)? +\\d+(.\\d+)?', old_expression):
        raise ValueError
    # regex for checking operands without operators between them (only spaces)
    old_expression = old_expression.replace(' ', '')  # further calculations need expression without spaces
    while True:
        new_expression: str = old_expression. \
            replace('++', '+'). \
            replace('--', '+'). \
            replace('+-', '-'). \
            replace('-+', '-')
        if old_expression == new_expression:
            break
        old_expression = new_expression
    return new_expression


if __name__ == '__main__':
    print(' '.join(parse(input())))
