#! /usr/bin/env python
#coding=utf-8
import ply.lex as lex
import ply.yacc as yacc
import csv
import re
from math import *
from node import node

literals = ['=', '+', '-', '*', '^', '>', '<']

#TOKENS
tokens = ('SELECT',
          'FROM',
          'WHERE',
          'ORDER',
          'BY',
          'NAME',
          'AND',
          'OR',
          'COMMA',
          'LP',
          'RP',
          'AVG',
          'BETWEEN',
          'IN',
          'SUM',
          'MAX',
          'MIN',
          'COUNT',
          'NUMBER',
          'AS',
          'DOT')


#DEFINE OF TOKENS
def t_SELECT(t):
    r"""(?i)SELECT"""
    return t

def t_FROM(t):
    r"""(?i)FROM"""
    return t

def t_WHERE(t):
    r"""(?i)WHERE"""
    return t

def t_ORDER(t):
    r"""(?i)ORDER"""
    return t

def t_BY(t):
    r"""(?i)by"""
    return t


def t_AND(t):
    r"""(?i)AND"""
    return t

def t_OR(t):
    r"""(?i)OR"""
    return t

def t_COMMA(t):
    r""","""
    return t

def t_LP(t):
    r"""\("""
    return t

def t_RP(t):
    r"""\)"""
    return t

def t_AVG(t):
    r"""(?i)AVG"""
    return t

def t_BETWEEN(t):
    r"""(?i)BETWEEN"""
    return t

def t_SUM(t):
    r"""(?i)SUM"""
    return t

def t_MAX(t):
    r"""(?i)MAX"""
    return t

def t_MIN(t):
    r"""(?i)MIN"""
    return t

def t_COUNT(t):
    r"""(?i)count"""
    return t

def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t

def t_AS(t):
    r"""(?i)AS"""
    return t

def t_DOT(t):
    r"""(?i)DOT"""
    return t


def t_NAME(t):
    r"""(?i)[A-Za-z]+|[a-zA-Z_][a-zA-Z0-9_]*|[A-Z]*\.[A-Z]$"""
    return t

# IGNORED
t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# LEX ANALYSIS   
lex.lex()

#PARSING
def p_query(t):
    """query :  select"""
    t[0] = t[1]

def p_LP_query_RP(t):
    """query : LP query RP"""
    t[0] = t[2]
        
def p_select_from(t):
    """select : SELECT list FROM table """
    t[0] = node('QUERY')
    t[0].add(node('[SELECT]'))
    t[0].add(t[2])
    t[0].add(node('[FROM]'))
    t[0].add(t[4])

def p_select_from_order_by(t):
    """select : SELECT list FROM table ORDER BY list """
    t[0] = node('QUERY')
    t[0].add(node('[SELECT]'))
    t[0].add(t[2])
    t[0].add(node('[FROM]'))
    t[0].add(t[4])
    t[0].add(node('[ORDER BY]'))
    t[0].add(t[7])

def p_select_from_where(t):
    """select : SELECT list FROM table WHERE lst """
    t[0] = node('QUERY')
    t[0].add(node('[SELECT]'))
    t[0].add(t[2])
    t[0].add(node('[FROM]'))
    t[0].add(t[4])
    t[0].add(node('[WHERE]'))
    t[0].add(t[6])

def p_select_from_where_order_by(t):
    """select : SELECT list FROM table WHERE lst ORDER BY list"""
    t[0] = node('QUERY')
    t[0].add(node('[SELECT]'))
    t[0].add(t[2])
    t[0].add(node('[FROM]'))
    t[0].add(t[4])
    t[0].add(node('[WHERE]'))
    t[0].add(t[6])
    t[0].add(node('[ORDER BY]'))
    t[0].add(t[9])

def p_table_name(t):
    """table : NAME"""
    t[0] = node(t[1])

def p_table_query(t):
    """table : LP query RP"""
    t[0] = node('[TABLE]')
    t[0].add(node[t[2]])

def p_name_as_name(t):
    """tabel : NAME AS NAME"""
    t[0] = node('TABLE')
    t[0].add(node(t[1]))
    t[0].add(node('[AS]'))
    t[0].add(node(t[3]))


def p_table_as_name(t):
    """table : table AS NAME"""
    t[0] = node('TABLE')
    t[0].add(node('AS'))
    t[0].add(node(t[3]))

def p_table_comma_table(t):
    """table : table COMMA table"""
    t[0] = node(['TABLE'])
    t[0].add(node(t[1]))
    t[0].add(node(t[3]))
"""
def p_lst_condition(t):
    lst : lst
    t[0] = node['LST']
    t[0].add(node(t[1]))"""

def p_lst_condition_and(t):
    """lst : lst AND lst"""
    t[0] = node(t[1])
    t[0].add(node('AND'))
    t[0].add(node(t[3]))

