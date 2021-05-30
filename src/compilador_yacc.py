import ply.yacc as yacc
import re
# Get the tokens from the lexer
from compilador_lex import tokens
from difflib import SequenceMatcher

# Production rules for Program
def p_Program(p):
    "Program : Start Code" 
    outputFile.write("STOP")

# Production rules for start
def p_Start(p):
    "Start : Declaration start"
    p.parser.var.update({"0" : p.parser.startup})
    p.parser.startup += 1
    outputFile.write("PUSHN " + str(p.parser.startup - p[1]) + "\n")
    outputFile.write("START\n")

# Production rules for declaration
def p_Declaration(p):
    "Declaration : int Attr Declaration"
    p[0] = p[2] + p[3]

def p_Declaration_Array(p):
    "Declaration : int id '[' integer ']' ';' Declaration"
    if id := p.parser.var.get(p[2]):
        print("Semantic error:")
        print("\tVariable \'" + p[2] + "\' already defined")
    else:
        p.parser.var.update({p[2] : (p.parser.startup, p[4])})
        p.parser.startup += p[4]
    p[0] = p[7]


def p_Declaration_Empty(p):
    "Declaration : "  
    p[0] = 0  

# Production rules for Attr
def p_Attr(p):
    "Attr : id ',' Attr "
    if type(p.parser.var.get(p[1])):
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' already defined")
    else:
        p.parser.var.update({p[1] : p.parser.startup})
        p.parser.startup += 1
    p[0] = p[3]

def p_Attr_value(p):
    "Attr : id '=' Atomic ',' Attr"
    if type(p.parser.var.get(p[1])):
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' already defined")
        p[0] = p[5]
    else:
        p.parser.var.update({p[1] : p.parser.startup})
        p.parser.startup += 1
        p[0] = 1 + p[5]
        outputFile.write("PUSHI " + str(p[3]) + "\n")    

def p_Attr_value_empty(p):
    "Attr : id '=' integer ';'"
    if type(p.parser.var.get(p[1])):
        p.parser.var.update({p[1] : p.parser.startup})
        p.parser.startup += 1
        p[0] = 1
        outputFile.write("PUSHI " + str(p[3]) + "\n")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' already defined")
        p[0] = 0

def p_Attr_empty(p):
    "Attr : id ';'"
    if type(p.parser.var.get(p[1])):
        p.parser.var.update({p[1] : p.parser.startup})
        p.parser.startup += 1
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' already defined")
    p[0] = 0

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

def p_Line_Print_String(p):
    "Line : printS '(' String ')'"

def p_Line_Read_Attr(p):
    "Line : read '(' id ')'"
    outputFile.write("\tREAD\n")
    outputFile.write("\tATOI\n")
    outputFile.write("\tSTOREG " + str(p.parser.var.get(p[3])) + "\n")

def p_Line_Read_Array(p):
    "Line : read '(' id '[' integer ']' ')'"
    id = p.parser.var.get(p[3])
    if type(id) is tuple:
        outputFile.write("\tPUSHGP\n\tPUSHI " + str(id[0]) + "\n\tPADD\n")
        outputFile.write("\tPUSHI " + str(p[5]) + "\n")
        outputFile.write("\tREAD\n")
        outputFile.write("\tATOI\n")
        outputFile.write("\tSTOREN\n")
    elif type(id):
        print("Semantic error:")
        print("\tVariable \'" + p[3] + "\' is not an array.")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[3] + "\' not defined.")


    
def p_Line_Read_Array_Id(p):
    "Line : read '(' id '[' id ']' ')'"
    id = p.parser.var.get(p[3])
    if type(id) is tuple:
        id1 = p.parser.var.get(p[5])
        if type(id1):
            outputFile.write("\tPUSHGP\n\tPUSHI " + str(id[0]) + "\n\tPADD\n")
            outputFile.write("\tPUSHG " + str(p.parser.var.get(p[5])) + "\n")
            outputFile.write("\tREAD\n")
            outputFile.write("\tATOI\n")
            outputFile.write("\tSTOREN\n")
        else:
            print("Semantic error:")
            print("\tVariable \'" + p[5] + "\' not defined.")
    elif type(id):
        print("Semantic error:")
        print("\tVariable \'" + p[3] + "\' is not an array.")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[3] + "\' not defined.")

