import ply.lex as lex
import sys
import os, re
reserved = ('ABORT', 'ELSE', 'NEW', 'RETURN', 'ABS', 'ELSIF', 'NOT', 'REVERSE', 'ABSTRACT', 'END', 'NULL',
'ACCEPT', 'ENTRY', 'SELECT', 'ACCESS', 'EXCEPTION', 'OF', 'SEPARATE', 'ALIASED', 'EXIT', 'OR',
'SOME', 'ALL', 'OTHERS', 'SUBTYPE', 'AND', 'FOR', 'OUT', 'SYNCHRONIZED', 'ARRAY', 'FUNCTION',
'OVERRIDING', 'AT', 'TAGGED', 'GENERIC', 'PACKAGE', 'TASK', 'BEGIN', 'GOTO', 'PRAGMA', 'TERMINATE',
'BODY', 'PRIVATE', 'THEN', 'IF', 'PROCEDURE', 'TYPE', 'CASE', 'IN', 'PROTECTED', 'CONSTANT',
'INTERFACE', 'UNTIL', 'IS', 'RAISE', 'USE', 'DECLARE', 'RANGE', 'DELAY', 'LIMITED', 'RECORD', 'WHEN',
'DELTA', 'LOOP', 'REM', 'WHILE', 'DIGITS', 'RENAMES', 'WITH', 'DO', 'MOD', 'REQUEUE', 'XOR', 'TRUE', 'FALSE')

tokens = reserved + (
          'IDENTIFIER',
          'NUMBER',
          'CHARACTER',
          'STRING',
          'DELIMITER',
          'COMMENT',
          # Operators
          'PLUS', 'MINUS', 'AMPERSAND', 'TIMES', 'DIVIDE', 'POW',
          'NE', 'EQ', 'LE', 'LT', 'GE', 'GT',
          # Delims
          'TICK', # '
          'LPAREN', # (
          'RPAREN', # )
          'COMMA', # ,
          'DOT', # .
          'COLON', # :
          'SEMICOLON', # ;
          'VLINE', # |
          'ARROW', # =>
          'DOUBLEDOT', # ..
          'IS_ASSIGNED', # :=
          'LLB', # << Left Label Bracket
          'RLB', # >> Right Label Bracket
          'BOX', # <>
          # Special characters
          'QUOTE',
          'NUMBERSIGN', # #
          'LSQB', # [
          'RSQB', # ]
          'LCB', # {
          'RCB', # }
          
)

#Definition of each operator
t_QUOTE = r'\"'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_AMPERSAND =   r'&'
t_TIMES =       r'\*'
t_DIVIDE =      r'/'
t_POW =         r'\*\*'
t_NE = r'/='
t_EQ = r'='
t_LT = r'<'
t_LE = r'<='
t_GE = r'>='
t_GT = r'>'
t_TICK = r"'"
t_LPAREN =      r'\('
t_RPAREN =      r'\)'
t_COMMA =       r'\,'
t_DOT =         r'\.'
t_COLON =       r':'
t_SEMICOLON =   r';'
t_VLINE =       r'\|'
t_ARROW = r'=>'
t_DOUBLEDOT = r'\.\.'
t_IS_ASSIGNED = r':='
t_LLB = r'<<'
t_RLB = r'>>'
t_BOX = r'<>'
t_NUMBERSIGN = r'\#'
t_LSQB = r'\['
t_RSQB = r'\]'
t_LCB = r'\{'
t_RCB = r'\}'

# Definition of operators ends

# Defining explicit states for ignoring the comments
states = (
          ('adacomment', 'exclusive'),
)
def t_adacomment(t):
    r'--[^\n]*'
    t.lexer.begin('adacomment')
    
def t_adacomment_end(t):
    r'\n'
    t.lexer.lineno += 1 # t.value.count('\n')
    t.lexer.begin('INITIAL')

def t_adacomment_error(t):
    t.lexer.skip(1)


##r'[a-zA-Z](?:[a-zA-Z0-9_]*[a-zA-Z0-9])*'
def t_IDENTIFIER(t):
    r'[a-zA-Z](?:_*[a-zA-Z0-9]+)*'
    t.value = t.value.lower()
    if t.value.upper() in reserved :
        t.type = t.value.upper()
    else :
        t.type = 'IDENTIFIER'
    return t

def __is_valid(x, base):
    a = "0123456789abcdef"
    c = a[0:base]
    p = r"[^" + c + "_.]+"
    if re.search(p, x, re.I) != None:
            return False
    return True

def t_NUMBER(t):
    r'(?:(?:[0-9](_?[0-9])*\#[0-9a-fA-F](_?[0-9a-fA-F])*(\.?[0-9a-fA-F](_?[0-9a-fA-F])*)?\#([Ee][+\-]?[0-9](_?[0-9])*)?)|[0-9](_?[0-9])*(?:(?:\.[0-9](_?[0-9])*([Ee][+\-]?[0-9](_?[0-9])*)?)|(?:([Ee]\+?[0-9](_?[0-9])*)?)))'
    t.value = t.value.replace('_','')
    try:
        if '#' in t.value:
            h1 = t.value.index('#')
            h2 = h1 + t.value[h1+1:].index('#') + 1
            base, num, exp = t.value[0:h1], t.value[h1+1:h2], t.value[h2+1:]
            ##print base, num, exp
            if exp !=None and len(exp) > 0:
                exp = exp[1:]
                exp = int(exp)
            else: exp = 0
            base = int(base)
            if base <= 1 or base > 16: print "WARNING: Invalid base of the number used"
            if __is_valid(num, base) == False:
                print "WARNING: Incorrect symbols used in the number with base",base
            if '.' not in num:
                #its a integer
                num = int(num, base)
                t.value = num*pow(base, exp)
        elif '.' in t.value or 'e' in t.value or 'E' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
    except:
        print "WARNING: ",sys.exc_info()[0] 
    return t

t_ignore = " \t\r\v\x0c"

#r'"[^"]*"'
#r'"([^"\\]|(\\.))*"'
def t_STRING(t):
    r'"(?:[^"\\]|(?:\\.))*"'
    t.value = t.value[1:-1]
    return t

def t_CHARACTER(t):
    r'\'[^\']?\''
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex();
