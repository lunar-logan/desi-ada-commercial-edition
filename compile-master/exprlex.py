# exprlex.py
r'''
Project 1 - Write a Lexer
=========================
In the first project, you are going to write a simple lexer for the
expression language.  Please read the complete contents of
this file and carefully complete the steps indicated by comments.

Overview:
---------
The process of lexing is that of taking input text and breaking it
down into a stream of tokens. Each token is like a valid word from the
dictionary.  Essentially, the role of the lexer is to simply make sure
that the input text consists of valid symbols and tokens prior to any
further processing related to parsing.

Each token is defined by a regular expression.  Thus, your primary task
in this first project is to define a set of regular expressions for
the language.  The actual job of lexing will be handled by PLY
(http://www.dabeaz.com/ply).

Specification:
--------------
Your lexer must recognize the following symbols and tokens.  The name
on the left is the token name, the value on the right is the matching
text.

Reserved Keywords:
    CONST   : 'const'
    VAR     : 'var'  
    PRINT   : 'print'

Identifiers:   (Same rules as for Python)
    ID      : Text starting with a letter or '_', followed by any number
              number of letters, digits, or underscores.

Operators and Delimiters:
    PLUS    : '+'
    MINUS   : '-'
    TIMES   : '*'
    DIVIDE  : '/'
    ASSIGN  : '='
    SEMI    : ';'
    LPAREN  : '('
    RPAREN  : ')'

Literals:
    INTEGER : '123'   (decimal)
              '0123'  (octal)
              '0x123' (hex)

    FLOAT   : '1.234'
              '1.234e1'
              '1.234e+1'
              '1.234e-1'
              '1e2'
              '.1234'
              '1234.'

    STRING  : '"Hello World\n"'

Comments:  To be ignored by your lexer
     //             Skips the rest of the line
     /* ... */      Skips a block (no nesting allowed)

Errors: Your lexer must report the following error messages:

     lineno: Illegal char 'c'         
     lineno: Unterminated string     
     lineno: Unterminated comment
     lineno: Bad string escape code '\..'

Testing
-------
For initial development, try running the lexer on a sample input file
such as:

     bash % python exprlex.py sample.e

Carefully study the output of the lexer and make sure that it makes sense.
Once you are reasonably happy with the output, try running the unit tests.

     bash % python test_exprlex.py

The unit tests are designed to stress test various corner cases.
'''
import re

# ----------------------------------------------------------------------
# The following import loads a function error(lineno,msg) that should be
# used to report all error messages issued by your lexer.  Unit tests and
# other features of the compiler will rely on this function.  See the
# file errors.py for more documentation about the error handling mechanism.
from errors import error

# ----------------------------------------------------------------------
# Lexers are defined using the ply.lex library.
#
# See http://www.dabeaz.com/ply/ply.html#ply_nn3
from ply.lex import lex

# ----------------------------------------------------------------------
# Token list. This list identifies the complete list of token names
# to be recognized by your lexer.  Do not change any of these names.
# Doing so will break unit tests.

tokens = [
    # keywords
    'ID','CONST','VAR','PRINT', 'IF', 'ELSE', 'WHILE', 'FUNC', 'RETURN',

    # Operators and delimiters
    'PLUS','MINUS','TIMES','DIVIDE',
    'ASSIGN', 'SEMI', 'LPAREN', 'RPAREN', 'COMMA',
    
    # Literals
    'INTEGER', 'FLOAT', 'STRING', 'BOOL',

    # Relations
    'LT', 'GT', 'LTE', 'GTE', 'EQ', 'NEQ',

    # Boolean operators
    'LAND', 'LOR', 'NOT',

    # Curly braces
    'LCURL', 'RCURL'
]

# ----------------------------------------------------------------------
# Ignored characters (whitespace)
#
# The following characters are ignored completely by the lexer. 
# Do not change.

t_ignore = ' \t\r'

# ----------------------------------------------------------------------
# *** YOU MUST COMPLETE : write the regexs indicated below ***
# 
# Tokens for simple symbols: + - * / = ( ) ; 

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_SEMI      = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LT        = r'\<'
t_GT        = r'\>'
t_LTE       = r'\<='
t_GTE       = r'\>='
t_EQ        = r'=='
t_NEQ       = r'!='
t_LAND      = r'&&'
t_LOR       = r'\|\|'
t_NOT       = r'!'
t_LCURL     = r'\{'
t_RCURL     = r'\}'
t_COMMA     = r','

# ----------------------------------------------------------------------
# *** YOU MUST COMPLETE : write the regexs and additional code below ***
#
# Tokens for literals, INTEGER, FLOAT, STRING. 

# Floating point constant.   You must recognize floating point numbers in
# formats as shown in the following examples:
#
#   1.23, 1.23e1, 1.23e+1, 1.23e-1, 123., .123, 1e1, 0.
#
# The value should be converted to a Python float when lexed
#
# AM notes:
#  - float can have a leading dot, followed by any numbers
#  - float can be a number.number
#  - either of above two forms can have a an exponential form

