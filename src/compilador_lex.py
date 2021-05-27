# Lexer do compilador

import re
import ply.lex as lex

# Tokens
reserved = {
    'print' : 'print',
    'printS' : 'printS',
    'start' : 'start',
    'read' : 'read',
    'if' : 'if',
    'else' : 'else',
    'and' : 'and',
    'or' : 'or',
    'while' : 'while',
    'repeat' : 'repeat',
    'int' : 'int',
}
tokens = ['integer','id', 'string'] + list(reserved.values())
literals = [
    '+','-','*','/','%',
    '(',')','[',']','{','}',
    ',',';','=','<','>','!']

def t_comment(t):
    r'(\#[^\n]*)|(\#[^\#]*)'
    pass

def t_id(t):
    r'[a-zA-Z]+'
    t.type = reserved.get(t.value,'id')
    return t

def t_integer(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_string(t):
    r'\"[^\"]*\"'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

t_ignore = " \t"

def t_error(t):
    print('LEX ERROR:\n\t' + str(t))
    print("\tCarater ilegal \'" + t.value[0] + '\'')
    print("\tLinha " + str(t.lexer.lineno))
    t.lexer.skip(1)

lexer = lex.lex()