def p_Line_Store_Attr(p):
    "Line : id '=' Exp ';'"
    id = p.parser.var.get(p[1])
    if type(id) is int or type(id) is tuple:
        outputFile.write("\tSTOREG " + str(p.parser.var.get(p[1])) + "\n")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' not defined.")
    
def p_Line_Store_Attr_Array(p):
    "Line : Array '=' Exp ';'"
    outputFile.write("\tSTOREN\n")

def p_Line_Inc_Attr(p):
    "Line : id '+' '+' ';'"
    outputFile.write("\tPUSHG " + str(p.parser.var.get(p[1], 0)) + "\n")
    outputFile.write("\tPUSHI 1\n\tADD\n")
    outputFile.write("\tSTOREG " + str(p.parser.var.get(p[1])) + "\n")

def p_Line_Dec_Attr(p):
    "Line : id '-' '-' ';'"
    outputFile.write("\tPUSHG " + str(p.parser.var.get(p[1], 0)) + "\n")
    outputFile.write("\tPUSHI 1\nSUB\n")
    outputFile.write("\tSTOREG " + str(p.parser.var.get(p[1])) + "\n")

def p_Line_Cond(p):
    "Line : if Ifcond CondCode"
    pass

def p_Line_While(p):
    "Line : WhileStart WhileLoop '{' Code '}'"
    outputFile.write("\tJUMP " + p[1] + "\n")
    outputFile.write(p[2] + ":\n")

def p_Line_Repeat(p):
    "Line : RepeatStart RepeatLoop '{' Code '}'"
    outputFile.write("\tPUSHG " + str(p.parser.var.get("0")) + "\n\tPUSHI 1\n\tSUB\n")
    outputFile.write("\tSTOREG " + str(p.parser.var.get("0")) + "\n")
    outputFile.write("\tJUMP " + p[1] + "\n")
    outputFile.write(p[2] + ":\n")

def p_Line_Exp(p):
    "Line : '(' Exp ')'"
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
    p[0] = "whileEnd" + str(p.parser.id)
    outputFile.write("\tJZ " + p[0] + "\n")

# Production for WhileLoop
def p_WhileLoop_error(p):
    "WhileLoop : '(' error ')'"
    print("\tError found in 'while' condition.")
    print("\tExpected while condition:\n\t\twhile(condition){code}")
    print("\tExpected condition structure:")
    print('''\t\tCondition : Exp </>/=</>=/==/!= Exp
                Condition and Condition
                Condition or Condition
                !Condition!''')
    outputFile.write("\tPUSHI 0\n")
    p.parser.id += 1
    p[0] = "whileEnd" + str(p.parser.id)
    outputFile.write("\tJZ " + p[0] + "\n")

# Production for Repeat
def p_RepeatStart(p):
    "RepeatStart : repeat '(' Exp"
    outputFile.write("\tSTOREG " + str(p.parser.var.get("0")) + "\n")
    p.parser.id += 1
    p[0] = "repeat" + str(p.parser.id)
    outputFile.write(p[0] + ":\n")

def p_RepeatStart_error(p):
    "RepeatStart : repeat '(' error"
    outputFile.write("\tPUSHI 0\n")
    outputFile.write("\tSTOREG " + str(p.parser.var.get("0")) + "\n")
    p.parser.id += 1
    p[0] = "repeat" + str(p.parser.id)
    outputFile.write(p[0] + ":\n")
    print("\tError found in repeat number.")
    print("\tValid repeat structure:\n\t\trepeat(integer){code}")
    print("\tPlease insert valid integer.")

# Production for RepeatLoop
def p_RepeatLoop(p):
    "RepeatLoop : ')'"
    outputFile.write("\tPUSHG " + str(p.parser.var.get("0")) + "\n\tPUSHI 0\n\tSUP\n")
    p.parser.id += 1
    p[0] = "repeatEnd" + str(p.parser.id)
    outputFile.write("\tJZ " + p[0] + "\n")

