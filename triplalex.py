# ------------------------------------------------------------
# triplalex.py
#
# tokenizer for the TRIPLA parser
# ------------------------------------------------------------

import ply.lex as lex

reserved = {
    'let' : 'LET',
    'in' : 'IN',
    'while' : 'WHILE',
    'do' : 'DO',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'true' : 'TRUE',
    'false' : 'FALSE',
}

# List of token names. This is always required
tokens = [
    'ID',
    'CONST',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'GT',
    'LT',
    'GTE',
    'LTE',
    'AND',
    'OR',
    'EQ',
    'NEQ',
    'LB',
    'RB',
    'LP',
    'RP',
    'COMMA',
    'ASSIGN',
    'SEMICOLON',
    'COMMENT',
]+list(reserved.values())

# Regular expression rules for simple tokens
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_GT = r'>'
t_LT = r'<'
t_GTE = r'>='
t_LTE = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_EQ = r'=='
t_NEQ = r'!='
t_LB = r'\{'
t_RB = r'\}'
t_LP = r'\('
t_RP = r'\)'
t_COMMA = r','
t_ASSIGN = r'='
t_SEMICOLON = r';'

# Regular explression rules for complex tokens
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_CONST(t):
    r'0|[1-9][0-9]*'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_COMMENT(t):
    r'/\*[^*]*\*+(?:[^*/][^*]*\*+)*/|//.*'
    # Comments of form '//...' and '/* ... */' are filtered
    pass
    # No return value. Token discarded


# Build the lexer
lexer = lex.lex()


