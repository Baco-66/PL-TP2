import ply.yacc as yacc
import re
# Get the tokens from the lexer
from compilador_lex import tokens

# Production rules fro Program
def p_Program(p):
    "Program : Start Code" 
    outputFile.write("STOP")

# Production rules for declaration
def p_Declaration(p):
    "Declaration : type id ';' Declaration"
    p[0] = p[4] + 1
    p.parser.var.update({p[2] : len(p.parser.var)})
    #p.var[p[2]] = 

def p_Declaration_Empty(p):
    "Declaration : "
    p[0] = 0    

# Production rules for start
def p_Start(p):
    "Start : Declaration start"
    outputFile.write("PUSHN "+ str(p[1]) + "\n")
    outputFile.write("START\n")

# Production rules for code
def p_Code(p):
    "Code : Line Code"
    pass

def p_Code_empty(p):
    "Code : "
    pass

# Production rules for line
def p_Line_Print_Exp(p):
    "Line : print '(' Exp ')'"
    outputFile.write("\tWRITEI\n")

def p_Line_Read_Attr(p):
    "Line : read '(' id ')'"
    outputFile.write("\tREAD\n")
    outputFile.write("\tATOI\n")
    outputFile.write("\tSTOREG " + str(p.parser.var.get(p[3])) + "\n")
    pass

def p_Line_Store_Attr(p):
    "Line : id '=' Exp ';'"
    outputFile.write("\tSTOREG " + str(p.parser.var.get(p[1])) + "\n")
    pass

def p_Line_Cond(p):
    "Line : if '(' Cond ')' CondCode"
    pass

def p_Line_While(p):
    "Line : WhileStart WhileLoop '{' Code '}'"
    outputFile.write("\tJZ " + p[1] + "\n")
    outputFile.write(p[2] + ":\n")

def p_Line_Exp(p):
    "Line : Exp ';'"
    pass

# Production for WhileStart
def p_WhileStart(p):
    "WhileStart : while"
    p.parser.id += 1
    p[0] = "while" + str(p.parser.id)
    outputFile.write(p[0] + ":\n")

# Production for WhileLoop
def p_WhileLoop(p):
    "WhileLoop : '(' Cond ')'"
    p.parser.id += 1
    p[0] = "while_end" + str(p.parser.id)
    outputFile.write("\tJZ " + p[0] + "\n")

# Production for CondCode
def p_CondCode(p):
    "CondCode : IfStart Code '}'"
    outputFile.write(p[1] + ":\n")

def p_CondCode_Else(p):
    "CondCode : ElseStart Code '}'"
    outputFile.write(p[1] + ":\n")

# Production rules for Ifstart
def p_IfStart(p):
    "IfStart : '{'"
    p.parser.id += 1
    p[0] = "if" + str(p.parser.id)
    outputFile.write("\tJZ " + p[0] + "\n")

def p_ElseStart(p):
    "ElseStart : IfStart Code '}' else '{'"
    p.parser.id += 1
    p[0] = "else" + str(p.parser.id)
    outputFile.write("\tJUMP " + p[0] + "\n")
    outputFile.write(p[1] + ":\n")
    
# Production rules for Cond
# OR
def p_Cond_Or(p):
    "Cond : Cond or CondAnd"
    outputFile.write("\tADD\n")

def p_Cond_Empty(p):
    "Cond : CondAnd"
    pass

# AND
def p_CondAnd(p):
    "CondAnd : CondAnd and CondNot"
    outputFile.write("\tMUL\n")

def p_CondAnd_empty(p):
    "CondAnd : CondNot"
    pass

# Not Condition
def p_CondNot(p):
    "CondNot : '!' Cond '!'"
    outputFile.write("\tNOT\n")

def p_CondNot_Par(p):
    "CondNot : '(' Cond ')'"
    pass

def p_CondNot_Empty(p):
    "CondNot : Rel"
    pass

# Production rules for Rel
def p_Rel_Sup(p):
    "Rel : Exp '>' Exp"
    outputFile.write("\tSUP\n")

def p_Cond_Supeq(p):
    "Rel : Exp '>' '=' Exp"
    outputFile.write("\tSUPEQ\n")

def p_Cond_Inf(p):
    "Rel : Exp '<' Exp"
    outputFile.write("\tINF\n")

def p_Cond_Infeq(p):
    "Rel : Exp '=' '<' Exp"
    outputFile.write("\tINFEQ\n")

def p_Cond_Equal(p):
    "Rel : Exp '=' '=' Exp"
    outputFile.write("\tEQUAL\n")

def p_Cond_Not_Equal(p):
    "Rel : Exp '!' '=' Exp"
    outputFile.write("\tEQUAL\n")
    outputFile.write("\tNOT\n")

# Production rules for exp
def p_Exp_SUM(p):
    "Exp : Exp '+' Termo"
    outputFile.write("\tADD\n")
    
def p_Exp_SUB(p):
    "Exp : Exp '-' Termo"
    outputFile.write("\tSUB\n")

def p_Exp(p):
    "Exp : Termo"
    pass

# Production rules for termo
def p_Termo_MULT(p):
    "Termo : Termo '*' Factor"
    outputFile.write("\tMUL\n")

def p_Termo_DIV(p):
    "Termo : Termo '/' Factor"
    outputFile.write("\tDIV\n")

def p_Termo(p):
    "Termo : Factor"
    pass

# Production rules for fator
def p_Factor(p):
    "Factor : '(' Exp ')'"
    pass

def p_Factor_Int(p):
    "Factor : Atomic"
    pass

def p_Factor_Signal(p):
    "Factor : Signal Atomic"
    outputFile.write("\tMUL\n")

# Production rules for Atomic
def p_Atomic_Int(p):
    "Atomic : int"
    outputFile.write("\tPUSHI " + str(p[1])+ "\n")

def p_Atomic_Id(p):
    "Atomic : id"
    outputFile.write("\tPUSHG " + str(p.parser.var.get(p[1], 0)) + "\n")

#def p_Factor_Float(p):
#    "Factor : Signal float"
#    outputFile.write("pushi ", p[2])
#    outputFile.write("pushi ", p[1], "\n")
#    outputFile.write("mul\n")
#    p[0] = p[1] * p[2]

# Production rules for signal
def p_Signal_End(p):
    "Signal : '-'"
    outputFile.write("\tPUSHI -1\n")

def p_Signal(p):
    "Signal : Signal '-'"
    outputFile.write("\tPUSHI -1\n")
    outputFile.write("\tMUL\n")

# Error rule for syntax error
def p_error(p):
    print("Erro sintático", p)
    parser.success = False

# Build parser
parser = yacc.yacc()

import sys

inputFile = open("/home/baco/Documents/PL2021/Compilador/src/input_test.txt","r")
outputFile = open("/home/baco/Documents/PL2021/Compilador/src/output_test.vm","w")

i = len(sys.argv)

while i > 0:
    i -= 1
    if path := sys.argv[i]:
        if re.search(r'\.vm$',path):
            outputFile = open(path,"w")
        elif re.search(r'\.txt$',path):
            inputFile = open(path,"r")
    

# parser state
parser.erros = []
parser.var = {}
parser.id = 0

# Read input and parse it by line
#for linha in inputFile:
#    parser.success = True
#    parser.parse(linha)


parser.parse(inputFile.read())

print("Ficheiro compilado com sucesso")



inputFile.close
outputFile.close