# Production rules for Ifcond
def p_Ifcond(p):
    "Ifcond : '(' Cond ')'"
    pass

def p_Ifcond_error(p):
    "Ifcond : '(' error ')'"
    print("\tError found in 'if' condition.")
    print("\tExpected if structure:\n\t\tif(condition){code}\n\t\tif(condition){code}else{code}")
    print("\tExpected condition structure:")
    print('''\t\tCondition : Exp </>/=</>=/==/!= Exp
                Condition and Condition
                Condition or Condition
                !Condition!''')
    outputFile.write("\tPUSHI 0\n")

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

def p_Rel_Supeq(p):
    "Rel : Exp '>' '=' Exp"
    outputFile.write("\tSUPEQ\n")

def p_Rel_Inf(p):
    "Rel : Exp '<' Exp"
    outputFile.write("\tINF\n")

def p_Rel_Infeq(p):
    "Rel : Exp '=' '<' Exp"
    outputFile.write("\tINFEQ\n")

def p_Rel_Equal(p):
    "Rel : Exp '=' '=' Exp"
    outputFile.write("\tEQUAL\n")

def p_Rel_Not_Equal(p):
    "Rel : Exp '!' '=' Exp"
    outputFile.write("\tEQUAL\n")
    outputFile.write("\tNOT\n")

# Production rules for Array
def p_Array(p):
    "Array : id '[' integer ']'"
    id = p.parser.var.get(p[1])
    if type(id):
        if type(id) is tuple:
            outputFile.write("\tPUSHGP\n\tPUSHI " + str(id[0]) + "\n\tPADD\n")
            outputFile.write("\tPUSHI " + str(p[3]) + "\n")
        else:
            outputFile.write("\tPUSHGP\n")
            print("Semantic error:")
            print("\tVariable \'" + p[1] + "\' is not an array.")
    else:
        outputFile.write("\tPUSHGP\n")
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' not defined.")

def p_Array_id(p):
    "Array : id '[' id ']'"
    id = p.parser.var.get(p[1])
    id1 = p.parser.var.get(p[3])
    if type(id):
        if type(id) is tuple:
            if type(id1) is int:
                outputFile.write("\tPUSHGP\n\tPUSHI " + str(id[0]) + "\n\tPADD\n")
                outputFile.write("\tPUSHG " + str(id1) + "\n")
            else:
                outputFile.write("\tPUSHGP\n")
                print("Semantic error:")
                print("\tVariable \'" + p[3] + "\' not defined.")
        else:
            outputFile.write("\tPUSHGP\n")
            print("Semantic error:")
            print("\tVariable \'" + p[1] + "\' is not an array.")
    else:
        outputFile.write("\tPUSHGP\n")
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' not defined.")

# INTEGERS

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

def p_Termo_MOD(p):
    "Termo : Termo '%' Factor"
    outputFile.write("\tMOD\n")

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
    "Atomic : integer"
    outputFile.write("\tPUSHI " + str(p[1])+ "\n")

def p_Atomic_Id(p):
    "Atomic : id"
    id = p.parser.var.get(p[1])
    if type(id):
        outputFile.write("\tPUSHG " + str(id) + "\n")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' not defined.")

def p_Atomic_Array(p):
    "Atomic : id '[' integer ']'"
    id = p.parser.var.get(p[1])
    if type(id):
        if type(id) is tuple:
            outputFile.write("\tPUSHGP\n\tPUSHI " + str(id[0]) + "\n\tPADD\n")
            outputFile.write("\tPUSHI " + str(p[3]) + "\n")
            outputFile.write("\tLOADN\n")
        else:
            print("Semantic error:")
            print("\tVariable \'" + p[1] + "\' is not an array.")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' not defined.")
    
def p_Atomic_Array_Id(p):
    "Atomic : id '[' id ']'"
    id = p.parser.var.get(p[1])
    if type(id):
        if type(id) is tuple:
            if type(p.parser.var.get(p[3])) is int:
                outputFile.write("\tPUSHGP\n\tPUSHI " + str(id[0]) + "\n\tPADD\n")
                outputFile.write("\tPUSHG " + str(p.parser.var.get(p[3])) + "\n")
                outputFile.write("\tLOADN\n")
            else:
                print("Semantic error:")
                print("\tVariable \'" + p[3] + "\' not defined.")
        else:
            print("Semantic error:")
            print("\tVariable \'" + p[1] + "\' is not an array.")
    else:
        print("Semantic error:")
        print("\tVariable \'" + p[1] + "\' not defined.")

