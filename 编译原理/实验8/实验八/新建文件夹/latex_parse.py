#! /usr/bin/env python
#coding=utf-8
import re
import ply.lex as lex
import ply.yacc as yacc
from html2pdf import html2pdf
from node import node

def clear_text(text):
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 0:
            lines.append(line)
    return ' '.join(lines)


# TOKENS
tokens = ('TITLE', 'ABS', 'AUTHOR', 'DOC', 'SECTION', 'SUBSECTION', 'TEXT', 'BEGIN', 'END', 'LB', 'RB', 'ITEMIZE'
          , 'ITEM')

#DEFINE OF TOKENS
def t_TITLE(t):
    r'\\title'
    return t

def t_AUTHOR(t):
    r'\\author'
    return t

def t_DOC(t):
    r'document'
    return t

def t_ABS(t):
    r"""abstract"""
    return t


def t_SECTION(t):
    r"""\\section"""
    return t

def t_SUBSECTION(t):
    r"""\\subsection"""
    return t

def t_ITEMIZE(t):
    r"""itemize"""
    return t

def t_ITEM(t):
    r"""\\item"""
    return t

def t_BEGIN(t):
    r"""\\begin"""
    return t

def t_END(t):
    r"""\\end"""
    return t

def t_LB(t):
    r"""\{"""
    return t

def t_RB(t):
    r"""\}"""
    return t

def t_TEXT(t):
    r"""[a-zA-Z\s\.\,\:\']+"""
    return t

# IGNORED
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# LEX
lex.lex()

# PARSE
def p_doc(t):
    r"""doc : BEGIN LB DOC RB content END LB DOC RB"""
    if len(t) == 10:
        t[0] = node('[DOC]')
        t[0].add(t[5])

def p_content(t):
    r"""content : title author abs sections subsections itemize TEXT"""
    t[0] = node('[CONTENT]')
    t[0].add(t[1])
    t[0].add(t[2])
    t[0].add(t[3])
    t[0].add(t[4])
    t[0].add(t[5])
    t[0].add(t[6])
    t[0].add(node(t[7]))


def p_title(t):
    r"""title : TITLE LB TEXT RB"""
    if len(t) == 5:
        t[0] = node('[TITLE]')
        t[0].add(node(t[3]))

def p_author(t):
    r"""author : AUTHOR LB TEXT RB"""
    if len(t) == 5:
        t[0] = node('[AUTHOR]')
        t[0].add(node(t[3]))

def p_abs(t):
    r"""abs : BEGIN LB ABS RB TEXT END LB ABS RB"""
    if len(t) == 10:
        t[0] = node('[ABSTRACT]')
        t[0].add(node(t[5]))

def p_sections(t):
    """sections : sections section
                | section"""
    if len(t) == 3:
        t[0] = node('[SECTIONS]')
        t[0].add(t[1])
        t[0].add(t[2])
    if len(t) == 2:
        t[0] = node('[SECTIONS]')
        t[0].add(t[1])

def p_section(t):
    r"""section : SECTION LB TEXT RB TEXT"""
    if len(t) == 6:
        t[0] = node('[SECTION](%s)' % t[3])
        t[0].add(node(t[5]))

def p_subsections(t):
    r"""subsections : subsections subsection
                    | subsection"""
    if len(t) == 3:
        t[0] = node('[SUBSECTIONS]')
        t[0].add(t[1])
        t[0].add(t[2])
    if len(t) == 2:
        t[0] = node('[SUBSECTIONS]')
        t[0].add(t[1])

def p_subsection(t):
    r"""subsection : SUBSECTION LB TEXT RB TEXT"""
    t[0] = node('[SUBSECTION](%s)' % t[3])
    t[0].add(node(t[5]))

def p_itemize(t):
    r"""itemize : BEGIN LB ITEMIZE RB items END LB ITEMIZE RB"""
    t[0] = node('[ITEMIZE]')
    t[0].add(t[5])

def p_items(t):
    r"""items : items item
              | item"""
    if len(t) == 3:
        t[0] = t[1]
        t[0].add(t[2])
    if len(t) == 2:
        t[0] = t[1]

def p_item(t):
    """item : ITEM TEXT"""
    t[0] = node('[ITEM]')
    t[0].add(node(t[2]))


def p_error(t):
    print("Syntax error at '%s'" % t.value)

data = clear_text(open('example2.tex', 'rb').read())
#print(data)
lexer = lex.lex()
lexer.input(data)
# while 1:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
yacc.yacc()
parse = yacc.parse(data)
parse.print_node(0)

html = ""
root = parse.getchildren()[0].getchildren()

def get(str):
    pattern = re.compile(r".*\((.+)\).*")
    res = re.findall(pattern, str)[0]
    return res

for i in root:
    cur_tag = i.getdata()
    #print(cur_tag)
    if cur_tag == '[TITLE]':
        for j in i.getchildren():
            html += '<h1 align=\'center\'>%s</h1>\n' % j.getdata()
    elif cur_tag == '[AUTHOR]':
        for j in i.getchildren():
            html += '<h3 align=\'center\'>%s</h3>\n\n' % j.getdata()
    elif cur_tag == '[ABSTRACT]':
        html += '<h3 align=\'center\'>Abstract</h3>'
        for j in i.getchildren():
            html += '<p>%s</p>\n' % j.getdata()
    elif cur_tag == '[SECTIONS]':
        #print(i.getdata())
        for j in i.getchildren():
            if j.getdata() == '[SECTIONS]':
                for m in j.getchildren():
                    html += '<h3>%s</h3>' % get(m.getdata())
                    for n in m.getchildren():
                        html += '<p>%s</p>\n' % n.getdata()
            else:
                html += '<h3>%s</h3>' % get(j.getdata())
                for n in j.getchildren():
                    html += '<p>%s</p>\n' % n.getdata()
    elif cur_tag == '[SUBSECTIONS]':
        #print(i.getdata())
        for j in i.getchildren():
            if j.getdata() == '[SUBSECTIONS]':
                for m in j.getchildren():
                    html += '<h4>%s</h4>' % get(m.getdata())
                    for n in m.getchildren():
                        html += '<p>%s</p>' % n.getdata()
            else:
                html += '<h4>%s</h4>\n' % get(j.getdata())
                for n in j.getchildren():
                    html += '<p>%s</p>\n' % n.getdata()
    elif cur_tag =='[ITEMIZE]':
        html += "<ul>\n"
        for j in i.getchildren():
            for m in j.getchildren():
                if m.getdata() == '[ITEM]':
                    html = html + "<li>" + m.getchildren()[0].getdata() + "</li>\n"
                else:
                    html = html + "<li>" + m.getdata() + "</li>\n"
        html += "<ul>\n\n"
    else:
        html += '<p>%s</p>\n' % i.getdata()



#print(html)
html2pdf(html, '2.pdf')


