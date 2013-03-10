'''
Abstract Syntax Tree (AST) objects.

This file defines classes for different kinds of nodes of an Abstract
Syntax Tree.  During parsing, you will create these nodes and connect
them together.  In general, you will have a different AST node for
each kind of grammar rule.  A few sample AST nodes can be found at the
top of this file.  You will need to add more on your own.
'''

# DO NOT MODIFY
class AST(object):
    '''
    Base class for all of the AST nodes.  Each node is expected to
    define the _fields attribute which lists the names of stored
    attributes.   The __init__() method below takes positional
    arguments and assigns them to the appropriate fields.  Any
    additional arguments specified as keywords are also assigned. 
    '''
    _fields = []
    def __init__(self,*args,**kwargs):
        assert len(args) == len(self._fields)
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
        # Assign additional keyword arguments if supplied
        for name,value in kwargs.items():
            setattr(self,name,value)

    def __repr__(self):
        excluded = {"lineno"}
        return "{}[{}]".format(self.__class__.__name__, 
                              {key: value 
                               for key, value in vars(self).items() 
                               if not key.startswith("_") and not key in excluded})

# ----------------------------------------------------------------------
# Specific AST nodes.
#
# For each of these nodes, you need to add the appropriate _fields = []
# specification that indicates what fields are to be stored.  Just as
# an example, for a binary operator, you might store the operator, the
# left expression, and the right expression like this:
#
#    class Binop(AST):
#        _fields = ['op','leftexpr','rightexpr']
#
# Suggestion:  The nodes are listed here in a suggested order of work
# on your parse.  You should start simple and incrementally work your
# way up to building the complete grammar
# ----------------------------------------------------------------------

class Goal_symbol(AST):
    _fields = ['compilation'] 
    
class Object_decl(AST):
    _fields = ['def_id_s','object_qualifier_opt','object_subtype_def','init_opt']
    
class Def_id_s(AST):
    _fields = ['def_id_s']
    
    def append(self,stmt):
        self.def_id_s.append(stmt)

    def __len__(self):
        return len(self.def_id_s)
    
class Def_id(AST):
    _fields = ['identifier']
    
class Object_Aliased(AST):
    _fields = ['constant']
    
class Number_decl(AST):
    _fields = ['def_id_s','constant','expression']
    
class Type_decl(AST):
    _fields = ['identifier','discrim_part_opt','type_completion']
    
class Subtype_decl(AST):
    _fields = ['identifier','subtype_ind']
    
class Subtype_ind(AST):
    _fields = ['name','constraint']
    
class Doubledot_range(AST):
    _fields = ['l_simple_expression','r_simple_expression']
    
class Name_tick(AST):
    _fields = ['name','expression']
    
class Enum(AST):
    _fields = ['enum_id']
    
    def append(self,stmt):
        self.enum_id.append(stmt)

    def __len__(self):
        return len(self.enum_id)
    
class Float_type(AST):
    _fields = ['expression','range_spec']
    
class Fixed_type(AST):
    _fields = ['l_expression','r_expression','range_spec']
    
class Unconstr_array(AST):
    _fields = ['index_s','component_subtype_def']
    
class Constr_array(AST):
    _fields = ['index_constraint','component_subtype_def']
    
class Component_subtype(AST):
    _fields = ['aliased','subtype_ind']
    
class Array_aliased(AST):
    _fields = ['aliased']
    
class Index_s(AST):
    _fields = ['index_s']
    
    def append(self,stmt):
        self.index_s.append(stmt)

    def __len__(self):
        return len(self.index_s)
    
class Iter_discrete_range_s(AST):
    _fields = ['discrete_range']
    
    def append(self,stmt):
        self.discrete_range.append(stmt)

    def __len__(self):
        return len(self.discrete_range)
    
class Range_constr(AST):
    _fields = ['name','range_constr']
    
class Record_type(AST):
    _fields = ['tagged','limited','record_def']
    
class Record_def(AST):
    _fields = ['comp_list']
    
