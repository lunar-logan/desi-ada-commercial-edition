'''
Created on 04-Mar-2013

@author: prabhat
'''
# exprast.py
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

class Object_decl(AST):
    _fields = ['def_id_s','object_qualifier_opt','object_subtype_def','init_opt']
    
class Def_id_s(AST):
    _fields = ['def_id_s']
    
class Def_id(AST):
    _fields = ['identifier']
    
class Object_Aliased(AST):
    _fields = ['constant']
    
class Number_decl(AST):
    _fields = ['def_id_s','constant','expression']
    
class Type_decl(AST):
    _fields = ['identifier','discrim_part_opt','type_completion']
    
class Subtype_decl(AST):
    _fields = []
    
class Subtype_ind(AST):
    _fields = []
    
class Doubledot_range(AST):
    _fields = []
    
class Name_tick(AST):
    _fields = []
    
class Enum(AST):
    _fields = []
    
class Float_type(AST):
    _fields = []
    
class Fixed_type_1(AST):
    _fields = []
    
class Fixed_type_2(AST):
    _fields = []
    
class Unconstr_array(AST):
    _fields = []
    
class Constr_array(AST):
    _fields = []
    
class Component_subtype(AST):
    _fields = []
    
class Array_aliased(AST):
    _fields = []
    
class Index_s(AST):
    _fields = []
    
class Iter_discrete_range_s(AST):
    _fields = []
    
class Range_constr(AST):
    _fields = []
    
class Record_type(AST):
    _fields = []
    
class Record_def(AST):
    _fields = []
    
class Comp_list_1(AST):
    _fields = []
    
class Comp_decl_s(AST):
    _fields = []
    
class Comp_decl(AST):
    _fields = []
    
class Disrim_spec_s(AST):
    _fields = []
    
class Discrim_spec(AST):
    _fields = []
    
class Variant_part(AST):
    _fields = []
    
class Variant_s(AST):
    _fields = []
    
class Variant(AST):
    _fields = []
    
class Choice_s(AST):
    _fields = []

class Access_1(AST):
    _fields = []
    
class Access_2(AST):
    _fields = []
    
class Access_3(AST):
    _fields = []
    
class Access_4(AST):
    _fields = []
    
class Decl_or_body__s1(AST):
    _fields = []
    
class Mark(AST):
    _fields = []
    
class Compound_name(AST):
    _fields = ['compound_name','simple_name']
    
class C_name_list(AST):
    _fields = []
    
class Indexed_comp(AST):
    _fields = []
    
class Value_s(AST):
    _fields = []
    
class Selected_comp(AST):
    _fields = []
    
class Attribute(AST):
    _fields = []
    
class Aggregate_1(AST):
    _fields = []
    
class Aggregate_2(AST):
    _fields = []
    
class Aggregate_3(AST):
    _fields = []
    
class Value_s_2(AST):
    _fields = []
    
class Comp_assoc(AST):
    _fields = []
    
class Logical_op(AST):
    _fields = []
    
class Short_circuit(AST):
    _fields = []
    
class Membership(AST):
    _fields = []
    
class Relational(AST):
    _fields = []
    
class Unary_op(AST):
    _fields = []
    
class Adding(AST):
    _fields = []
    
class Multiplying(AST):
    _fields = []
    
class Not(AST):
    _fields = []
    
class Abs(AST):
    _fields = []
    
class Pow(AST):
    _fields = []
    
class Qualified(AST):
    _fields = []
    
class New(AST):
    _fields = []
    
class Statement_s(AST):
    _fields = []
    
class Assign_Stmt(AST):
    _fields = []
    
class If_stmt(AST):
    _fields = []
    
class Cond_clause(AST):
    _fields = []
    
class Case_stmt(AST):
    _fields = []
    
class Alternative(AST):
    _fields = []
    
class Loop_stmt(AST):
    _fields = []
    
class For_loop(AST):
    _fields = []
    
class Block(AST):
    _fields = []
    
class Exit_stmt(AST):
    _fields = []
    
class When_cond(AST):
    _fields = []
    
class Return_stmt(AST):
    _fields = []
    
class Goto_stmt(AST):
    _fields = []
    
class Procedure(AST):
    _fields = []
    
class Function(AST):
    _fields = []
    
class Param_s(AST):
    _fields = []
    
class Param(AST):
    _fields = []
    
class Is_push(AST):
    _fields = []
    
class Subprog_body(AST):
    _fields = []
    
class Procedure_call(AST):
    _fields = []
    
class Limited(AST):
    _fields = []
    
class Use(AST):
    _fields = []
    
class Name_s(AST):
    _fields = []
    
class Comp_unit(AST):
    _fields = []
    
class Private(AST):
    _fields = ['private']
    
class Context_spec(AST):
    _fields = []
    
class With_clause(AST):
    _fields = []
    
class Generic_decl(AST):
    _fields = []
    
class Generic(AST):
    _fields = []
    
class Gen_subp_inst(AST):
    _fields = []


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