def p_lst_condition_or(t):
    """lst : lst OR lst"""
    t[0] = node(t[1])
    t[0].add(node('OR'))
    t[0].add(node(t[3]))

def p_lst_between(t):
    """lst : NAME BETWEEN NUMBER AND NUMBER"""
    t[0] = node(t[1])
    t[0].add(node('BETWEEN'))
    t[0].add(node(t[3]))
    t[0].add(node('AND'))
    t[0].add(node(t[5]))

def p_lst_in(t):
    """lst : NAME IN LP query RP"""
    t[0] = node(t[1])
    t[0].add(node('[IN]'))
    t[0].add(node(t[4]))

def p_lst_query(t):
    """lst : NAME '=' query"""
    t[0] = node(t[1])
    t[0].add(node('[=]'))
    t[0].add(t[3])

def p_agg_xiaoyu_name(t):
    """lst : NAME '<' agg"""
    t[0] = node(t[1])
    t[0].add(node('[<]'))
    t[0].add(t[3])

def p_agg_dayu_name(t):
    """lst : NAME '>' agg"""
    t[0] = node(t[1])
    t[0].add(node('[>]'))
    t[0].add(t[3])

def p_agg_dengyu_name(t):
    """lst : NAME '=' agg"""
    t[0] = node(t[1])
    t[0].add(node('[=]'))
    t[0].add(t[3])

def p_number_xiaoyu_name(t):
    """lst : NAME '<' NUMBER"""
    t[0] = node(t[1])
    t[0].add(node('[<]'))
    t[0].add(node(t[3]))

def p_NUMBER_dayu_name(t):
    """lst : NAME '>' NUMBER"""
    t[0] = node(t[1])
    t[0].add(node('[>]'))
    t[0].add(node(t[3]))

def p_NUMBER_dengyu_name(t):
    """lst : NAME '=' NUMBER"""
    t[0] = node(t[1])
    t[0].add(node('[=]'))
    t[0].add(node(t[3]))

def p_agg_dayu_number(t):
    """lst : agg '>' NUMBER"""
    t[0] = t[1]
    t[0].add(node('[>]'))
    t[0].add(node(t[3]))

def p_agg_xiaoyu_number(t):
    """lst : agg '<' NUMBER"""
    t[0] = t[1]
    t[0].add(node('[<]'))
    t[0].add(node(t[3]))

def p_agg_dengyu_number(t):
    """lst : agg '=' NUMBER"""
    t[0] = t[1]
    t[0].add(node('[=]'))
    t[0].add(node(t[3]))

def p_agg_sum(t):
    """agg : SUM LP NAME RP"""
    t[0] = node('[SUM]')
    t[0].add(node(t[3]))

def p_agg_avg(t):
    """agg : AVG LP NAME RP"""
    t[0] = node('[AVG]')
    t[0].add(node(t[3]))

def p_agg_COUNT(t):
    """agg : COUNT LP NAME RP"""
    t[0] = node('[COUNT]')
    t[0].add(node(t[3]))

def p_agg_MIN(t):
    """agg : MIN LP NAME RP"""
    t[0] = node('[MIN]')
    t[0].add(node(t[3]))

def p_agg_MAX(t):
    """agg : MAX LP NAME RP"""
    t[0] = node(['MAX'])
    t[0].add(node(t[3]))

def p_agg_count_all(t):
    """agg : COUNT LP '*' RP"""
    t[0] = node('[COUNT]')
    t[0].add(node('*'))

def p_list_name(t):
    """ list : NAME"""
    t[0] = node('[FIELD]')
    t[0].add(node(t[1]))

def p_list_all(t):
    """ list : '*'"""
    t[0] = node('[FIELD]')
    t[0].add(node('[all]'))

def p_list_list(t):
    """list : list COMMA list"""
    t[0] = node('[FIELD]')
    t[0].add(node(t[1]))
    t[0] = node('[FIELD]')
    t[0].add(node(t[3]))

def p_list_and_name(t):
    """list : list AND NAME"""
    t[0] = node('[FIELD]')
    t[0].add(node(t[1]))
    t[0] = node('[AND]')
    t[0].add(node(t[3]))

def p_list_or_name(t):
    """list : list OR NAME"""
    t[0] = node('[FIELD]')
    t[0].add(node(t[1]))
    t[0] = node('[OR]')
    t[0].add(node(t[3]))

def p_list_agg(t):
    """list : agg"""
    t[0] = t[1]


yacc.yacc()


#query = 'select id from scroe where yuwen = select max(yuwen) from scroe'
#query = 'select * from scroe order by grade'
query = 'select avg(math) from score'

parse = yacc.parse(query)
parse.print_node(0)

