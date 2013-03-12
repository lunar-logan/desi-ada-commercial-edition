import sys
import lexer
import ply.yacc as yacc

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
    pass

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
    pass
#end

def p_object_decl(p):
    '''object_decl : def_id_s COLON object_qualifier_opt object_subtype_def init_opt SEMICOLON'''
    pass
def p_def_id_s(p):
    '''def_id_s : def_id
    | def_id_s COMMA def_id'''
    pass
def p_def_id(p):
    '''def_id  : IDENTIFIER'''
    pass
def p_object_qualifier_opt(p):
    '''object_qualifier_opt :
    | ALIASED
    | CONSTANT
    | ALIASED CONSTANT'''
    pass
def p_object_subtype_def(p):
    '''object_subtype_def : subtype_ind
    | array_type'''
    pass
def p_init_opt(p):
    '''init_opt :
    | IS_ASSIGNED expression'''
    pass
def p_number_decl(p):
    '''number_decl : def_id_s COLON CONSTANT IS_ASSIGNED expression SEMICOLON'''
    pass
def p_type_decl(p):
    '''type_decl : TYPE IDENTIFIER discrim_part_opt type_completion SEMICOLON'''
    pass
def p_discrim_part_opt(p):
    '''discrim_part_opt :
    | discrim_part
    | LPAREN BOX RPAREN'''
    pass
def p_type_completion(p):
    '''type_completion :
    | IS type_def'''
    pass

#modified
def p_type_def(p):
    '''type_def : enumeration_type 
    | integer_type
    | real_type
    | array_type
    | record_type
    | access_type'''
    pass
#end

def p_subtype_decl(p):
    '''subtype_decl : SUBTYPE IDENTIFIER IS subtype_ind SEMICOLON'''
    pass
def p_subtype_ind(p):
    '''subtype_ind : name constraint
    | name'''
    pass
def p_constraint(p):
    '''constraint : range_constraint
    | decimal_digits_constraint'''
    pass
def p_decimal_digits_constraint(p):
    '''decimal_digits_constraint : DIGITS expression range_constr_opt'''
    pass

#derived_type

def p_range_constraint(p):
    '''range_constraint : RANGE range'''
    pass
def p_range(p):
    '''range : simple_expression DOUBLEDOT simple_expression
    | name TICK RANGE
    | name TICK RANGE LPAREN expression RPAREN'''
    pass
def p_enumeration_type(p):
    '''enumeration_type : LPAREN enum_id_s RPAREN'''
    pass
def p_enum_id_s(p):
    '''enum_id_s : enum_id
    | enum_id_s COMMA enum_id'''
    pass
def p_enum_id(p):
    '''enum_id : IDENTIFIER
    | CHARACTER'''
    pass
def p_integer_type(p):
    '''integer_type : range_spec
    | MOD expression'''
    pass
def p_range_spec(p):
    '''range_spec : range_constraint'''
    pass
def p_range_spec_opt(p):
    '''range_spec_opt :
    | range_spec'''
    pass
def p_real_type(p):
    '''real_type : float_type
    | fixed_type'''
    pass
def p_float_type(p):
    '''float_type : DIGITS expression range_spec_opt'''
    pass
def p_fixed_type(p):
    '''fixed_type : DELTA expression range_spec
    | DELTA expression DIGITS expression range_spec_opt'''
    pass
def p_array_type(p):
    '''array_type : unconstr_array_type
    | constr_array_type'''
    pass
def p_unconstr_array_type(p):
    '''unconstr_array_type : ARRAY LPAREN index_s RPAREN OF component_subtype_def'''
    pass
def p_constr_array_type(p):
    '''constr_array_type : ARRAY iter_index_constraint OF component_subtype_def'''
    pass
def p_component_subtype_def(p):
    '''component_subtype_def : aliased_opt subtype_ind'''
    pass
def p_aliased_opt(p):
    '''aliased_opt : 
    | ALIASED'''
    pass
def p_index_s(p):
    '''index_s : index
    | index_s COMMA index'''
    pass
def p_index(p):
    '''index : name RANGE BOX'''
    pass
def p_iter_index_constraint(p):
    '''iter_index_constraint : LPAREN iter_discrete_range_s RPAREN'''
    pass
def p_iter_discrete_range_s(p):
    '''iter_discrete_range_s : discrete_range
    | iter_discrete_range_s COMMA discrete_range'''
    pass
def p_discrete_range(p):
    '''discrete_range : name range_constr_opt
    | range'''
    pass
def p_range_constr_opt(p):
    '''range_constr_opt :
    | range_constraint'''
    pass
def p_record_type(p):
    '''record_type : tagged_opt limited_opt record_def'''
    pass
def p_record_def(p):
    '''record_def : RECORD comp_list END RECORD
    | NULL RECORD'''
    pass