def t_FLOAT(t):
    r'\d+[eE][-+]?\d+|(\.\d+|\d+\.\d+)([eE][-+]?\d+)?'
    t.value = float(t.value)               # Conversion to Python float
    return t

# Integer constant.  You must recognize integers in all of the following
# formats:
#
#     1234             (decimal)
#     01234            (octal)
#     0x1234 or 0X1234 (hex)
#
# The value should be converted to a Python int when lexed.
def t_INTEGER(t):
    r'(\d+|0[Xx]\d+)'
    # Conversion to a Python int
    if t.value.startswith(('0x','0X')):
        t.value = int(t.value,16)              
    elif t.value.startswith('0'):
        t.value = int(t.value,8)
    else:
        t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(true|false)'
    mapping = {"true": True, "false": False}
    t.value = mapping[t.value]
    return t

# String constant. You must recognize text enclosed in quotes.
# For example:
#
#     "Hello World"
#
# Strings are allowed to have escape codes which are defined by
# a leading backslash.    The following backslash codes must be
# understood:
#      
#       \n    = newline (10)
#       \r    = carriage return (13) 
#       \t    = tab (9)
#       \\    = baskslash char (\)
#       \"    = quote (")
#       \bhh  = byte character code hh  (h is a hex digit)
#
# All other escape codes should result in an error. Note: string literals
# do *NOT* understand the full range of character codes supported by Python.
#
# The token value should be the string with all escape codes replaced by
# their corresponding raw character code.

def _replace_escape_codes(t):
    r'''
    *** YOU MUST IMPLEMENT ***
    
    Replace all of the valid escape codes \.. in a string with
    their raw character code equivalents.   Suggest doing this
    with re.sub()
    '''
    literals = {
        r"\\n": "\n",
        r"\\r": "\r",
        r"\\t": "\t",
        r"\\\\": r"\\",
        r'\\"': r'"'
    }
    re_byte = r".*\\b(?P<val>[0-9a-fA-F]{2}).*"
    byte_pat = re.compile(re_byte)
    for pattern, repl in literals.items():
        t.value = re.sub(pattern, repl, t.value)
    matcher = byte_pat.match(t.value)
    if matcher:
        val = matcher.groupdict()["val"]
        val = chr(int(val, 16))
        # chomping first 2 and last 2 chars of pattern to eliminate .*
        # yes, this is a bit hacky
        t.value = re.sub(re_byte[2:-2], val, t.value)
    # Error to use for reporting a bad escape code
    if False:
        error(t.lexer.lineno,"Bad string escape code '%s'" % escape_code)
    
def t_STRING(t):
    r'\".*?\"'
    # Convert t.value into a string with escape codes replaced by actual values.
    t.value = t.value[1:-1]
    _replace_escape_codes(t)    # Must implement above
    return t

# ----------------------------------------------------------------------
# *** YOU MUST COMPLETE : Write the regex and add keywords ***
#
# Identifiers and keywords. 

# Match a raw identifier.  Identifiers follow the same rules as Python.
# That is, they start with a letter or underscore (_) and can contain
# an arbitrary number of letters, digits, or underscores after that.
keywords = {"var", "const", "print", "if", "else", "while", "func", "return"}
def t_ID(t):
    r'[_A-Za-z][_A-Za-z0-9]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

# *** YOU MUST IMPLEMENT ***
# Add code to match keywords such as 'var','const','print'

# ----------------------------------------------------------------------
# *** YOU MUST COMPLETE : Write the indicated regexes ***
#
# Ignored text.   The following rules are used to ignore text in the
# input file.  This includes comments and blank lines

# One or more blank lines
def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

# C-style comment (/* ... */)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    
# C++-style comment (//...)
def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1

# ----------------------------------------------------------------------
# *** YOU MUST COMPLETE : Add indicated regexs ***
#
# Error handling.  The following error conditions must be handled by
# your lexer.

# Illegal character (generic error handling)
def t_error(t):
    error(t.lexer.lineno,"Illegal character %r" % t.value[0])
    t.lexer.skip(1)

# Unterminated C-style comment
def t_COMMENT_UNTERM(t):
    r'/\*(.|\n)*$'
    error(t.lexer.lineno,"Unterminated comment")

# Unterminated string literal
def t_STRING_UNTERM(t):
    r'\"(\.|.)*?\n'
    error(t.lexer.lineno,"Unterminated string literal")
    t.lexer.lineno += 1
    
# ----------------------------------------------------------------------
#                DO NOT CHANGE ANYTHING BELOW THIS PART
# ----------------------------------------------------------------------
def make_lexer():
    '''
    Utility function for making the lexer object
    '''
    return lex()

if __name__ == '__main__':
    import sys
    from errors import subscribe_errors
    
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s filename\n" % sys.argv[0])
        raise SystemExit(1)

    
    lexer = make_lexer()
    with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
        lexer.input(open(sys.argv[1]).read())
        for tok in iter(lexer.token,None):
            sys.stdout.write("%s\n" % tok)
