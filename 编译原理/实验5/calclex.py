# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
# List of reversed names.   This is always required
reserved  = {
    'int'  : 'INT',
    'while': 'WHILE',
    'if'   : 'IF',
    'cout' : 'COUT',
    'endl' : 'ENDL'
}

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',

    'ID',
    'EQUAL',
    'STATEMENTEND',
    'OUTPUT',
    'LESS',
    'LBRACE',
    'RBRACE',
    'STRING'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


t_EQUAL = r'='
t_STATEMENTEND = r';'
t_OUTPUT = r'\<<'
t_LESS = r'\<'
t_LBRACE = r'{'
t_RBRACE = r'}'



# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'\"(.)+?\"'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# ADDITIONAL CODE
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID') # Check for reserved words
    return t

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
int asd = 0;
int bc = 10;
while ( asd < bc)
{
	if(bc - asd < 2)
		cout<<"they are close."<<endl;
	asd = asd + 1;
}


'''
# Give the lexer some input
lexer.input(data)
# Tokenize
while True:
	tok = lexer.token()
	if not tok: break # No more input
	print tok