def p_tagged_opt(p):
    '''tagged_opt :
    | TAGGED
    | ABSTRACT TAGGED'''
    pass

#modified
def p_comp_list(p):
    '''comp_list : comp_decl_s variant_part_opt
    | variant_part
    | NULL SEMICOLON'''
    pass
def p_comp_decl_s(p):
    '''comp_decl_s : comp_decl
    | comp_decl_s comp_decl'''
    pass
def p_variant_part_opt(p):
    '''variant_part_opt : 
    | variant_part'''
    pass
#end

def p_comp_decl(p):
    '''comp_decl : def_id_s COLON component_subtype_def init_opt SEMICOLON
    | error SEMICOLON'''
    pass
def p_discrim_part(p):
    '''discrim_part : LPAREN discrim_spec_s RPAREN'''
    pass
def p_discrim_spec_s(p):
    '''discrim_spec_s : discrim_spec
    | discrim_spec_s SEMICOLON discrim_spec'''
    pass
def p_discrim_spec(p):
    '''discrim_spec : def_id_s COLON access_opt mark init_opt
    | error'''
    pass
def p_access_opt(p):
    '''access_opt :
    | ACCESS'''
    pass

#modified
def p_variant_part(p):
    '''variant_part : CASE simple_name IS variant_s END CASE SEMICOLON'''
    pass
def p_variant_s(p):
    '''variant_s : variant
    | variant_s variant'''
    pass
def p_variant(p):
    '''variant : WHEN choice_s ARROW comp_list'''
    pass
#end

def p_choice_s(p):
    '''choice_s : choice
    | choice_s '|' choice'''
    pass
def p_choice(p):
    '''choice : expression
    | discrete_with_range
    | OTHERS'''
    pass
def p_discrete_with_range(p):
    '''discrete_with_range : name range_constraint
    | range'''
    pass
def p_access_type(p):
    '''access_type : ACCESS subtype_ind
    | ACCESS CONSTANT subtype_ind
    | ACCESS ALL subtype_ind
    | ACCESS prot_opt PROCEDURE formal_part_opt
    | ACCESS prot_opt FUNCTION formal_part_opt RETURN mark'''
    pass
def p_prot_opt(p):
    '''prot_opt :
    | PROTECTED'''
    pass
def p_decl_part(p):
    '''decl_part :
    | decl_item_or_body_s1'''
    pass

#decl_item --> unused

#modified
def p_decl_item(p):
    '''decl_item : decl
    | use_clause'''
    pass
#end

def p_decl_item_or_body_s1(p):
    '''decl_item_or_body_s1 : decl_item_or_body
    | decl_item_or_body_s1 decl_item_or_body'''
    pass
def p_decl_item_or_body(p):
    '''decl_item_or_body : body
    | decl_item'''
    pass

#modified
def p_body(p):
    '''body : subprog_body'''
    pass
#end

def p_name(p):
    '''name : simple_name
    | indexed_comp
    | selected_comp
    | attribute
    | operator_symbol'''
    pass
def p_mark(p):
    '''mark : simple_name
    | mark TICK attribute_id
    | mark DOT simple_name'''
    pass
def p_simple_name(p):
    '''simple_name : IDENTIFIER'''
    pass
def p_compound_name(p):
    '''compound_name : simple_name
    | compound_name DOT simple_name'''
    pass
def p_c_name_list(p):
    '''c_name_list : compound_name
     | c_name_list COMMA compound_name'''
    pass
def p_used_char(p):
    '''used_char : CHARACTER'''
    pass
def p_operator_symbol(p):
    '''operator_symbol : STRING'''
    pass
def p_indexed_comp(p):
    '''indexed_comp : name LPAREN value_s RPAREN'''
    pass
def p_value_s(p):
    '''value_s : value
    | value_s COMMA value'''
    pass
def p_value(p):
    '''value : expression
    | comp_assoc
    | discrete_with_range
    | error'''
    pass
def p_selected_comp(p):
    '''selected_comp : name DOT simple_name
    | name DOT used_char
    | name DOT operator_symbol
    | name DOT ALL'''
    pass
def p_attribute(p):
    '''attribute : name TICK attribute_id'''
    pass
def p_attribute_id(p):
    '''attribute_id : IDENTIFIER
    | DIGITS
    | DELTA
    | ACCESS'''
    pass
def p_literal(p):
    '''literal : NUMBER
    | used_char
    | NULL'''
    pass
def p_aggregate(p):
    '''aggregate : LPAREN comp_assoc RPAREN
    | LPAREN value_s_2 RPAREN
    | LPAREN expression WITH value_s RPAREN
    | LPAREN expression WITH NULL RECORD RPAREN
    | LPAREN NULL RECORD RPAREN'''
    pass
