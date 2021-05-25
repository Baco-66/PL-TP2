# Lexer da minha calculadora

import re
import ply.lex as lex

# Tokens
reserved = {
    'print' : 'print',
    'start' : 'start',
    'read' : 'read',
    'if' : 'if',
    'else' : 'else',
    'and' : 'and',
    'or' : 'or',
    'while' : 'while',
}
tokens = ['int','id','type'] + list(reserved.values())
literals = ['+','-','*','/','(',')',';','=','<','>','{','}','!']

t_ignore = " \t\n"

def t_type(t):
    r'int'
    return t

def t_print(t):
    r'print'
    return t

def t_start(t):
    r'start|START'
    return t

def t_read(t):
    r'read'
    return t

def t_if(t):
    r'if'
    return t

def t_else(t):
    r'else'
    return t

def t_and(t):
    r'and'
    return t

def t_or(t):
    r'or'
    return t

def t_while(t):
    r'while'
    return t

def t_id(t):
    r'[a-zA-Z]+'
    t.type = reserved.get(t.value,'id')
    return t

def t_int(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print('Carater ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
