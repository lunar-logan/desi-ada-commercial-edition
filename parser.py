import ply.yacc as yacc
import lex
import sys
import os

tokens = lex.tokens
counter = 0
endcounter = 0
precedence = (
('left','PLUS','MINUS'),
('left','TIMES','DIVIDE'),
('right','UMINUS'),
)

def p_program(p):
    '''program : statements'''
    counter=0
    p[0] = '.text\n.globl main\nmain:\n'+p[1]+'li $v0 10\nsyscall'

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p)==2 :
        p[0] = p[1]
    else :
        p[0] =  p[1]+p[2]

def p_statement(p):
    '''statement : simple_stmt'''
    p[0]=p[1]

def p_simple_stmt(p):
    '''simple_stmt : null_stmt
                   | assign_stmt
                   | exit_stmt
                   | if_stmt'''
    p[0] = p[1]

def p_null_stmt(p):
    '''null_stmt : NULL SEMICOLON'''
    p[0] = 'nop\n'

def p_assign_stmt(p):
    '''assign_stmt : IDENTIFIER ASSIGN expression SEMICOLON'''
    p[0] = p[3]+'li $v0 1\nsyscall\n'

def p_expression(p):
    '''expression : relation
                  | expression AND relation
                  | expression OR relation
                  | expression XOR relation'''
    if len(p)==2 :
        p[0]=p[1]
    else :
        p[0]=p[1]+'sw $a0 0($sp)\naddiu $sp $sp -4\n'+p[3]+'lw $t1 4($sp)\n'
        if p[2]=='AND' :
            p[0]+='and'
        elif p[2]=='OR' :
            p[0]+='or'
        else :
            p[0]+='xor'
        p[0]+=' $a0 $t1 a0\naddiu $sp $sp 4\n'

def p_relation(p):
    '''relation : simple_expression
                | simple_expression relational simple_expression'''
    if len(p)==2 :
        p[0]=p[1]
    else :
        p[0]=p[1]+'sw $a0 0($sp)\n'+'addiu $sp $sp -4\n'+p[3]+'lw $t1 4($sp)\n'
        if p[2]=='=' :
            p[0]+= 'seq'
        elif p[2]=='/=' :
            p[0]+= 'sne'
        elif p[2]=='<' :
            p[0]+= 'slt'
        elif p[2]=='<=' :
            p[0]+= 'sle'
        elif p[2]=='>' :
            p[0]+= 'sgt'
        else :
            p[0]+= 'sge'
        p[0]+=' $a0 $t1 $a0\naddiu $sp $sp 4\n'

def p_relational(p):
    '''relational : EQ
                  | NE
                  | LT
                  | LE
                  | GT
                  | GE'''
    p[0]=p[1]

def p_simple_expression(p):
    '''simple_expression : term
                         | PLUS term
                         | MINUS term %prec UMINUS
                         | simple_expression adding term'''
    if len(p)==2 :
        p[0]=p[1]
    elif len(p)==3 :
        if p[1]=='+' :
            p[0]=p[1]
        else :
            p[0]=p[1]+'neg $a0 $a0\n'
    else :
        p[0]=p[1]+'sw $a0 0($sp)\n'+'addiu $sp $sp -4\n'+p[3]+'lw $t1 4($sp)\n'
        if p[2]=='+' :
            p[0]+='add'
        elif p[2]=='-' :
            p[0]+='sub'
        else :
            p[2]+='and'
        p[0]+=' $a0 $t1 $a0\naddiu $sp $sp 4\n'

def p_adding(p):
    '''adding : PLUS
              | MINUS
              | AMPERSAND'''
    p[0]=p[1]

def p_term(p):
    '''term : factor
            | term multiplying factor'''
    if len(p)==2 :
        p[0]=p[1]
    else :
        p[0]=p[1]+'sw $a0 0($sp)\n'+'addiu $sp $sp -4\n'+p[3]+'lw $t1 4($sp)\n'
        if p[2]=='*' :
            p[0]+='mul'
        elif p[2]=='/' :
            p[0]+='div'
        else :
            p[0]='rem'
        p[0]+=' $a0 $t1 $a0\naddiu $sp $sp 4\n'

def p_multiplying(p):
    '''multiplying : TIMES
                   | DIVIDE
                   | REM'''
    p[0]=p[1]

def p_factor(p):
    '''factor : primary
              | NOT primary
              | ABS primary'''
    if len(p)==2 :
        p[0]=p[1]
    elif p[1]=='NOT' :
        p[0]=p[1]+'not $a0 $a0\n'
    else :
        p[0]=p[1]+'abs $a0 $a0\n'

def p_primary(p):
    '''primary : literal
               | parenthesized_primary'''
    p[0]=p[1]

def p_parenthesized_primary(p):
    '''parenthesized_primary : LPAREN expression RPAREN'''
    p[0]=p[2]

def p_literal(p):
    '''literal : NUMBER
               | CHARACTER'''
    p[0]='li $a0 '+str(p[1])+'\n'

def p_if_stmt(p):
    '''if_stmt : IF cond_clauses else_opt END IF SEMICOLON'''
    global counter
    global endcounter
    p[0]=p[2]+p[3]+'l'+str(counter)+':\n'
    counter+=1
    p[0]+='el'+str(endcounter)+':\n'
    endcounter+=1

def p_cond_clauses(p):
    '''cond_clauses : cond_clause
                    | cond_clauses ELSIF cond_clause'''
    if len(p)==2 :
        p[0]=p[1]
    else :
        p[0]=p[1]+p[3]

def p_cond_clause(p):
    '''cond_clause : expression THEN statements'''
    global counter
    p[0]='l'+str(counter)+':\n'+p[1]+'beq $a0 0 l'+str(counter+1)+'\n'+p[3]+'b el'+str(endcounter)+'\n'
    counter+=1

def p_else_opt(p):
    '''else_opt : 
                | ELSE statements'''
    global counter
    if len(p)>1 :
        p[0]='l'+str(counter)+':\n'+p[2]
        counter+=1
    else :
        p[0]=''

def p_exit_stmt(p):
    '''exit_stmt : EXIT'''
    p[0]='li $v0 10\nsyscall\n'

yacc.yacc()
lang='''if (4=3) then a:=0; elsif (2=2) then b:=1; else c:=2; end if; if (2=3) then d:=9; end if; e:=6;'''
print yacc.parse(lang)
