
def priority(op):
    if op == '(' or op == ')':
        return 0
    if op == '~':
        return 4
    if op == '&':
        return 3
    if op == '|' or op == '+':
        return 2
    if op == '>':
        return 1

def postfix(expression):
    operations = '~&|+>'
    stack = []
    out = []
    for token in expression:
        if token.isdigit() or token.isalpha():
            out.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack[-1] != '(':
                out.append(stack[-1])
                stack = stack[:-1]
            stack = stack[:-1]
        elif token in operations:
            if len(stack) > 0 and priority(token) < priority(stack[-1]):
                while len(stack) > 0 and priority(token) < priority(stack[-1]):
                    out.append(stack[-1])
                    stack = stack[-1]
                out.append(token)
            else:
                stack.append(token)
    while len(stack) > 0:
        out.append(stack[-1])
        stack = stack[:-1]