def p_value_s_2(p):
    '''value_s_2 : value COMMA value
    | value_s_2 COMMA value'''
    pass
def p_comp_assoc(p):
    '''comp_assoc : choice_s ARROW expression'''
    pass
def p_expression(p):
    '''expression : relation
    | expression logical relation
    | expression short_circuit relation'''
    pass
def p_logical(p):
    '''logical : AND
    | OR
    | XOR'''
    pass
def p_short_circuit(p):
    '''short_circuit : AND THEN
    | OR ELSE'''
    pass
def p_relation(p):
    '''relation : simple_expression
    | simple_expression relational simple_expression
    | simple_expression membership range
    | simple_expression membership name'''
    pass
def p_relational(p):
    '''relational : EQ
    | NE
    | LT
    | LE
    | GT
    | GE'''
    pass
def p_membership(p):
    '''membership : IN
    | NOT IN'''
    pass
def p_simple_expression(p):
    '''simple_expression : unary term
    | term
    | simple_expression adding term'''
    pass
def p_unary(p):
    '''unary   : PLUS
    | MINUS'''
    pass
def p_adding(p):
    '''adding  : PLUS
    | MINUS
    | AMPERSAND'''
    pass
def p_term(p):
    '''term    : factor
    | term multiplying factor'''
    pass
def p_multiplying(p):
    '''multiplying : TIMES
    | DIVIDE
    | MOD
    | REM'''
    pass
def p_factor(p):
    '''factor : primary
    | NOT primary
    | ABS primary
    | primary POW primary'''
    pass
def p_primary(p):
    '''primary : literal
    | name
    | allocator
    | qualified
    | parenthesized_primary'''
    pass
def p_parenthesized_primary(p):
    '''parenthesized_primary : aggregate
    | LPAREN expression RPAREN'''
    pass
def p_qualified(p):
    '''qualified : name TICK parenthesized_primary'''
    pass
def p_allocator(p):
    '''allocator : NEW name
    | NEW qualified'''
    pass
def p_statement_s(p):
    '''statement_s : statement
    | statement_s statement'''
    pass

#modified
def p_statement(p):
    '''statement : unlabeled'''
    pass
def p_unlabeled(p):
    '''unlabeled : simple_stmt
    | compound_stmt'''
    pass
def p_simple_stmt(p):
    '''simple_stmt : NULL_stmt
    | assign_stmt
    | exit_stmt
    | return_stmt
    | goto_stmt
    | procedure_call
    | error SEMICOLON'''
    pass
def p_compound_stmt(p):
    '''compound_stmt : if_stmt
    | case_stmt
    | loop_stmt
    | block'''
    pass
#end

#label

def p_NULL_stmt(p):
    '''NULL_stmt : NULL SEMICOLON'''
    pass
def p_assign_stmt(p):
    '''assign_stmt : name IS_ASSIGNED expression SEMICOLON'''
    pass
def p_if_stmt(p):
    '''if_stmt : IF cond_clause_s else_opt END IF SEMICOLON'''
    pass
def p_cond_clause_s(p):
    '''cond_clause_s : cond_clause
    | cond_clause_s ELSIF cond_clause'''
    pass
def p_cond_clause(p):
    '''cond_clause : cond_part statement_s'''
    pass
def p_cond_part(p):
    '''cond_part : condition THEN'''
    pass
def p_condition(p):
    '''condition : expression'''
    pass
def p_else_opt(p):
    '''else_opt :
    | ELSE statement_s'''
    pass

#modified
def p_case_stmt(p):
    '''case_stmt : CASE expression IS alternative_s END CASE SEMICOLON'''
    pass
#end

def p_alternative_s(p):
    '''alternative_s :
    | alternative_s alternative'''
    pass
def p_alternative(p):
    '''alternative : WHEN choice_s ARROW statement_s'''
    pass
def p_loop_stmt(p):
    '''loop_stmt : label_opt iteration basic_loop id_opt SEMICOLON'''
    pass
def p_label_opt(p):
    '''label_opt :
    | IDENTIFIER COLON'''
    pass
def p_iteration(p):
    '''iteration :
    | WHILE condition
    | iter_part reverse_opt discrete_range'''
    pass
def p_iter_part(p):
    '''iter_part : FOR IDENTIFIER IN'''
    pass
def p_reverse_opt(p):
    '''reverse_opt :
    | REVERSE'''
    pass
def p_basic_loop(p):
    '''basic_loop : LOOP statement_s END LOOP'''
    pass
def p_id_opt(p):
    '''id_opt :
    | designator'''
    pass

#modified
def p_block(p):
    '''block : label_opt block_body END id_opt SEMICOLON'''
    pass
#end

#block_decl

def p_block_body(p):
    '''block_body : BEGIN handled_stmt_s'''
    pass