class Comp_list_1(AST):
    _fields = ['comp_decl_s','variant_part']
    
class Comp_decl_s(AST):
    _fields = ['comp_decl_s']
    
    def append(self,stmt):
        self.comp_decl_s.append(stmt)

    def __len__(self):
        return len(self.comp_decl_s)
    
class Comp_decl(AST):
    _fields = ['def_id_s','component_subtype_def','init']
    
class Disrim_spec_s(AST):
    _fields = ['discrim_spec_s']
    
    def append(self,stmt):
        self.discrim_spec_s.append(stmt)

    def __len__(self):
        return len(self.discrim_spec_s)
    
class Discrim_spec(AST):
    _fields = ['def_id_s','access','mark','init']
    
class Variant_part(AST):
    _fields = ['simple_name','variant_s']
    
class Variant_s(AST):
    _fields = ['variant_s']
    
    def append(self,stmt):
        self.variant_s.append(stmt)

    def __len__(self):
        return len(self.variant_s)
    
class Variant(AST):
    _fields = ['choice_s','comp_list']
    
class Choice_s(AST):
    _fields = ['choice_s']
    
    def append(self,stmt):
        self.choice_s.append(stmt)

    def __len__(self):
        return len(self.choice_s)

class Access_1(AST):
    _fields = ['cons','subtype_ind']
    
class Access_2(AST):
    _fields = ['prot_opt','formal_part']
    
class Access_3(AST):
    _fields = ['prot_opt','formal_part','return']
    
class Decl_or_body__s1(AST):
    _fields = ['decl_item_or_body_s1']
    
    def append(self,stmt):
        self.decl_item_or_body_s1.append(stmt)

    def __len__(self):
        return len(self.decl_item_or_body_s1)
    
class Mark(AST):
    _fields = ['mark','attribute']
    
class Compound_name(AST):
    _fields = ['compound_name','simple_name']
    
class C_name_list(AST):
    _fields = ['c_name_list']
    
    def append(self,stmt):
        self.c_name_list.append(stmt)

    def __len__(self):
        return len(self.c_name_list)
    
class Indexed_comp(AST):
    _fields = ['name','value_s']
    
class Value_s(AST):
    _fields = ['value_s']
    
    def append(self,stmt):
        self.value_s.append(stmt)

    def __len__(self):
        return len(self.value_s)
    
class Selected_comp(AST):
    _fields = ['name','simple_name']
    
class Attribute(AST):
    _fields = ['name','attribute_id']
    
class Aggregate_1(AST):
    _fields = ['comp']
    
class Aggregate_2(AST):
    _fields = ['expression','value_s']
    
class Aggregate_3(AST):
    _fields = ['expression']
    
class Value_s_2(AST):
    _fields = ['value_s_2']
    
    def append(self,stmt):
        self.value_s_2.append(stmt)

    def __len__(self):
        return len(self.value_s_2)
    
class Comp_assoc(AST):
    _fields = ['choice_s','expression']
    
class Logical_op(AST):
    _fields = ['logical','expression','relation']
    
class Short_circuit(AST):
    _fields = ['short_circuit','expression','relation']
    
class Membership(AST):
    _fields = ['membership','simple_expression','range']
    
class Relational(AST):
    _fields = ['membership','simple_expression','name']
    
class Unary_op(AST):
    _fields = ['unary','term']
    
class Adding(AST):
    _fields = ['adding','simple_expression','term']
    
class Multiplying(AST):
    _fields = ['multiplying','term','factor']
    
class Not(AST):
    _fields = ['primary']
    
class Abs(AST):
    _fields = ['primary']
    
class Pow(AST):
    _fields = ['l_primary','r_primary']
    
class Qualified(AST):
    _fields = ['name','parenthesized_primary']
    
class New(AST):
    _fields = ['name']
    
class Statement_s(AST):
    _fields = ['statement_s']
    
    def append(self,stmt):
        self.statement_s.append(stmt)

    def __len__(self):
        return len(self.statement_s)
    
