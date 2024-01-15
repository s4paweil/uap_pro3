class IDotExporter:
    def to_dot(self, dot, extensive):
        pass

    def getNodeId(self):
        return str(self.pp)

    def create_node(self, dot, id, label):
        dot.node(id, label, color='lightblue2', style='filled')

    def create_leaf(self, dot, id, label):
        dot.node(id, label, shape='box', color='chartreuse2', style='filled')

    def create_edge(self, dot, source, target):
        dot.edge(source, target)

    def create_minimal_node(self, dot, id, label, color):
        dot.node(id, label, shape='plaintext', fontcolor=color)



class EXPRESSION(IDotExporter):
    ppcount=0

    def __init__(self):
        self.pp=EXPRESSION.ppcount
        EXPRESSION.ppcount=EXPRESSION.ppcount+1

    def copy(self):
        return EXPRESSION()

    def allNodes(self):
        ret = [self]
        for node in (self.__getattribute__(a) for a in self.__dict__.keys()):
            if isinstance(node, EXPRESSION):
                ret = ret + node.allNodes()
            if isinstance(node, list):
                for n in node:
                    if isinstance(n, EXPRESSION):
                        ret = ret + n.allNodes()
        return ret

class LET(EXPRESSION):
    def __init__(self, declarations, body):
        super().__init__()
        self.declarations=declarations
        self.body=body

    def __str__(self): return "let " \
        +','.join([ str(decl) for decl in self.declarations ]) \
        + " in " + str(self.body)

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "LET")
            self.create_leaf(dot, "let_" + self.getNodeId(), "let")
            self.create_edge(dot, self.getNodeId(), "let_" + self.getNodeId())
            for index, decl in enumerate(self.declarations):
                self.create_edge(dot, self.getNodeId(), decl.to_dot(dot, True))
                # Füge ein ","-Blatt zwischen den Deklarationen ein
                if index < len(self.declarations) - 1:
                    self.create_leaf(dot, "comma_" + self.getNodeId() + str(index), "comma")
                    self.create_edge(dot, self.getNodeId(), "comma_" + self.getNodeId() + str(index))
            self.create_leaf(dot, "in_" + self.getNodeId(), "in")
            self.create_edge(dot, self.getNodeId(), "in_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.body.to_dot(dot, True))
        else:
            self.create_minimal_node(dot, self.getNodeId(), "LET", 'brown1')
            for decl in self.declarations:
                self.create_edge(dot, self.getNodeId(), decl.to_dot(dot, False))
            self.create_edge(dot, self.getNodeId(), self.body.to_dot(dot, False))
        return self.getNodeId()

class DECL(EXPRESSION):
    def __init__(self, fname, params, body):
        super().__init__()
        self.fname=fname
        self.params=params
        self.body=body

    def __str__(self): return self.fname+"(" \
        +','.join([ str(param) for param in self.params ]) \
        +"){ "+str(self.body)+" }"

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "DECL")
            self.create_leaf(dot, "id_" + self.getNodeId(), "id(" + self.fname + ")")
            self.create_edge(dot, self.getNodeId(), "id_" + self.getNodeId())
            self.create_leaf(dot, "lp_" + self.getNodeId(), "(")
            self.create_edge(dot, self.getNodeId(), "lp_" + self.getNodeId())
            for index, param in enumerate(self.params):
                self.create_edge(dot, self.getNodeId(), param.to_dot(dot, True))
                # Füge ein ","-Blatt zwischen den Deklarationen ein
                if index < len(self.params) - 1:
                    self.create_leaf(dot, "comma_" + self.getNodeId() + str(index), "comma")
                    self.create_edge(dot, self.getNodeId(), "comma_" + self.getNodeId() + str(index))
            self.create_leaf(dot, "rp_" + self.getNodeId(), ")")
            self.create_edge(dot, self.getNodeId(), "rp_" + self.getNodeId())
            self.create_leaf(dot, "lb_" + self.getNodeId(), "{")
            self.create_edge(dot, self.getNodeId(), "lb_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.body.to_dot(dot, True))
            self.create_leaf(dot, "rb_" + self.getNodeId(), "}")
            self.create_edge(dot, self.getNodeId(), "rb_" + self.getNodeId())
        else:
            self.create_minimal_node(dot, self.getNodeId(), self.fname, 'chocolate1')
            for param in self.params:
                self.create_edge(dot, self.getNodeId(), param.to_dot(dot, False))
            self.create_edge(dot, self.getNodeId(), self.body.to_dot(dot, False))
        return self.getNodeId()


class CALL(EXPRESSION):
    def __init__(self, fname, arguments):
        super().__init__()
        self.fname=fname
        self.arguments=arguments

    def __str__(self): return self.fname+"(" \
        +','.join([ str(arg) for arg in self.arguments ]) +")"

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "CALL")
            self.create_leaf(dot, "id_" + self.getNodeId(), "id(" + self.fname + ")")
            self.create_edge(dot, self.getNodeId(), "id_" + self.getNodeId())
            self.create_leaf(dot, "lp_" + self.getNodeId(), "(")
            self.create_edge(dot, self.getNodeId(), "lp_" + self.getNodeId())
            for index, arg in enumerate(self.arguments):
                self.create_edge(dot, self.getNodeId(), arg.to_dot(dot, True))
                # Füge ein ","-Blatt zwischen den Deklarationen ein
                if index < len(self.arguments) - 1:
                    self.create_leaf(dot, "comma_" + self.getNodeId() + str(index), "comma")
                    self.create_edge(dot, self.getNodeId(), "comma_" + self.getNodeId() + str(index))
            self.create_leaf(dot, "rp_" + self.getNodeId(), ")")
            self.create_edge(dot, self.getNodeId(), "rp_" + self.getNodeId())
        else:
            self.create_minimal_node(dot, self.getNodeId(), self.fname, 'darkslategray')
            for arg in self.arguments:
                self.create_edge(dot, self.getNodeId(), arg.to_dot(dot, False))
        return self.getNodeId()


class VAR(EXPRESSION):
    def __init__(self,name):
        super().__init__()
        self.name=name

    def __str__(self): return self.name

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "VAR")
            self.create_leaf(dot, "var_" + self.getNodeId(), "var(" + self.name + ")")
            self.create_edge(dot, self.getNodeId(), "var_" + self.getNodeId())
        else:
            self.create_minimal_node(dot, self.getNodeId(), self.name, 'chartreuse2')
        return self.getNodeId()

class BINOP(EXPRESSION):
    def __init__(self,operator,arg1,arg2):
        super().__init__()
        self.operator=operator
        self.arg1=arg1
        self.arg2=arg2

    def __str__(self): return "("+str(self.arg1)+self.operator+str(self.arg2)+")"

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "BINOP")
            self.create_edge(dot, self.getNodeId(), self.arg1.to_dot(dot, True))
            self.create_leaf(dot, "op_" + self.getNodeId(), self.operator)
            self.create_edge(dot, self.getNodeId(), "op_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.arg2.to_dot(dot, True))
        else:
            self.create_minimal_node(dot, self.getNodeId(), self.operator, 'red')
            self.create_edge(dot, self.getNodeId(), self.arg1.to_dot(dot, False))
            self.create_edge(dot, self.getNodeId(), self.arg2.to_dot(dot, False))

        return self.getNodeId()

class CONST(EXPRESSION):
    def __init__(self,value):
        super().__init__()
        self.value=value

    def __str__(self): return str(self.value)

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "CONST")
            self.create_leaf(dot, "const_" + self.getNodeId(), "const(" + str(self.value) + ")")
            self.create_edge(dot, self.getNodeId(), "const_" + self.getNodeId())
        else:
            self.create_minimal_node(dot, self.getNodeId(), str(self.value), 'purple')
        return self.getNodeId()

class BOOL(EXPRESSION):
    def __init__(self,bool):
        super().__init__()
        self.bool=bool


    def __str__(self): return str(self.bool)

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "BOOL")
            self.create_leaf(dot, "bool_" + self.getNodeId(), "bool(" + str(self.bool) + ")")
            self.create_edge(dot, self.getNodeId(), "bool_" + self.getNodeId())
        else:
            self.create_minimal_node(dot, self.getNodeId(), str(self.bool), 'seagreen')

        return self.getNodeId()

class ASSIGN(EXPRESSION):
    def __init__(self, variable, expression):
        super().__init__()
        self.variable=variable
        self.expression=expression

    def __str__(self): return self.variable.name+"="+str(self.expression)

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "ASSIGN")
            self.create_edge(dot, self.getNodeId(), self.variable.to_dot(dot, True))
            self.create_leaf(dot, "assign_" + self.getNodeId(), "=")
            self.create_edge(dot, self.getNodeId(), "assign_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.expression.to_dot(dot, True))
        else:
            self.create_minimal_node(dot, self.getNodeId(), "=", 'turquoise')
            self.create_edge(dot, self.getNodeId(), self.variable.to_dot(dot, False))
            self.create_edge(dot, self.getNodeId(), self.expression.to_dot(dot, False))
        return self.getNodeId()

class SEQ(EXPRESSION):
    def __init__(self, exp1, exp2):
        super().__init__()
        self.exp1=exp1
        self.exp2=exp2

    def __str__(self): return str(self.exp1)+";"+str(self.exp2)

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "SEQ")
            self.create_edge(dot, self.getNodeId(), self.exp1.to_dot(dot, True))
            self.create_leaf(dot, "seq_" + self.getNodeId(), ";")
            self.create_edge(dot, self.getNodeId(), "seq_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.exp2.to_dot(dot, True))
        else:
            self.create_minimal_node(dot, self.getNodeId(), "SEQ", 'black')
            self.create_edge(dot, self.getNodeId(), self.exp1.to_dot(dot, False))
            self.create_edge(dot, self.getNodeId(), self.exp2.to_dot(dot, False))
        return self.getNodeId()

class IF(EXPRESSION):
    def __init__(self,condition,exp1,exp2):
        super().__init__()
        self.condition=condition
        self.exp1=exp1
        self.exp2=exp2

    def __str__(self): return "if "+str(self.condition)+" then { " \
            + str(self.exp1)+" } else { "+str(self.exp2)+" } "

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "IF")
            self.create_leaf(dot, "if_" + self.getNodeId(), "if")
            self.create_edge(dot, self.getNodeId(), "if_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.condition.to_dot(dot, True))
            self.create_leaf(dot, "then_" + self.getNodeId(), "then")
            self.create_edge(dot, self.getNodeId(), "then_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.exp1.to_dot(dot, True))
            self.create_leaf(dot, "else_" + self.getNodeId(), "else")
            self.create_edge(dot, self.getNodeId(), "else_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.exp2.to_dot(dot, True))
        else:
            self.create_minimal_node(dot, self.getNodeId(), "if", 'blue')
            self.create_edge(dot, self.getNodeId(), self.condition.to_dot(dot, False))
            self.create_minimal_node(dot, "then_" + self.getNodeId(), "then", 'blue')
            self.create_minimal_node(dot, "else_" + self.getNodeId(), "else", 'blue')
            self.create_edge(dot, self.getNodeId(),"then_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), "else_" + self.getNodeId())
            self.create_edge(dot, "then_" + self.getNodeId(), self.exp1.to_dot(dot, False))
            self.create_edge(dot, "else_" + self.getNodeId(), self.exp2.to_dot(dot, False))

        return self.getNodeId()

class WHILE(EXPRESSION):
    def __init__(self,condition,body):
        super().__init__()
        self.condition=condition
        self.body=body

    def __str__(self): return "while "+str(self.condition)+" do { "+str(self.body)+" }"

    def to_dot(self, dot, extensive):
        if extensive:
            self.create_node(dot, self.getNodeId(), "WHILE")
            self.create_leaf(dot, "while_" + self.getNodeId(), "while")
            self.create_edge(dot, self.getNodeId(), "while_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.condition.to_dot(dot, True))
            self.create_leaf(dot, "do_" + self.getNodeId(), "do")
            self.create_edge(dot, self.getNodeId(), "do_" + self.getNodeId())
            self.create_leaf(dot, "lb_" + self.getNodeId(), "{")
            self.create_edge(dot, self.getNodeId(), "lb_" + self.getNodeId())
            self.create_edge(dot, self.getNodeId(), self.body.to_dot(dot, True))
            self.create_leaf(dot, "rb_" + self.getNodeId(), "}")
            self.create_edge(dot, self.getNodeId(), "rb_" + self.getNodeId())
        else:
            self.create_minimal_node(dot, self.getNodeId(), "while", 'dodgerblue')
            self.create_edge(dot, self.getNodeId(), self.condition.to_dot(dot, False))
            self.create_minimal_node(dot, "do_" + self.getNodeId(), "do", 'dodgerblue')
            self.create_edge(dot, self.getNodeId(), "do_" + self.getNodeId())
            self.create_edge(dot, "do_" + self.getNodeId(), self.body.to_dot(dot, False))
        return self.getNodeId()

