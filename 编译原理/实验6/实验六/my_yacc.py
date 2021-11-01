#! /usr/bin/env python
# coding=utf-8
from my_calclex import tokens
import ply.yacc as yacc


def p_species_list(p):
    """species_list : species """
    p[0] = p[1]


def p_species_list_species(p):
    """species_list : species_list species"""
    p[0] = p[1] + p[2]


def p_species_SYMBOL(p):
    """species : SYMBOL"""
    p[0] = 1


def p_species_SYMBOL_COUNT(p):
    """species : SYMBOL COUNT"""
    p[0] = p[2]


# Error rule for syntax errors
def p_error():
    print()
    "Syntax error in input!"


# Build the parser
parser = yacc.yacc()


# 分子式的数据结构
class Atom(object):
    def __init__(self, symbol, count):
        self.symbol = symbol
        self.count = count

    def __repr__(self):
        return "Atom(%r, %r)" % (self.symbol, self.count)

def atom_count(symbol):
    result = parser.parse(symbol)
    return result

test_list = ["H2SO4", "He", "CH3COOH", "NaCl", "C60H60"]

for i in test_list:
    print(Atom(i, atom_count(i)))

