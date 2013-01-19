import ply.lex as lex

reserved = ('ABORT', 'ELSE', 'NEW', 'RETURN', 'ABS', 'ELSIF', 'NOT', 'REVERSE', 'ABSTRACT', 'END', 'NULL',
'ACCEPT', 'ENTRY', 'SELECT', 'ACCESS', 'EXCEPTION', 'OF', 'SEPARATE', 'ALIASED', 'EXIT', 'OR',
'SOME', 'ALL', 'OTHERS', 'SUBTYPE', 'AND', 'FOR', 'OUT', 'SYNCHRONIZED', 'ARRAY', 'FUNCTION',
'OVERRIDING', 'AT', 'TAGGED', 'GENERIC', 'PACKAGE', 'TASK', 'BEGIN', 'GOTO', 'PRAGMA', 'TERMINATE',
'BODY', 'PRIVATE', 'THEN', 'IF', 'PROCEDURE', 'TYPE', 'CASE', 'IN', 'PROTECTED', 'CONSTANT',
'INTERFACE', 'UNTIL', 'IS', 'RAISE', 'USE', 'DECLARE', 'RANGE', 'DELAY', 'LIMITED', 'RECORD', 'WHEN',
'DELTA', 'LOOP', 'REM', 'WHILE', 'DIGITS', 'RENAMES', 'WITH', 'DO', 'MOD', 'REQUEUE', 'XOR')

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
          'TICK',       # '
          'LPAREN',     # ( 
          'RPAREN',     # ) 
          'COMMA',       # ,
          'DOT',        # .
          'COLON',      # :
          'SEMICOLON',  # ;
          'VLINE',      # |
          'ARROW',      # =>
          'DOUBLEDOT',  # ..
          'ASSIGN',     # :=
          'LLB',        # << Left Label Bracket
          'RLB',        # >> Right Label Bracket
          'BOX',        # <> 
          'NUMBERSIGN', # #
          'LSQB',       # [
          'RSQB',       # ]
          'LCB',        # {
          'RCB',        # }
          
)

#Definition of each operator
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_AMPERSAND     = r'&'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_POW           = r'\*\*'
t_NE            = r'/='
t_EQ            = r'='
t_LT            = r'<'
t_LE            = r'<='
t_GE            = r'>='
t_GT            = r'>'
t_TICK          = r"'"
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_COMMA         = r'\,'
t_DOT           = r'\.'
t_COLON         = r':'
t_SEMICOLON     = r';'
t_VLINE         = r'\|'
t_ARROW         = r'=>'
t_DOUBLEDOT     = r'\.\.'
t_ASSIGN        = r':='
t_LLB           = r'<<'
t_RLB           = r'>>'
t_BOX           = r'<>'
t_NUMBERSIGN    = r'\#'
t_LSQB          = r'\['
t_RSQB          = r'\]'
t_LCB           = r'\{'
t_RCB           = r'\}'
# Definition of operators ends

#Creating a map of each keyword
reserved_map = {}
for key in reserved:
    reserved_map[key.lower()] = key

# Defining explicit states for ignoring the comments    
states = (
          ('adacomment', 'exclusive'),
)
def t_adacomment(t):
    r'--[^\n]*'
    t.lexer.begin('adacomment')
    
def t_adacomment_end(t):
    r'\n'
    t.lexer.lineno += 1  # t.value.count('\n')
    t.lexer.begin('INITIAL')
    pass

def t_adacomment_error(t):
    t.lexer.skip(1)

##r'[a-zA-Z](?:[a-zA-Z0-9_]*[a-zA-Z0-9])*'  
def t_IDENTIFIER(t):    
    r'[a-zA-Z](?:_*[a-zA-Z0-9]+)*'  
    t.type = reserved_map.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'-?[0-9]*\.?[0-9]+([Ee]?[+\-]?[0-9]+)?'
    v = t.value
    if '.' in v:
        t.value = float(v)
    else:
        t.value = int(t.value)
    return t
#
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_CHARACTER(t):
    r'\'[^\']?\''
    t.value = t.value[1:-1]
    return t

t_ignore = " \t\r\n\v"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

########### Lexer Ends Here ##########################

lang = """
with Ada.Text_IO; use Ada.Text_IO;
procedure Hello is
A: Float;
begin -- hjgyugy
    A:=-.6e+6;
  Put_Line ("Hello, world!");
  Put(Float'Image(A));
end Hello;
 !!"""
adalexer = lex.lex()
adalexer.input(lang)
while True:
    tok = adalexer.token()
    if not tok: break
    print tok
     