class Assign_Stmt(AST):
    _fields = ['name','expression']
    
class If_stmt(AST):
    _fields = ['cond_clause_s','else']
    
class Cond_clause(AST):
    _fields = ['cond_part','statement_s']
    
class Case_stmt(AST):
    _fields = ['expression','alternative_s']
    
class Alternative(AST):
    _fields = ['choice_s','statement_s']
    
class Loop_stmt(AST):
    _fields = ['label','iteration','basic_loop','id']
    
class For_loop(AST):
    _fields = ['identifier','reverse','discrete_range']
    
class Block(AST):
    _fields = ['label','block_body','id']
    
class Exit_stmt(AST):
    _fields = ['name','when']
    
class Return_stmt(AST):
    _fields = ['expression']
    
class Goto_stmt(AST):
    _fields = ['name']
    
class Procedure(AST):
    _fields = ['compound_name','formal_part']
    
class Function(AST):
    _fields = ['designator','formal_part','name']
    
class Param_s(AST):
    _fields = ['param_s']
    
    def append(self,stmt):
        self.param_s.append(stmt)

    def __len__(self):
        return len(self.param_s)
    
class Param(AST):
    _fields = ['def_id_s','mode','mark','init']
    
class Is_push(AST):
    _fields = ['subprog_spec']
    
class Subprog_body(AST):
    _fields = ['subprog_spec','decl_part','block_body','id']
    
class Procedure_call(AST):
    _fields = ['name']
    
class Limited(AST):
    _fields = ['limited']
    
class Use(AST):
    _fields = ['type','name_s']
    
class Name_s(AST):
    _fields = ['name_s']
    
    def append(self,stmt):
        self.name_s.append(stmt)

    def __len__(self):
        return len(self.name_s)
    
class Comp_unit(AST):
    _fields = ['context_spec','private','unit']
    
class Private(AST):
    _fields = ['private']
    
class Context_spec(AST):
    _fields = ['context_spec']
    
    def append(self,stmt):
        self.context_spec.append(stmt)

    def __len__(self):
        return len(self.context_spec)
    
class With_clause(AST):
    _fields = ['c_name_list']
    
class Generic_decl(AST):
    _fields = ['generic_formal','subprog_spec']
    
class Generic(AST):
    _fields = ['generic']
    
class Gen_subp_inst(AST):
    _fields = ['subprog_spec','generic_inst']


# ----------------------------------------------------------------------
#                  DO NOT MODIFY ANYTHING BELOW HERE
# ----------------------------------------------------------------------

# The following classes for visiting and rewriting the AST are taken
# from Python's ast module.   

# DO NOT MODIFY
class NodeVisitor(object):
    '''
    Class for visiting nodes of the parse tree.  This is modeled after
    a similar class in the standard library ast.NodeVisitor.  For each
    node, the visit(node) method calls a method visit_NodeName(node)
    which should be implemented in subclasses.  The generic_visit() method
    is called for all nodes where there is no matching visit_NodeName() method.

    Here is a example of a visitor that examines binary operators:

        class VisitOps(NodeVisitor):
            visit_Binop(self,node):
                print("Binary operator", node.op)
                self.visit(node.left)
                self.visit(node.right)
            visit_Unaryop(self,node):
                print("Unary operator", node.op)
                self.visit(node.expr)

        tree = parse(txt)
        VisitOps().visit(tree)
    '''
    def visit(self,node):
        '''
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        '''
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None
    
    def generic_visit(self,node):
        '''
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        '''
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)

# DO NOT MODIFY
def flatten(top):
    '''
    Flatten the entire parse tree into a list for the purposes of
    debugging and testing.  This returns a list of tuples of the
    form (depth, node) where depth is an integer representing the
    parse tree depth and node is the associated AST node.
    '''
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = []
        def generic_visit(self,node):
            self.nodes.append((self.depth,node))
            self.depth += 1
            NodeVisitor.generic_visit(self,node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes
