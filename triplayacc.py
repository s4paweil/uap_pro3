
# ------------------------------------------------------------
# triplayacc.py
#
# Yacc grammar of the TRIPLA language
''' Here the grammar
	E -> let D in E
		| ID
		| ID ( A )
		| E AOP E
		| ( E )
		| CONST
		| ID = E
		| E ; E
		| if B then E else E
		| while B do { E }
	A -> E | A , E
	D -> ID ( V ) { E }
		| D ID ( V ) { E }
	V -> ID | V , V
	B -> (B)
		| true | false
		| B LOP B
		| E RELOP E

	ID : Bezeichner = [A-Za-z_] [A-Za-z0-9_] *
	CONST: Positive, ganze Zahl = 0 | [1-9] [0-9] *
	AOP: Operatoren (+, - , * , /)
	RELOP: Vergleichsoperatoren (==, !=, <, >, <=, >=)
	LOP: Logische Operatoren (||, &&, ==, !=)

'''

# Note: For LALR(1) left recursion is preferred
# ------------------------------------------------------------

import ply.yacc as yacc
#import syntax as ast
import compiler as ast

# Get the token map from the lexer.  This is required.
from triplalex import tokens


# Precedence
precedence = (
    ('nonassoc', 'RP', 'IN'),
    ('left', 'SEMICOLON', 'COMMA', 'ID'),
    ('nonassoc', 'ASSIGN', 'ELSE', 'WHILE', 'IF', 'DO', 'LET'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LT', 'GT', 'EQ', 'NEQ', 'LTE', 'GTE'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)


# Parsing rules
def p_E_let(p):
    'E : LET D IN E'
    p[0] = ast.LET(p[2], p[4])

def p_E_id(p):
    'E : ID'
    p[0] = ast.VAR(p[1])

def p_E_id_arg(p):
    'E : ID LP A RP'
    p[0] = ast.CALL(p[1], p[3])

def p_E_binop(p):
    '''
    E : E ADD E
      | E SUB E
      | E MUL E
      | E DIV E
    '''
    p[0] = ast.BINOP(p[2], p[1], p[3])

def p_E_parentheses(p):
    'E : LP E RP'
    p[0] = p[2]

def p_E_const(p):
    'E : CONST'
    p[0] = ast.CONST(p[1])

def p_E_assign(p):
    'E : ID ASSIGN E'
    p[0] = ast.ASSIGN(ast.VAR(p[1]), p[3])

def p_E_semicolon(p):
    'E : E SEMICOLON E'
    p[0] = ast.SEQ(p[1], p[3])

def p_E_if_ele(p):
    'E : IF B THEN E ELSE E'
    p[0] = ast.IF(p[2], p[4], p[6])

def p_E_while(p):
    'E : WHILE B DO LB E RB'
    p[0] = ast.WHILE(p[2],p[5])

def p_A_single(p):
    'A : E'
    p[0] = [p[1]]

def p_A_multiple(p):
    'A : A COMMA E'
    p[0] = p[1] + [p[3]]

def p_D_single(p):
    'D : ID LP V RP LB E RB'
    p[0] = [ast.DECL(p[1], p[3], p[6])]

def p_D_multiple(p):
    'D : D ID LP V RP LB E RB'
    p[0] = p[1] + [ast.DECL(p[2], p[4], p[7])]

def p_V_single(p):
    'V : ID'
    p[0] = [ast.VAR(p[1])]

def p_V_multiple(p):
    'V : V COMMA V'
    p[0] = p[1] + p[3]

def p_B_parentheses(p):
    'B : LP B RP'
    p[0] = p[2]

def p_B_true(p):
    'B : TRUE'
    p[0] = ast.BOOL(True)

def p_B_false(p):
    'B : FALSE'
    p[0] = ast.BOOL(False)

def p_B_lop(p):
    '''
    B : B OR B
      | B AND B
      | B NEQ B
      | B EQ B
    '''
    p[0] = ast.BINOP(p[2], p[1], p[3])

def p_B_relop(p):
    '''
    B : E EQ E
      | E NEQ E
      | E LT E
      | E GT E
      | E LTE E
      | E GTE E
    '''
    p[0] = ast.BINOP(p[2], p[1], p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()  # debug=True