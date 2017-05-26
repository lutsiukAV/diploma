def priority(op):
    ops = {
        '(': 0,
        ')': 0,
        '>': 1,
        '+': 2,
        '|': 2,
        '&': 3,
        '~': 4
    }
    return ops[op]


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
                    stack = stack[:-1]
                stack.append(token)
            else:
                stack.append(token)
    while len(stack) > 0:
        out.append(stack[-1])
        stack = stack[:-1]
    return out


def generate(postfix):
    vars = ''
    for token in postfix:
        if token.isalpha() and not token in vars:
            vars += token
    vars_number = len(vars)
    sets = [()]
    for i in range(vars_number):
        step0 = []
        step1 = []
        for set in sets:
            step0 = [(0,) + elem for elem in sets]
            step1 = [(1,) + elem for elem in sets]
        sets = step0 + step1
    return sets, vars


def calculate(postfix, expression):
    res = []
    s_p = []
    s_e = []
    for i in range(len(postfix)):
        t_p = postfix[i]
        t_e = expression[i]
        if t_p.isalpha():
            s_p.append(t_p)
            s_e.append(t_e)
        else:
            if t_p == '~':
                op_p = s_p[-1]
                s_p = s_p[:-1]
                op_e = s_e[-1]
                s_e = s_e[:-1]
                r_p = '~' + op_p
                r_e = 1 - op_e
                s_p.append(r_p)
                s_e.append(r_e)
                res.append([r_p, r_e])
            elif t_p == '+':
                op2_p = s_p[-1]
                s_p = s_p[:-1]
                op2_e = s_e[-1]
                s_e = s_e[:-1]
                op1_p = s_p[-1]
                s_p = s_p[:-1]
                op1_e = s_e[-1]
                s_e = s_e[:-1]
                r_p = op1_p + '+' + op2_p
                r_e = 0
                if op1_e != op2_e:
                    r_e = 1
                s_p.append(r_p)
                s_e.append(r_e)
                res.append([r_p, r_e])
            elif t_p == '|':
                op2_p = s_p[-1]
                s_p = s_p[:-1]
                op2_e = s_e[-1]
                s_e = s_e[:-1]
                op1_p = s_p[-1]
                s_p = s_p[:-1]
                op1_e = s_e[-1]
                s_e = s_e[:-1]
                r_p = op1_p + '|' + op2_p
                r_e = 1
                if op1_e == 0 and op2_e == 0:
                    r_e = 0
                s_p.append(r_p)
                s_e.append(r_e)
                res.append([r_p, r_e])
            elif t_p == '&':
                op2_p = s_p[-1]
                s_p = s_p[:-1]
                op2_e = s_e[-1]
                s_e = s_e[:-1]
                op1_p = s_p[-1]
                s_p = s_p[:-1]
                op1_e = s_e[-1]
                s_e = s_e[:-1]
                r_p = op1_p + '&' + op2_p
                r_e = 0
                if op1_e == 1 and op2_e == 1:
                    r_e = 1
                s_p.append(r_p)
                s_e.append(r_e)
                res.append([r_p, r_e])
            elif t_p == '>':
                op2_p = s_p[-1]
                s_p = s_p[:-1]
                op2_e = s_e[-1]
                s_e = s_e[:-1]
                op1_p = s_p[-1]
                s_p = s_p[:-1]
                op1_e = s_e[-1]
                s_e = s_e[:-1]
                r_p = op1_p + '>' + op2_p
                r_e = 1
                if op1_e == 1 and op2_e == 0:
                    r_e = 0
                s_p.append(r_p)
                s_e.append(r_e)
                res.append([r_p, r_e])
    return res


def subs(postfix, st):
    res = []
    for token in postfix:
        if token.isalpha():
            res.append(st[token])
        else:
            res.append(token)
    return calculate(postfix, res)


def base(postfix, sets, var):
    res = []
    for st in sets:
        substitution = {}
        input = []
        for i in range(len(var)):
            substitution[var[i]] = st[i]
            input.append([var[i], st[i]])
        res.append(input + subs(postfix, substitution))
    return res


def tree(postfix):
    stack = []
    for token in postfix:
        if token.isalpha():
            stack.append(token)
        else:
            if token == '~':
                op = stack[-1]
                stack = stack[:-1]
                stack.append([token, op])
            else:
                op2 = stack[-1]
                stack = stack[:-1]
                op1 = stack[-1]
                stack = stack[:-1]
                stack.append([token, op1, op2])
    return stack[-1]


def transform(sign, tree):
    if type(tree) == type(''):
        if sign == '|-':
            return ['+' + tree], [sign, tree, []]
        elif sign == '-|':
            return ['-' + tree], [sign, tree, []]
    elif type(tree) == type([]):
        if tree[0] == '~':
            if sign == '|-':
                res, sub_expr = transform('-|', tree[1])
                return res, [sign, '~' + sub_expr[1], [sub_expr]]
            elif sign == '-|':
                res, sub_expr = transform('|-', tree[1])
                return res, [sign, '~' + sub_expr[1], [sub_expr]]
        elif tree[0] == '|':
            if sign == '|-':
                res1, sub_expr1 = transform('|-', tree[1])
                res2, sub_expr2 = transform('|-', tree[2])
                return res1 + res2, [sign, sub_expr1[1] + '|' + sub_expr2[1], [sub_expr1, sub_expr2]]
            elif sign == '-|':
                res1, sub_expr1 = transform('-|', tree[1])
                res2, sub_expr2 = transform('-|', tree[2])
                return res1 + res2, [sign, sub_expr1[1] + '|' + sub_expr2[1], [sub_expr1, sub_expr2]]
        elif tree[0] == '&':
            if sign == '|-':
                res1, sub_expr1 = transform('|-', tree[1])
                res2, sub_expr2 = transform('|-', tree[2])
                return res1 + res2, [sign, sub_expr1[1] + '&' + sub_expr2[1], [sub_expr1, sub_expr2]]
            elif sign == '-|':
                res1, sub_expr1 = transform('-|', tree[1])
                res2, sub_expr2 = transform('-|', tree[2])
                return res1 + res2, [sign, sub_expr1[1] + '&' + sub_expr2[1], [sub_expr1, sub_expr2]]
        elif tree[0] == '>':
            if sign == '|-':
                res1, sub_expr1 = transform('-|', tree[1])
                res2, sub_expr2 = transform('|-', tree[2])
                return res1 + res2, [sign, sub_expr1[1] + '>' + sub_expr2[1], [sub_expr1, sub_expr2]]
            elif sign == '-|':
                res1, sub_expr1 = transform('|-', tree[1])
                res2, sub_expr2 = transform('-|', tree[2])
                return res1 + res2, [sign, sub_expr1[1] + '>' + sub_expr2[1], [sub_expr1, sub_expr2]]


def solve_seq(left, right):
    l, sl = transform('|-', tree(left))
    r, sr = transform('-|', tree(right))
    tr = ['-|', sl[1] + '>' + sr[1], [sl, sr]]
    res = l + r
    buckets = {}
    for item in res:
        key = item[1:]
        try:
            buckets[key].append(item[0])
        except:
            buckets[key] = [item[0]]
    for key in buckets:
        if '-' in buckets[key] and '+' in buckets[key]:
            return True, tree, None
    counter_example = []
    for key in sorted(buckets):
        if buckets[key][0] == '-':
            counter_example.append([key, 0])
        else:
            counter_example.append([key, 1])
    return False, tree, counter_example