# Production rules for signal
def p_Signal_End(p):
    "Signal : '-'"
    outputFile.write("\tPUSHI -1\n")

def p_Signal(p):
    "Signal : Signal '-'"
    outputFile.write("\tPUSHI -1\n")
    outputFile.write("\tMUL\n")

# Production rules for String
def p_String_str(p):
    "String : String '+' string"
    outputFile.write("\tPUSHS " + p[3] + "\n")
    outputFile.write("\tWRITES\n")

def p_String_int(p):
    "String : String '+' id "
    outputFile.write("\tPUSHG " + str(p.parser.var.get(p[3])) + "\n\tSTRI\n\tWRITES\n")

def p_String_str_end(p):
    "String : string"
    outputFile.write("\tPUSHS " + p[1] + "\n")
    outputFile.write("\tWRITES\n")

def p_String_int_end(p):
    "String : id "
    outputFile.write("\tPUSHG " + str(p.parser.var.get(p[1])) + "\n\tSTRI\n")
    outputFile.write("\tWRITES\n")

# Error rule for syntax error
def p_error(p):
    print("YACC ERROR:\n\t" + str(p))
    line_size = p.lexpos - code.rfind('\n', 0, p.lexpos) +1
    print("\tError found on line", p.lineno, "column", line_size)
    if p.type == "id":
        if expected := mostSimilar(p.value):
            print("\tYou wrote \'" + p.value + "\', did you mean to write \'" + expected + "\'?")
        else:
            print("\tUnkown simbol: " + p.value)
            pass
    elif p.type == "start":
        print("\tKeyword 'start' misused, this keyword is utilized in the begining of your code block.")
    elif p.type == "print":
        print("\tKeyword 'print' misused, this keyword prints any integer in the standard output.")
    elif p.type == "printS":
        print("\tKeyword 'printS' misused, this keyword prints any string of characters in the standard output.")
    elif p.type == "print":
        print("\tKeyword 'read' misused, this keyword reads any integer in the standard input.")
    elif p.type == "if":
        print("\tKeyword 'if' misused, this keyword initiates an if statement.")
    elif p.type == "else":
        print("\tKeyword 'else' misused, this keyword must be utilized after an if code block.")
    elif p.type == "repeat":
        print("\tKeyword 'repeat' misused, this keyword loops the given block of code as many times as the result of the given expression.")
    elif p.type == "while":
        print("\tKeyword 'while' misused, this keyword loops the given block of code as long as the given condition is true.")
    elif p.type == "and":
        print("\tKeyword 'and' misused, this keyword is the logical conjunction opetator.")
    elif p.type == "or":
        print("\tKeyword 'or' misused, this keyword is the logical disjunction opetator.")
    elif p.type == "int":
        print("\tKeyword 'int' misused, this keyword indicates the type of a variable.")
    else:
        pass

def mostSimilar(error):
    r = (None,0.4)
    for t in tokens:
        if t != "id" and t != "integer" and t != "string":
            sim = similar(error, t)
            if r[1] < sim:
                r = (t,sim)
    return r[0]
    
def similar(error,token):
    return SequenceMatcher(None, error, token).ratio()

# Build parser
parser = yacc.yacc()

import sys
if len(sys.argv) == 2 and re.search(r'\.txt$',sys.argv[1]):
    path = sys.argv[1]
else:
    path = "/home/baco/Documents/PL2021/Compilador/src/test.txt"

inputFile = open(path,"r")
path = re.sub(r'\.txt$',
        r'.vm',
        path)
outputFile = open(path,"w")
    
# parser state
parser.erros = []
parser.var = {}
parser.id = 0

parser.startup = len(parser.var)

# Read input and parse the whole file
code = inputFile.read()
parser.parse(code)

print("Exited parser")

inputFile.close
outputFile.close