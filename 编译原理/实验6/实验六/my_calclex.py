# ------------------------------------------------------------
# my_calclex.py
#
# tokenizer for a simple expression evaluator for
# SYMBOL and COUNT
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'SYMBOL',
    'COUNT'
)

# Regular expression rules for simple tokens
t_SYMBOL = (
    r"C[laroudsemf]?|Os?|N[eaibdpos]?|S[icernbmg]?|P[drmtboau]?|"
    r"H[eofgas]?|A[lrsgutcm]|B[eraik]?|Dy|E[urs]|F[erm]?|G[aed]|"
    r"I[nr]?|Kr?|L[iaur]|M[gnodt]|R[buhenaf]|T[icebmalh]|"  
    r"U|V|W|Xe|Yb?|Z[nr]")


# A regular expression rule with some action code
def t_COUNT(t):
    r"""\d+"""
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

## Build the lexer
lexer = lex.lex()
