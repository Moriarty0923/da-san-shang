#! /usr/bin/env python
#coding=utf-8
import re
from html2pdf import html2pdf

# parse by regex

def re_find(p,text):
    m=p.findall(text)
    if len(m)==1:
        return m[0]
    else:
        return ''

def re_findall(p,text):
    return p.findall(text)

def clear_text(text):
    lines=[]
    for line in text.split('\n'):
        line=line.strip()
        if len(line)>0:
            lines.append(line)
    return ' '.join(lines)

# 1. read tex file
content=open('example.tex','rb').read()

# 2. extract document part
p_doc=re.compile(r'\\begin{document}(.+?)\\end{document}',re.S)
document=re_find(p_doc,content)


# 3. extract head
p_title=re.compile(r'\\title{(.+?)}',re.S)
title=re_find(p_title,document)

# 4. extract abstract
p_abs=re.compile(r'\\begin{abstract}(.+?)\\end{abstract}',re.S)
abstract=re_find(p_abs,document)
abstract=clear_text(abstract)

# 5. sections
p_sec=re.compile(r'\\section{(.+?)}(.+?)\\section{(.+?)}(.+?)\\subsection',re.S) #  for Section 1 and 2
section_title,section_content,section2_title,section2_content=re_find(p_sec,document)
section_content=clear_text(section_content)
section2_content=clear_text(section2_content)


'''
还需完成标记的解析
a.	subsection
b.	itemize/item
c.	tabular
d.	emph
e.	textbf
'''
#a. subsections
p_sub=re.compile(r'\\subsection{(.+?)}(.+?)\\subsubsection',re.S)
subsection_title,subsection_content=re_find(p_sub,document)
subsection_content=clear_text(subsection_content)

#b. itemize/item
p_itemize = re.compile(r'\\begin{itemize}.+?\\end{itemize}',re.S)
itemize = re_findall(p_itemize, document)
p_item = re.compile(r'{\\textbackslash(.*?)} - ((.|\r|\t|\n)*?)(\\item|\\end)')
item_title=[]
item_context=[]
for i in itemize:
    for j in re_findall(p_item,i):
        item_title.append(clear_text(j[0]))
        item_context.append(clear_text(j[1]))

# c. tabular
p_tabular = re.compile(r'\\begin{tabular}.+?\\end{tabular}',re.S)
tabular = re_findall(p_tabular, document)
p_t = re.compile(r'{\\textbackslash(.*?)\\(.*?)(-\d|\d)')
tab_title=[]
tab_context=[]
for j in re_findall(p_t,tabular[0]):
    tab_title.append(clear_text(j[0]))
    tab_context.append(clear_text(j[2]))

# d. emph
p_emph = re.compile(r'{\\emph{(.*?)}',re.S)
emph_list = re_findall(p_emph, document)

#e.	textbf

'''
以下部分为将提取的tex源码内容转化为字符串形式的html文件
'''
# 6. generate html text

html_text=''
# title
html_text+='<h1>%s</h1>\n\n' %title
# abstract
html_text+='<p>%s</p>\n\n' %abstract
# section -- 1
html_text+='<h2>%s</h2>\n\n' %section_title
html_text+='<p>%s</p>\n\n' %section_content
# section -- 2
html_text+='<h2>%s</h2>\n\n' %section2_title
html_text+='<p>%s</p>\n\n' %section2_content

'''
generate new html text
html_a  subsection
html_b	itemize/item
html_c	tabular
html_d	emph
html_e	textbf
'''
# html_a  subsection
html_text+='<h3>%s</h3>\n\n' %subsection_title
html_text+='<p>%s</p>\n\n' %subsection_content


#html_b  itemize.item
html_text+='<h2>%s</h2>' %"Itemize"
html_text+="<ul>"
for i in range(len(item_title)):
    html_text = html_text + "<li>"+item_title[i]+"    -    "+item_context[i]+"</li>"
html_text+="<ul>"


#html_c  tabular
html_text+='<h2>%s</h2>' %"Table"
html_text+='''
<table border="1" align="center" width="50%">
<thead><tr><th width="70%">command</th><th width="30%">level</th></tr></thead>
<tbody>
'''
for i in range(len(tab_title)):
    html_text+="<tr><td align=\"left\">/%s{%s}</td><td align=\"center\">%s</td></tr>"%(tab_title[i],tab_title[i],tab_context[i])
html_text+="""
</tbody>
</table>
"""

#html_d  emph
html_text+='<h2><B>%s</B></h2>' %"Emph"
for i in emph_list:
    html_text+='<p><B>%s</B></p>' %i

html2pdf(html_text,'2.pdf')