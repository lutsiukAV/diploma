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
                    stack = stack[:-1]
                stack.append(token)
            else:
                stack.append(token)
    while len(stack) > 0:
        out.append(stack[-1])
        stack = stack[:-1]
    return out


def generate(pstfx):
    vars = ""
    for p in pstfx:
        if p.isalpha() and not p in vars:
            vars += p
    totalvars = len(vars)
    sets = [()]
    for i in range(totalvars):
        step0 = []
        step1 = []
        for s in sets:
            step0 = [(0,) + elem for elem in sets]
            step1 = [(1,) + elem for elem in sets]
        sets = step0 + step1
    return sets, vars


def calculate(pstfx, expression):
    res = []
    s_p = []
    s_e = []
    for i in range(len(pstfx)):
        t_p = pstfx[i]
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
                res.append((r_p, r_e))
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
                res.append((r_p, r_e))
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
                res.append((r_p, r_e))
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
                res.append((r_p, r_e))
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
                res.append((r_p, r_e))
    return res

def subs(pstfx, subst):
    res = []
    for p in pstfx:
        if p.isalpha():
            res.append(subst[p])
        else:
            res.append(p)
    return calculate(pstfx, res)

def base(pstfx, sets, vars):
    for s in sets:
        res = {}
        for i in range(len(vars)):
            res[vars[i]] = s[i]
        subs(pstfx, res)



