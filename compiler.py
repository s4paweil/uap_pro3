import copy

import syntax
from instruction import *


class Compiler():
    def to_code(self):
        return self.code({},0) + [halt()]

class LET(syntax.LET, Compiler):
    def code(self, rho, nl):
        l1 = Label()
        rho = self.elab_def(rho, nl)
        code_decl = []
        for decl in self.declarations:
            code_decl += decl.code(rho,nl)
        code_body = self.body.code(rho,nl)
        code_body[0].assigned_labels += [l1]
        return(
            [goto(l1)] +
            code_decl +
            code_body
        )

    def elab_def(self, rho, nl):
        rho_copy = rho.copy()
        for declaration in self.declarations:
            label = Label()
            rho_copy[str(declaration.fname)] = (label, nl)
        return rho_copy


class DECL(syntax.DECL, Compiler):
    def code(self, rho, nl):
        l_id, nl_id = rho[str(self.fname)]
        rho_copy = rho.copy()
        for index,param in enumerate(self.params):
            rho_copy[str(param)] = (index, nl+1)
        code_body = self.body.code(rho_copy, nl+1)
        code_body[0].assigned_labels += [l_id]
        return (
            code_body +
            [ireturn()]
        )


class CALL(syntax.CALL, Compiler):
    def code(self, rho, nl):
        l_id, nl_id = rho[str(self.fname)]
        code_args = []

        for arg in self.arguments:
            code_args += arg.code(rho,nl)

        return(
            code_args +
            [invoke(len(self.arguments), l_id, nl-nl_id)]
        )


class VAR(syntax.VAR, Compiler):
    def code(self, rho, nl):
        l_id, nl_id = rho[str(self.name)]
        return [load(l_id, nl - nl_id)]


class BINOP(syntax.BINOP, Compiler):
    def code(self, rho, nl):
        code_arg1 = self.arg1.code(rho, nl)
        code_arg2 = self.arg2.code(rho, nl)
        if self.operator == '+':
            code_operator = add()
        elif self.operator == '-':
            code_operator = sub()
        elif self.operator == '/':
            code_operator = div()
        elif self.operator == '*':
            code_operator = mul()
        elif self.operator == '>':
            code_operator = gt()
        elif self.operator == '<':
            code_operator = lt()
        elif self.operator == '!=':
            code_operator = neq()
        elif self.operator == '==':
            code_operator = eq()
        elif self.operator == '||':
            l1 = Label()
            l2 = Label()
            code_arg2[0].assigned_labels += [l1]
            return (
                    code_arg1 +
                    [ifzero(l1), const(1), goto(l2)] +
                    code_arg2 +
                    [nop(assigned_label=l2)]
            )
        elif self.operator == '&&':
            l1 = Label()
            l2 = Label()
            return (
                    code_arg1 +
                    [ifzero(l1), const(1)] +
                    code_arg2 +
                    [mul(), goto(l2), const(0, assigned_label=l1), nop(assigned_label=l2)]
            )
        elif self.operator == '<=':
            l1 = Label()
            l2 = Label()
            code_args = code_arg1 + code_arg2
            code_args_labeled = copy.deepcopy(code_args)
            code_args_labeled[0].assigned_labels += [l1]
            return(
                    code_args + [lt()] +
                    [ifzero(l1), const(1), goto(l2)] +
                    code_args_labeled + [eq()] +
                    [nop(assigned_label=l2)]
            )
        elif self.operator == '>=':
            l1 = Label()
            l2 = Label()
            code_args = code_arg1 + code_arg2
            code_args_labeled = copy.deepcopy(code_args)
            code_args_labeled[0].assigned_labels += [l1]
            return(
                    code_args + [gt()] +
                    [ifzero(l1), const(1), goto(l2)] +
                    code_args_labeled + [eq()] +
                    [nop(assigned_label=l2)]
            )
        else:
            code_operator = "Ungültiger Operator"

        return code_arg1 + code_arg2 + [code_operator]


class CONST(syntax.CONST, Compiler):
    def code(self, rho, nl):
        return [const(self.value)]


class BOOL(syntax.BOOL, Compiler):
    def code(self, rho, nl):
        if self.bool:
            code = [const(1)]
        else:
            code = [const(0)]
        return(
            code
        )


class ASSIGN(syntax.ASSIGN, Compiler):
    def code(self, rho, nl):
        l_id, nl_id = rho[str(self.variable)]
        code_exp = self.expression.code(rho, nl)
        return code_exp + [store(l_id, nl - nl_id), load(l_id, nl - nl_id)]


class SEQ(syntax.SEQ, Compiler):
    def code(self, rho, nl):
        code_exp1 = self.exp1.code(rho, nl)
        code_exp2 = self.exp2.code(rho, nl)
        return code_exp1 + [pop()] + code_exp2


class IF(syntax.IF, Compiler):
    def code(self, rho, nl):
        l1 = Label()
        l2 = Label()
        code_condition = self.condition.code(rho, nl)
        code_exp1 = self.exp1.code(rho, nl)
        code_exp2 = self.exp2.code(rho, nl)
        code_exp2[0].assigned_labels += [l1]

        return (
                code_condition +
                [ifzero(l1)] +
                code_exp1 +
                [goto(l2)] +
                code_exp2 +
                [nop(assigned_label=l2)]
        )


class WHILE(syntax.WHILE, Compiler):
    def code(self, rho, nl):
        l1 = Label()
        l2 = Label()
        l3 = Label()
        l4 = Label()
        code_condition = self.condition.code(rho, nl)
        code_body = self.body.code(rho, nl)
        code_body[0].assigned_labels += [l4]
        code_condition_labeled = copy.deepcopy(code_condition)
        code_condition_labeled[0].assigned_labels += [l1]
        return (
                code_condition +
                [ifzero(l3), goto(l4)] +
                code_condition_labeled +
                [ifzero(l2), pop()] +
                code_body +
                [goto(l1), const(0, assigned_label=l3), nop(assigned_label=l2)]
        )