#modified
def p_handled_stmt_s(p):
    '''handled_stmt_s : statement_s'''
    pass
#end

#exception_handle

def p_exit_stmt(p):
    '''exit_stmt : EXIT name_opt when_opt SEMICOLON'''
    pass
def p_name_opt(p):
    '''name_opt :
    | name'''
    pass
def p_when_opt(p):
    '''when_opt :
    | WHEN condition'''
    pass
def p_return_stmt(p):
    '''return_stmt : RETURN SEMICOLON
    | RETURN expression SEMICOLON'''
    pass
def p_goto_stmt(p):
    '''goto_stmt : GOTO name SEMICOLON'''
    pass

#modified
def p_subprog_decl(p):
    '''subprog_decl : subprog_spec SEMICOLON
    | generic_subp_inst SEMICOLON'''
    pass
#end

def p_subprog_spec(p):
    '''subprog_spec : PROCEDURE compound_name formal_part_opt
    | FUNCTION designator formal_part_opt RETURN name
    | FUNCTION designator '''
    pass
def p_designator(p):
    '''designator : compound_name
    | STRING'''
    pass
def p_formal_part_opt(p):
    '''formal_part_opt : 
    | formal_part'''
    pass
def p_formal_part(p):
    '''formal_part : LPAREN param_s RPAREN'''
    pass
def p_param_s(p):
    '''param_s : param
    | param_s SEMICOLON param'''
    pass
def p_param(p):
    '''param : def_id_s COLON mode mark init_opt
    | error'''
    pass
def p_mode(p):
    '''mode :
    | IN
    | OUT
    | IN OUT
    | ACCESS'''
    pass
def p_subprog_spec_is_push(p):
    '''subprog_spec_is_push : subprog_spec IS'''
    pass
def p_subprog_body(p):
    '''subprog_body : subprog_spec_is_push decl_part block_body END id_opt SEMICOLON'''
    pass
def p_procedure_call(p):
    '''procedure_call : name SEMICOLON'''
    pass

#pkg_decl
#private_type

def p_limited_opt(p):
    '''limited_opt :
    | LIMITED'''
    pass
def p_use_clause(p):
    '''use_clause : USE name_s SEMICOLON
    | USE TYPE name_s SEMICOLON'''
    pass
def p_name_s(p):
    '''name_s : name
    | name_s COMMA name'''
    pass

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
    pass
def p_comp_unit(p):
    '''comp_unit : context_spec private_opt unit
    | private_opt unit'''
    pass
def p_private_opt(p):
    '''private_opt :
    | PRIVATE'''
    pass
def p_context_spec(p):
    '''context_spec : with_clause use_clause_opt
    | context_spec with_clause use_clause_opt'''
    pass
#end

def p_with_clause(p):
    '''with_clause : WITH c_name_list SEMICOLON'''
    pass
def p_use_clause_opt(p):
    '''use_clause_opt :
    | use_clause_opt use_clause'''
    pass

#modified
def p_unit(p):
    '''unit : subprog_decl
    | subprog_body
    | generic_decl'''
    pass
#end

#body_stub
#exception
#raise_stmt
#reque_stmt

#modified
def p_generic_decl(p):
    '''generic_decl : generic_formal_part subprog_spec SEMICOLON'''
    pass
#end

def p_generic_formal_part(p):
    '''generic_formal_part : GENERIC
    | generic_formal_part generic_formal'''
    pass
def p_generic_formal(p):
    '''generic_formal : param SEMICOLON
    | use_clause'''
    pass

#generic_related

def p_generic_subp_inst(p):
    '''generic_subp_inst : subprog_spec IS generic_inst'''
    pass

#generic_pkg

def p_generic_inst(p):
    '''generic_inst : NEW name'''
    pass

#rep_spec
#code_stmt

def p_empty(t):
    'empty : '
    pass

def p_error(p):
    if p:
        print("Syntax error near '%s' at line %d" % (p.value, p.lineno))
    else:
        print("Syntax error at EOF")
    

yacc = yacc.yacc()
cu = '''
function Levenshtein(Left, Right : String) return Natural is
    D : array(0 .. Left'Last, 0 .. Right'Last) of Natural;
  begin
    for I in D'range(1) loop D(I, 0) := I;end loop;
    for J in D'range(2) loop D(0, J) := J;end loop;
 
    for I in Left'range loop
      for J in Right'range loop
        D(I, J) := Natural'Min(D(I - 1, J), D(I, J - 1)) + 1;
        D(I, J) := Natural'Min(D(I, J), D(I - 1, J - 1) + Boolean'Pos(Left(I) /= Right(J)));
      end loop;
    end loop; 

    return D(D'Last(1), D'Last(2));
  end Levenshtein;
'''
print yacc.parse(cu)
