import sys
import lexer
import ply.yacc as yacc
from ast import *
# The token map
tokens = lexer.tokens

# My local symbol table
symTabl = {}


precedence = (
('left', 'PLUS', 'MINUS'),
('left', 'TIMES', 'DIVIDE'),
)
# Grammar description

def p_goal_symbol(p):
    '''goal_symbol : compilation'''
    p[0]=p[1]

#pragmas

#modified
def p_decl(p):
    '''decl    : object_decl
    | number_decl
    | type_decl
    | subtype_decl
    | subprog_decl
    | generic_decl
    | error SEMICOLON'''
    p[0]=p[1]
#end
 
def p_object_decl(p):
    '''object_decl : def_id_s COLON object_qualifier_opt object_subtype_def init_opt SEMICOLON'''
    p[0]=Object_decl(p[1],p[3],p[4],p[5],lineno=p.lineno(2))
       
def p_def_id_s(p):
    '''def_id_s : def_id
    | def_id_s COMMA def_id'''
    if len(p)==2:
        p[0]=Def_id_s([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_def_id(p):
    '''def_id  : IDENTIFIER'''
    Def_id(p[1],lineno=p.lineno(1))
    
def p_object_qualifier_opt(p):
    '''object_qualifier_opt :
    | ALIASED
    | CONSTANT
    | ALIASED CONSTANT'''
    if p[1]=='ALIASED':
        if len(p)==2:
            Object_Aliased(None)
        else:
            Object_Aliased(p[2])
    elif len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
        
def p_object_subtype_def(p):
    '''object_subtype_def : subtype_ind
    | array_type'''
    p[0]=p[1]
    
def p_init_opt(p):
    '''init_opt :
    | IS_ASSIGNED expression'''
    if len(p[1])==3:
        p[0]=p[2]
    else:
        p[0]=None
        
def p_number_decl(p):
    '''number_decl : def_id_s COLON CONSTANT IS_ASSIGNED expression SEMICOLON'''
    p[0]=Number_decl(p[1],p[3],p[5],lineno=p.lineno(2))
    
def p_type_decl(p):
    '''type_decl : TYPE IDENTIFIER discrim_part_opt type_completion SEMICOLON'''
    p[0]=Type_decl(p[2],p[3],p[4],lineno=p.lineno(1))
    
#discrim_part_opt not handled as of now
def p_discrim_part_opt(p):
    '''discrim_part_opt :
    | discrim_part
    | LPAREN BOX RPAREN'''
    pass

def p_type_completion(p):
    '''type_completion :
    | IS type_def'''
    if len(p)==3:
        p[0]=p[2]
    else:
        p[0]=None
    
#modified
def p_type_def(p):
    '''type_def : enumeration_type 
    | integer_type
    | real_type
    | array_type
    | record_type
    | access_type'''
    pass
    p[0]=p[1]
#end
    
def p_subtype_decl(p):
    '''subtype_decl : SUBTYPE IDENTIFIER IS subtype_ind SEMICOLON'''
    p[0]=Subtype_decl(p[2],p[4])
    
def p_subtype_ind(p):
    '''subtype_ind : name constraint
    | name'''
    if len(p)==3:
        p[0]=Subtype_ind(p[1],None)
    else:
        p[0]=Subtype_ind(p[1],p[2])
    
def p_constraint(p):
    '''constraint : range_constraint
    | decimal_digits_constraint'''
    p[0]=p[1]
     
# may be irrelevent
def p_decimal_digits_constraint(p):
    '''decimal_digits_constraint : DIGITS expression range_constr_opt'''
#end
    
#derived_type
    
def p_range_constraint(p):
    '''range_constraint : RANGE range'''
    p[0]=p[1]
    
def p_range(p):
    '''range : simple_expression DOUBLEDOT simple_expression
    | name TICK RANGE
    | name TICK RANGE LPAREN expression RPAREN'''
    if p[2]=='..':
        p[0]=Doubledot_range(p[1],p[3],p.lineno(2))
    elif len(p)==4:
        p[0]=Name_tick(p[1],None,lineno=p.lineno(2))
    else:
        p[0]=Name_tick(p[1],p[5],lineno=p.lineno(2))

def p_enumeration_type(p):
    '''enumeration_type : LPAREN enum_id_s RPAREN'''
    p[0]=p[1]

def p_enum_id_s(p):
    '''enum_id_s : enum_id
    | enum_id_s COMMA enum_id'''
    if len(p)==2:
        p[0]=Enum([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_enum_id(p):
    '''enum_id : IDENTIFIER
    | CHARACTER'''
    p[0]=p[1]
    
def p_integer_type(p):
    '''integer_type : range_spec
    | MOD expression'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=Doubledot_range(0,p[2],1)
        
def p_range_spec(p):
    '''range_spec : range_constraint'''
    p[0]=p[1]
    
def p_range_spec_opt(p):
    '''range_spec_opt :
    | range_spec'''
    if len(p)==2:
        p[0]=p[1]
    else:
        return
    
def p_real_type(p):
    '''real_type : float_type
    | fixed_type'''
    p[0]=p[1]
    
def p_float_type(p):
    '''float_type : DIGITS expression range_spec_opt'''
    p[0]=Float_type(p[2],p[3],lineno=p.lineno(1))
    
def p_fixed_type(p):
    '''fixed_type : DELTA expression range_spec
    | DELTA expression DIGITS expression range_spec_opt'''
    if len(p)==4:
        p[0]=Fixed_type_1(p[2],p[3],lineno=p.lineno(1))
    else:
        p[0]=Fixed_type_2(p[2],p[3],p[4],lineno=p.lineno(1))
    
def p_array_type(p):
    '''array_type : unconstr_array_type
    | constr_array_type'''
    p[0]=p[1]
    
def p_unconstr_array_type(p):
    '''unconstr_array_type : ARRAY LPAREN index_s RPAREN OF component_subtype_def'''
    p[0]=Unconstr_array(p[3],p[6],lineno=p.lineno(1))
    
def p_constr_array_type(p):
    '''constr_array_type : ARRAY iter_index_constraint OF component_subtype_def'''
    p[0]=Constr_array(p[2],p[4],lineno=p.lineno(1))
    
def p_component_subtype_def(p):
    '''component_subtype_def : aliased_opt subtype_ind'''
    p[0]=Component_subtype(p[1],p[2])
    
def p_aliased_opt(p):
    '''aliased_opt : 
    | ALIASED'''
    if len(p)==2:
        p[0]=Array_aliased(p[1])
    else:
        p[0]=Array_aliased(None)
        
def p_index_s(p):
    '''index_s : index
    | index_s COMMA index'''
    if len(p)==2:
        p[0]=Index_s([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_index(p):
    '''index : name RANGE BOX'''
    p[0]=p[1]
      
def p_iter_index_constraint(p):
    '''iter_index_constraint : LPAREN iter_discrete_range_s RPAREN'''
    p[0]=p[2]
    
def p_iter_discrete_range_s(p):
    '''iter_discrete_range_s : discrete_range
    | iter_discrete_range_s COMMA discrete_range'''
    if len(p)==2:
        p[0]=Iter_discrete_range_s([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_discrete_range(p):
    '''discrete_range : name range_constr_opt
    | range'''
    if len(p)==3:
        p[0]=Range_constr(p[1],p[2],lineno=p.lineno(1))
    else:
        p[0]=p[1]
        
def p_range_constr_opt(p):
    '''range_constr_opt :
    | range_constraint'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
        
def p_record_type(p):
    '''record_type : tagged_opt limited_opt record_def'''
    p[0]=Record_type(p[1],p[2],p[3],lineno=p.lineno(1))
    
def p_record_def(p):
    '''record_def : RECORD comp_list END RECORD
    | NULL RECORD'''
    if len(p)==5:
        p[0]=Record_def(p[2],lineno=p.lineno(1))
    else:
        p[0]=None
        
def p_tagged_opt(p):
    '''tagged_opt :
    | TAGGED
    | ABSTRACT TAGGED'''
    if len(p)==2:
        p[0]=p[1]
    elif len(p)==3:
        p[0]=p[1]
        p[0].append(p[1])
    else:
        p[0]=None
        
#modified
def p_comp_list(p):
    '''comp_list : comp_decl_s variant_part_opt
    | variant_part
    | NULL SEMICOLON'''
    if p[1]=='NULL':
        p[0]=None
    elif len(p)==3:
        p[0]=Comp_list_1(p[1],p[2],lineno=p.lineno(1))
    else:
        p[0]=p[1]
        
def p_comp_decl_s(p):
    '''comp_decl_s : comp_decl
    | comp_decl_s comp_decl'''
    if len(p)==2:
        p[0]=Comp_decl_s(p[1])
    else:
        p[0]=p[1]
        p[0].append(p[1])
        
def p_variant_part_opt(p):
    '''variant_part_opt : 
    | variant_part'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
#end
      
def p_comp_decl(p):
    '''comp_decl : def_id_s COLON component_subtype_def init_opt SEMICOLON
    | error SEMICOLON'''
    if len(p)==6:
        p[0]=Comp_decl(p[1],p[3],p[4])
    else:
        pass

def p_discrim_part(p):
    '''discrim_part : LPAREN discrim_spec_s RPAREN'''
    p[0]=p[1]
    
def p_discrim_spec_s(p):
    '''discrim_spec_s : discrim_spec
    | discrim_spec_s SEMICOLON discrim_spec'''
    if len(p)==2:
        p[0]=Disrim_spec_s([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_discrim_spec(p):
    '''discrim_spec : def_id_s COLON access_opt mark init_opt
    | error'''
    if len(p)==6:
        Discrim_spec(p[1],p[3],p[4],p[5],lineno=p.lineno(2))
    else:
        pass
    
def p_access_opt(p):
    '''access_opt :
    | ACCESS'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
 
#modified       
def p_variant_part(p):
    '''variant_part : CASE simple_name IS variant_s END CASE SEMICOLON'''
    p[0]=Variant_part(p[2],p[4],lineno=p.lineno(1))
    
def p_variant_s(p):
    '''variant_s : variant
    | variant_s variant'''
    if len(p)==2:
        p[0]=Variant_s([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[2])
        
def p_variant(p):
    '''variant : WHEN choice_s ARROW comp_list'''
    p[0]=Variant(p[2],p[4],lineno=p.lineno(1))
#end
  
def p_choice_s(p):
    '''choice_s : choice
    | choice_s '|' choice'''
    if len(p)==2:
        p[0]=Choice_s(p[1])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_choice(p):
    '''choice : expression
    | discrete_with_range
    | OTHERS'''
    p[0]=p[1]
    
def p_discrete_with_range(p):
    '''discrete_with_range : name range_constraint
    | range'''
    if len(p)==3:
        p[0]=Range_constr(p[1],p[2],lineno=p.lineno(1))
    else:
        p[0]=p[1]
        
def p_access_type(p):
    '''access_type : ACCESS subtype_ind
    | ACCESS CONSTANT subtype_ind
    | ACCESS ALL subtype_ind
    | ACCESS prot_opt PROCEDURE formal_part_opt
    | ACCESS prot_opt FUNCTION formal_part_opt RETURN mark'''
    if len(p)==3:
        Access_1(p[2],lineno=p.lineno(1))
    elif len(p)==4:
        Access_2(p[2],p[3],lineno=p.lineno(1))
    elif len(p)==5:
        Access_3(p[2],p[4],lineno=p.lineno(1))
    else:
        Access_4(p[2],p[4],p[6],lineno=p.lineno(1))
        
def p_prot_opt(p):
    '''prot_opt :
    | PROTECTED'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
        
def p_decl_part(p):
    '''decl_part :
    | decl_item_or_body_s1'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
        
#decl_item --> unused

#modified
def p_decl_item(p):
    '''decl_item : decl
    | use_clause'''
    p[0]=p[1]
#end
    
def p_decl_item_or_body_s1(p):
    '''decl_item_or_body_s1 : decl_item_or_body
    | decl_item_or_body_s1 decl_item_or_body'''
    if len(p)==2:
        p[0]=Decl_or_body__s1([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[2])
        
def p_decl_item_or_body(p):
    '''decl_item_or_body : body
    | decl_item'''
    p[0]=p[1]
    
#modified
def p_body(p):
    '''body : subprog_body'''
    p[0]=p[1]
#end
    
def p_name(p):
    '''name : simple_name
    | indexed_comp
    | selected_comp
    | attribute
    | operator_symbol'''
    p[0]=p[1]
    
def p_mark(p):
    '''mark : simple_name
    | mark TICK attribute_id
    | mark DOT simple_name'''
    if len(p)==2:
        p[0]=Mark(p[1],None,lineno=p.lineno(1))
    else:
        p[0]=Mark(p[1],p[3],lineno=p.lineno(2))
        
def p_simple_name(p):
    '''simple_name : IDENTIFIER'''
    p[0]=p[1]
    
def p_compound_name(p):
    '''compound_name : simple_name
    | compound_name DOT simple_name'''
    if len(p)==2:
        p[0]=Compound_name(None,p[1],lineno=p.lineno(1))
    else:
        p[0]=Compound_name(p[1],p[3],lineno=p.lineno(2))
        
def p_c_name_list(p):
    '''c_name_list : compound_name
     | c_name_list COMMA compound_name'''
    if len(p)==2:
        p[0]=C_name_list([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_used_char(p):
    '''used_char : CHARACTER'''
    p[0]=p[1]
    
def p_operator_symbol(p):
    '''operator_symbol : STRING'''
    p[0]=p[1]
    
def p_indexed_comp(p):
    '''indexed_comp : name LPAREN value_s RPAREN'''
    p[0]=Indexed_comp(p[1],p[3],lineno=p.lineno(2))
    
def p_value_s(p):
    '''value_s : value
    | value_s COMMA value'''
    if len(p)==2:
        p[0]=Value_s([p[1]])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_value(p):
    '''value : expression
    | comp_assoc
    | discrete_with_range
    | error'''
    p[0]=p[1]
    
def p_selected_comp(p):
    '''selected_comp : name DOT simple_name
    | name DOT used_char
    | name DOT operator_symbol
    | name DOT ALL'''
    p[0]=Selected_comp(p[1],p[3],lineno=p.lineno(2))
    
def p_attribute(p):
    '''attribute : name TICK attribute_id'''
    p[0]=Attribute(p[1],p[3],lineno=p.lineno(2))
    
def p_attribute_id(p):
    '''attribute_id : IDENTIFIER
    | DIGITS
    | DELTA
    | ACCESS'''
    p[0]=p[1]
    
def p_literal(p):
    '''literal : NUMBER
    | used_char
    | NULL'''
    p[0]=p[1]
    
def p_aggregate(p):
    '''aggregate : LPAREN comp_assoc RPAREN
    | LPAREN value_s_2 RPAREN
    | LPAREN expression WITH value_s RPAREN
    | LPAREN expression WITH NULL RECORD RPAREN
    | LPAREN NULL RECORD RPAREN'''
    if len(p)==4:
        p[0]=Aggregate_1(p[2],lineno=p.lineno(1))
    elif len(p)==6:
        p[0]=Aggregate_2(p[2],p[4],lineno=p.lineno(1))
    elif len(p)==7:
        p[0]=Aggregate_3(p[2],p.lineno(1))
    else:
        p[0]=Aggregate_3(None,lineno=p.lineno(1))
        
def p_value_s_2(p):
    '''value_s_2 : value COMMA value
    | value_s_2 COMMA value'''
    if len(p)==2:
        p[0]=Value_s_2([p[1]])
        p[0].append(p[3])
    else:
        p[0]=p[1]
        p[0].append(p[3])
        
def p_comp_assoc(p):
    '''comp_assoc : choice_s ARROW expression'''
    p[0]=Comp_assoc(p[1],p[3],lineno=p.lineno(2))

def p_expression(p):
    '''expression : relation
    | expression logical relation
    | expression short_circuit relation'''
    if len(p)==2:
        p[0]=p[1]
    elif p[2]=='AND' | p[2]=='OR' | p[2]=='XOR' :
        p[0]=Logical_op(p[2],p[1],p[3],lineno=p.lineno(2))
    else :
        p[0]=Short_circuit(p[2],p[1],p[3],lineno=p.lineno(2))
    
def p_logical(p):
    '''logical : AND
    | OR
    | XOR'''
    p[0]=p[1]
    
def p_short_circuit(p):
    '''short_circuit : AND THEN
    | OR ELSE'''
    p[0]=p[1]
    p[0].append(p[1])

def p_relation(p):
    '''relation : simple_expression
    | simple_expression relational simple_expression
    | simple_expression membership range
    | simple_expression membership name'''
    if len(p)==2:
        p[0]=p[1]
    elif p[1]=='IN' | p[1]=='NOT IN':
        Membership(p[2],p[1],p[3],lineno=p.lineno(2))
    else:
        Relational(p[2],p[1],p[3],lineno=p.lineno(2))
        
def p_relational(p):
    '''relational : EQ
    | NE
    | LT
    | LE
    | GT
    | GE'''
    p[0]=p[1]
    
def p_membership(p):
    '''membership : IN
    | NOT IN'''
    p[0]=p[1]
    if len(p)==3:
        p[0]=p[0].append(p[1])
        
def p_simple_expression(p):
    '''simple_expression : unary term
    | term
    | simple_expression adding term'''
    if len(p)==3:
        Unary_op(p[0],p[1],lineno=p.lineno(1))
    if len(p)==2:
        p[0]=p[1]
    else:
        Adding(p[2],p[1],p[3],lineno=p.lineno(2))
        
def p_unary(p):
    '''unary   : PLUS
    | MINUS'''
    p[0]=p[1]
    
def p_adding(p):
    '''adding  : PLUS
    | MINUS
    | AMPERSAND'''
    p[0]=p[1]

def p_term(p):
    '''term    : factor
    | term multiplying factor'''
    if len(p)==2:
        p[0]=p[1]
    else:
        Multiplying(p[2],p[1],p[3],lineno=p.lineno(2))
    
def p_multiplying(p):
    '''multiplying : TIMES
    | DIVIDE
    | MOD
    | REM'''
    p[0]=p[1]
    
def p_factor(p):
    '''factor : primary
    | NOT primary
    | ABS primary
    | primary POW primary'''
    if p[1]=='NOT':
        Not(p[1])
    elif p[1]=='ABS':
        Abs(p[1])
    elif len(p)==2:
        p[0]=p[1]
    else:
        Pow(p[1],p[3],lineno=p.lineno(2))
    
def p_primary(p):
    '''primary : literal
    | name
    | allocator
    | qualified
    | parenthesized_primary'''
    p[0]=p[1]
    
def p_parenthesized_primary(p):
    '''parenthesized_primary : aggregate
    | LPAREN expression RPAREN'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=p[2]
    
def p_qualified(p):
    '''qualified : name TICK parenthesized_primary'''
    p[0]=Qualified(p[1],p[3],lineno=p.lineno(2))
    
def p_allocator(p):
    '''allocator : NEW name
    | NEW qualified'''
    p[0]=New(p[2],lineno=p.lineno(1))
    
def p_statement_s(p):
    '''statement_s : statement
    | statement_s statement'''
    if len(p)==2 :
        p[0] = Statement_s([p[1]])
    else :
        p[0] = p[1]
        p[0].append(p[2]) 

#modified
def p_statement(p):
    '''statement : unlabeled'''
    p[0]=p[1]
    
def p_unlabeled(p):
    '''unlabeled : simple_stmt
    | compound_stmt'''
    p[0]=p[1]
    
def p_simple_stmt(p):
    '''simple_stmt : NULL_stmt
    | assign_stmt
    | exit_stmt
    | return_stmt
    | goto_stmt
    | procedure_call
    | error SEMICOLON'''
    p[0]=p[1]
    
def p_compound_stmt(p):
    '''compound_stmt : if_stmt
    | case_stmt
    | loop_stmt
    | block'''
    p[0]=p[1]
#end

#label
  
def p_NULL_stmt(p):
    '''NULL_stmt : NULL SEMICOLON'''
    p[0]=None
    
def p_assign_stmt(p):
    '''assign_stmt : name IS_ASSIGNED expression SEMICOLON'''
    p[0]=Assign_Stmt(p[1],p[3],lineno=p.lineno(2))
    
def p_if_stmt(p):
    '''if_stmt : IF cond_clause_s else_opt END IF SEMICOLON'''
    p[0] = If_stmt(p[2], p[3], lineno=p.lineno(1))
    
def p_cond_clause_s(p):
    '''cond_clause_s : cond_clause
    | cond_clause_s ELSIF cond_clause'''
    if len(p)==2 :
        p[0]=p[1]
    else :
        p[0]=If_stmt(p[1],p[2],lineno=p.lineno(2))
        
def p_cond_clause(p):
    '''cond_clause : cond_part statement_s'''
    p[0]=Cond_clause(p[0],p[1])
    
def p_cond_part(p):
    '''cond_part : condition THEN'''
    p[0]=p[1]
    
def p_condition(p):
    '''condition : expression'''
    p[0]=p[1]
    
def p_else_opt(p):
    '''else_opt :
    | ELSE statement_s'''
    if len(p)==1 :
        p[0]=Cond_clause()
    else :
        p[0]=Cond_clause()

#modified
def p_case_stmt(p):
    '''case_stmt : CASE expression IS alternative_s END CASE SEMICOLON'''
    p[0]=Case_stmt(p[2],p[4],lineno=p.lineno(1))
#end

def p_alternative_s(p):
    '''alternative_s :
    | alternative_s alternative'''
    if len(p)==3:
        p[0]=p[1]
        p[0].append(p[2])
    else:
        p[0]=None
    
def p_alternative(p):
    '''alternative : WHEN choice_s ARROW statement_s'''
    p[0]=Alternative(p[2],p[3],lineno=p.lineno(1))

def p_loop_stmt(p):
    '''loop_stmt : label_opt iteration basic_loop id_opt SEMICOLON'''
    p[0]=Loop_stmt(p[0],p[1],p[2],p[3],lineno=p.lineno(3))
    
def p_label_opt(p):
    '''label_opt :
    | IDENTIFIER COLON'''
    if len(p)==3:
        p[0]=p[1]
    else:
        p[0]=None
    
def p_iteration(p):
    '''iteration :
    | WHILE condition
    | iter_part reverse_opt discrete_range'''
    if len(p)==3:
        p[0]=p[2]
    elif len(p)==4:
        p[0]=For_loop(p[1],p[2],p[3],lineno=p.lineno(1))
    else:
        p[0]=None
        
def p_iter_part(p):
    '''iter_part : FOR IDENTIFIER IN'''
    p[0]=p[2]
    
def p_reverse_opt(p):
    '''reverse_opt :
    | REVERSE'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
    
def p_basic_loop(p):
    '''basic_loop : LOOP statement_s END LOOP'''
    p[0]=p[2]
    
def p_id_opt(p):
    '''id_opt :
    | designator'''
    p[0]=p[1]

#modified
def p_block(p):
    '''block : label_opt block_body END id_opt SEMICOLON'''
    p[0]=Block(p[1],p[2],p[4],lineno=p.lineno(3))
#end

#block_decl

def p_block_body(p):
    '''block_body : BEGIN handled_stmt_s'''
    p[0]=p[2]

#modified
def p_handled_stmt_s(p):
    '''handled_stmt_s : statement_s'''
    p[0]=p[1]
#end

#exception_handle

def p_exit_stmt(p):
    '''exit_stmt : EXIT name_opt when_opt SEMICOLON'''
    p[0]=Exit_stmt(p[2],p[3])
    
def p_name_opt(p):
    '''name_opt :
    | name'''
    p[0] = p[1]
    
def p_when_opt(p):
    '''when_opt :
    | WHEN condition'''
    if p[1] is None:
        p[0] = None
    else:
        p[0] = When_cond(p[2],lineno=p.lineno(1))
        
def p_return_stmt(p):
    '''return_stmt : RETURN SEMICOLON
    | RETURN expression SEMICOLON'''
    if len(p)==3:
        Return_stmt(None);
    else:
        Return_stmt(p[2],lineno=p.lineno(1))
        
def p_goto_stmt(p):
    '''goto_stmt : GOTO name SEMICOLON'''
    p[0]=Goto_stmt(p[2],lineno=p.lineno(2))
   
#modified 
def p_subprog_decl(p):
    '''subprog_decl : subprog_spec SEMICOLON
    | generic_subp_inst SEMICOLON'''
    p[0]=p[1]
#end

def p_subprog_spec(p):
    '''subprog_spec : PROCEDURE compound_name formal_part_opt
    | FUNCTION designator formal_part_opt RETURN name
    | FUNCTION designator '''
    if p[1]=='PROCEDURE':
        Procedure(p[2],p[3],lineno=p.lineno(1))
    elif len(p)==6:
        Function(p[2],p[3],p[5],lineno=p.lineno(1))
    else:
        Function(p[2],None,None,lineno=p.lineno(1))
        
def p_designator(p):
    '''designator : compound_name
    | STRING'''
    p[0]=p[1]
    
def p_formal_part_opt(p):
    '''formal_part_opt : 
    | formal_part'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=None
        
def p_formal_part(p):
    '''formal_part : LPAREN param_s RPAREN'''
    p[0]=p[1]
    
def p_param_s(p):
    '''param_s : param
    | param_s SEMICOLON param'''
    if len(p)==2 :
        p[0] = Param_s([p[1]])
    else :
        p[0] = p[1]
        p[0].append(p[3])
         
def p_param(p):
    '''param : def_id_s COLON mode mark init_opt
    | error'''
    if len(p)==6:
        p[0]=Param(p[1],p[3],p[4],p[5])
    else:
        pass
    
def p_mode(p):
    '''mode :
    | IN
    | OUT
    | IN OUT
    | ACCESS'''
    p[0]=p[1]
    
def p_subprog_spec_is_push(p):
    '''subprog_spec_is_push : subprog_spec IS'''
    pass
    p[0]=Is_push(p[1],lineno=p.lineno(p[2]))
    
def p_subprog_body(p):
    '''subprog_body : subprog_spec_is_push decl_part block_body END id_opt SEMICOLON'''
    p[0]=Subprog_body(p[1],p[2],p[3],p[5],lineno=p.lineno(4))
    
def p_procedure_call(p):
    '''procedure_call : name SEMICOLON'''
    p[0]=Procedure_call(p[1],lineno=p.lineno(2))

#pkg_decl
#private_type

def p_limited_opt(p):
    '''limited_opt :
    | LIMITED'''
    if len(p)==2:
        p[0]=Limited(p[1])
    else:
        p[0]=Limited(None)

def p_use_clause(p):
    '''use_clause : USE name_s SEMICOLON
    | USE TYPE name_s SEMICOLON'''
    if len(p)==4:
        p[0]=Use(None,p[2],lineno=p.lineno(1))
    else:
        p[0]=Use(p[2],p[3],lineno=p.lineno(1))
    
def p_name_s(p):
    '''name_s : name
    | name_s COMMA name'''
    if len(p)==2 :
        p[0] = Name_s([p[1]])
    else :
        p[0] = p[1]
        p[0].append(p[3]) 
    
#renames
#task
#prot
#entry
#accept_stmt
#delay_stmt
#select_stmt
#abort_stmt

#modified
def p_compilation(p):
    '''compilation :
    | compilation comp_unit'''
    if len(p)==2:
        p[0]=p[1]
        p[0].append(p[1])
    else:
        p[0]=None
        
def p_comp_unit(p):
    '''comp_unit : context_spec private_opt unit
    | private_opt unit'''
    if len(p)==4:
        p[0]=Comp_unit(p[1],p[2],p[3],lineno=p.lineno(3))
    else:
        p[0]=Comp_unit(None,p[1],p[2],lineno=p.lineno(3))
        
def p_private_opt(p):
    '''private_opt :
    | PRIVATE'''
    if len(p)==2:
        p[0]=Private(p[1])
    else:
        p[0]=Private(None)
        
def p_context_spec(p):
    '''context_spec : with_clause use_clause_opt
    | context_spec with_clause use_clause_opt'''
    if len(p)==3 :
        p[0] = Context_spec([p[1].append(p[2])])
    else :
        p[0] = p[1]
        p[0].append(p[2])
        p[0].append(p[3])
#end

def p_with_clause(p):
    '''with_clause : WITH c_name_list SEMICOLON'''
    p[0]=With_clause(p[2],lineno=p.lineno(1))
    
def p_use_clause_opt(p):
    '''use_clause_opt :
    | use_clause_opt use_clause'''
    if p[1] is None:
        p[0]=None
    else:
        p[0]=p[1]
        p[0].append(p[1])

#modified
def p_unit(p):
    '''unit : subprog_decl
    | subprog_body
    | generic_decl'''
    p[0]=p[1]
#end

#body_stub
#exception
#raise_stmt
#reque_stmt

#modified
def p_generic_decl(p):
    '''generic_decl : generic_formal_part subprog_spec SEMICOLON'''
    p[0]=Generic_decl(p[1],p[2],lineno=p.lineno(3))
#end

def p_generic_formal_part(p):
    '''generic_formal_part : GENERIC
    | generic_formal_part generic_formal'''
    if len(p)==2 :
        p[0] = Generic([p[1].append(p[2])])
    else :
        p[0] = p[1]
        p[0].append(p[2])
        
def p_generic_formal(p):
    '''generic_formal : param SEMICOLON
    | use_clause'''
    p[0]=p[1]

#generic_related

def p_generic_subp_inst(p):
    '''generic_subp_inst : subprog_spec IS generic_inst'''
    p[0]=Gen_subp_inst(p[1],p[3])

#generic_pkg

def p_generic_inst(p):
    '''generic_inst : NEW name'''
    p[0]=New(p[2],lineno=p.lineno(1))
    
#rep_spec
#code_stmt

def p_empty(t):
    'empty : '
    pass

def make_parser():
    parser = yacc.yacc()
    return parser

if __name__ == '__main__':
    import lexer
    import sys
    from errors import *
    lexer = lexer.make_lexer()
    parser = make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())

    # Output the resulting parse tree structure
    for depth,node in flatten(program):
        print("%s%s" % (" "*(4*depth),node))
