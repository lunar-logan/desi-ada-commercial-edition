# exprcheck.py
'''
Project 3 : Program Checking
============================
In this project you need to perform semantic checks on your program.
There are a few different aspects of doing this.

First, you will need to define a symbol table that keeps track of
previously declared identifiers.  The symbol table will be consulted
whenever the compiler needs to lookup information about variable and
constant declarations.

Next, you will need to define objects that represent the different
builtin datatypes and record information about their capabilities.
See the file exprtype.py.

Finally, you'll need to write code that walks the AST and enforces
a set of semantic rules.  Here is a complete list of everything you'll
need to check:

1.  Names and symbols:

    All identifiers must be defined before they are used.  This includes variables,
    constants, and typenames.  For example, this kind of code generates an error:

       a = 3;              // Error. 'a' not defined.
       var a int;

    Note: typenames such as "int", "float", and "string" are built-in names that
    should be defined at the start of the program.

2.  Types of literals

    All literal symbols must be assigned a type of "int", "float", or "string".  
    For example:

       const a = 42;         // Type "int"
       const b = 4.2;        // Type "float"
       const c = "forty";    // Type "string"
       const d = true;

    To do this assignment, check the Python type of the literal value and attach
    a type name as appropriate.

3.  Binary operator type checking

    Binary operators only operate on operands of the same type and produce a
    result of the same type.   Otherwise, you get a type error.  For example:

        var a int = 2;
        var b float = 3.14;

        var c int = a + 3;    // OK
        var d int = a + b;    // Error.  int + float
        var e int = b + 4.5;  // Error.  int = float
        var f bool = true;

4.  Unary operator type checking.

    Unary operators return a result that's the same type as the operand.

5.  Supported operators

    Here are the operators supported by each type:

    int:      binary { +, -, *, /, ==, !=, >, >=, <, <= }, unary { +, - }
    float:    binary { +, -, *, /, ==, !=, >, >=, <, <= }, unary { +, - }
    string:   binary { +, ==, != }, unary { }
    bool:     binary { ==, != }, unary { ! }

    Attempts to use unsupported operators should result in an error. 
    For example:

        var string a = "Hello" + "World";     // OK
        var string b = "Hello" * "World";     // Error (unsupported op *)

6.  Assignment.

    The left and right hand sides of an assignment operation must be
    declared as the same type.

    Values can only be assigned to variable declarations, not
    to constants.

For walking the AST, use the NodeVisitor class defined in exprast.py.
A shell of the code is provided below.
'''

from errors import error
from ast import *
from loo import IntType, FloatType, StringType, BoolType, ExprType
from pprint import pprint

counter = 0
class SymbolTable(dict):
    '''
    Class representing a symbol table.  It should provide functionality
    for adding and looking up nodes associated with identifiers.
    '''
    def __init__(self, decl=None):
        dict.__init__(self)
        self.decl = decl
    def add(self, name, value):
        self[name] = value
    def lookup(self, name):
        return self.get(name, None)
    def return_type(self):
        if self.decl:
            if self.decl.returntype != None:
                return self.decl.returntype.check_type
        return None

class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.root.update({
            "integer": IntType,
            "float": FloatType,
            "string": StringType,
            "bool": BoolType
        })

    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))

    def pop(self):
        self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def scope_level(self):
        return len(self.stack)

    def add_local(self, name, value):
        self.peek().add(name, value)

    def add_root(self, name, value):
        self.root.add(name, value)

    def lookup(self, name):
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        return None

    def look(self,name):
        hit = self.peek().lookup(name)
        if hit is not None :
            return hit
        return None

    def prnt(self):
        for indent, scope in enumerate(reversed(self.stack)):
            print("Scope for {}".format("ROOT" if scope.decl is None else scope.decl))
            pprint(scope, indent=indent*4, width=20)

class CheckProgramVisitor(NodeVisitor):
    '''
    Program checking class.   This class uses the visitor pattern as described
    in exprast.py.   You need to define methods of the form visit_NodeName()
    for each kind of AST node that you want to process.

    Note: You will need to adjust the names of the AST nodes if you
    picked different names.
    '''
    def __init__(self):
        self.environment = Environment()
        self.typemap = {
            int: IntType, 
            float: FloatType, 
            str: StringType,
            bool: BoolType
        }

    def check_type_unary(self, node, op, val):
        if hasattr(val, "check_type"):
            if op not in val.check_type.unary_ops:
                error(node.lineno, "Unary operator {} not supported".format(op))
            return val.check_type

    def check_type_binary(self, node, op, left, right):
        if hasattr(left, "check_type") and hasattr(right, "check_type"):
            if left.check_type != right.check_type:
                error(node.lineno, "Binary operator {} does not have matching LHS/RHS types".format(op))
                return left.check_type
            errside = None
            if op not in left.check_type.binary_ops:
                errside = "LHS"
            if op not in right.check_type.binary_ops:
                errside = "RHS"
            if errside is not None:
                error(node.lineno, "Binary operator {} not supported on {} of expression".format(op, errside))
            # XXX: right now we just propagate the left type, but we should probably handle error conditions
            return left.check_type

    def check_type_rel(self, node, op, left, right):
        if hasattr(left, "check_type") and hasattr(right, "check_type"):
            if left.check_type != right.check_type:
                error(node.lineno, "Relational operator {} does not have matching LHS/RHS types".format(op))
                return left.check_type
            errside = None
            if op not in left.check_type.rel_ops:
                errside = "LHS"
            if op not in right.check_type.rel_ops:
                errside = "RHS"
            if errside is not None:
                error(node.lineno, "Relational operator {} not supported on {} of expression".format(op, errside))
            # XXX: right now we just propagate the left type, but we should probably handle error conditions
            return BoolType

    def inside_function(self):
        return self.environment.scope_level() > 1

    def visit_Program(self,node):
        print 'Program'
        print self.environment.scope_level()
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # 1. Visit all of the statements
        for statement in node.statements.statements:
            self.visit(statement)
            # 2. Record the associated symbol table
            if isinstance(statement, AssignmentStatement):
                self.environment.add_local(statement.location.name, statement.expr)

    def visit_Unaryop(self,node):
        print 'Unaryop'
        print self.environment.scope_level()
        self.visit(node.expr)
        # 1. Make sure that the operation is supported by the type
        check_type = self.check_type_unary(node, node.op, node.expr)
        # 2. Set the result type to the same as the operand
        node.check_type = check_type

    def visit_Binop(self,node):
        print 'Binaryop'
#        print node.left
#        print node.right
        print self.environment.scope_level()
        # 1. Make sure left and right operands have the same type
        # 2. Make sure the operation is supported
        # AM note: both are done in check_type_binary
        print 'Visiting left'
        self.visit(node.left)
        print 'Visiting right'
        self.visit(node.right)
        check_type = self.check_type_binary(node, node.op, node.left, node.right)
        # 3. Assign the result type
        node.check_type = check_type

    def visit_Relop(self,node):
        print 'Relop'
        print self.environment.scope_level()
        # 1. Make sure left and right operands have the same type
        # 2. Make sure the operation is supported
        # AM note: both are done in check_type_binary
        self.visit(node.left)
        self.visit(node.right)
        check_type = self.check_type_rel(node, node.op, node.left, node.right)
        # 3. Assign the result type
        node.check_type = check_type
        print check_type

    def visit_Unconstr_array(self,node):
        print 'Unconstrained Array'
        for index in node.index_s.index_s :
            self.visit(index)
        self.visit(node.subtype_ind)
        node.check_type = node.subtype_ind.check_type

    def visit_Constr_array(self,node):
        print 'Constrained Array'
        for drange in node.index_constraint :
            if drange[0] != None :
                self.visit(drange[0])
            self.visit(drange[1])
            if drange[0]!=None :
                if hasattr(drange[0],'check_type') and hasattr(drange[1],'check_type'):
                    if drange[0].check_type != drange[1].check_type :
                        error(node.lineno, "Type Mismatch".format(node.location.name))
        self.visit(node.subtype_ind)
        node.check_type = node.subtype_ind.check_type

    def visit_Record(self,node):
        if node.record_def[1] != None :
            for comp in node.record_def[1].comp_decls:
                self.visit(comp)
        if node.record_def[0] != None :
            self.visit(node.record_def[0])

    def visit_AssignmentStatement(self,node):
        print 'Assignment'
        print node.location.name
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot assign variable '{}' outside function body".format(node.location.name))
            return
        # 1. Make sure the location of the assignment is defined
        sym = self.environment.lookup(node.location.name)
        if not sym:
            error(node.lineno, "name '{}' not defined".format(node.location.name))
        # 2. Check that assignment is allowed
        self.visit(node.expr)
        print 'Visited expression'
        if isinstance(sym, VarDeclaration):
            # empty var declaration, so check against the declared type name
            if hasattr(sym, "check_type") and hasattr(node.expr, "check_type"):
                declared_type = sym.check_type
                value_type = node.expr.check_type
                if declared_type != value_type:
                    error(node.lineno, "Cannot assign {} to {}".format(value_type, declared_type))
                    return
        if isinstance(sym, ConstDeclaration):
            error(node.lineno, "Cannot assign to constant {}".format(sym.name))
            return
        # 3. Check that the types match
        if hasattr(node.location, "check_type") and hasattr(node.expr, "check_type"):
            declared_type = node.location.check_type
            value_type = node.expr.check_type
            if declared_type != value_type:
                error(node.lineno, "Cannot assign {} to {}".format(value_type, declared_type))

    def visit_IfStatement(self,node):
        print 'If'
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot use if statement outside function body")
            return
        self.visit(node.expr)
        if node.expr.check_type != BoolType:
            error(node.lineno, "Expression in if statement must evaluate to bool")
        self.visit(node.truebranch)
        if node.falsebranch is not None:
            self.visit(node.falsebranch)

    def visit_CaseStatement(self,node):
        print 'Case'
        self.visit(node.condition)
        for al in self.alternatives.alternatives :
            self.visit(al)
            if hasattr(node.condition,'check_type') and hasattr(al,'check_type') :
                if node.condition.check_type  != al.check_type :
                    error(node.lineno, "Expression in case statement must evaluate to bool")
                    return
            else :
                    error(node.lineno, "No type assigned to node")

    def  visit_Alternative(self,node) :
        print 'Alternative'
        self.visit(node.choices.choices[0])
        if hasattr(node.choices.choices[0],'check_type') :
            temp=node.choices.choices[0].check_type
        else :
            error(node.lineno, "Type error") 
        for ch in range(1,(node.choices.choices.len()-1)) :
            self.visit(node.choices.choices[ch])
            if hasattr(node.choices.choices[ch],'check_type')==False or node.choices.choices[ch].check_type!=temp :
                error(node.lineno, "Type error")
        node.check_type = temp
        self.visit(node.statements)
                

    def visit_WhileStatement(self,node):
        global counter
        print 'While'
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot use while statement outside function body")
            return
        if node.label ==  None :
            while self.environment.lookup(counter) is not None :
                counter+=1
            node.label = counter
            counter+=1
        else:
            if self.environment.lookup(node.label) is not None:
                error(node.lineno, "Attempted to redefine label, not allowed".format(node.label))
                return
            if node.id!=None and node.label != node.id :
                error(node.lineno, "Label does not match".format(node.label))
        self.environment.push(node)
        self.environment.add_local(node.label, node)
        self.visit(node.expr)
        if node.expr != None :
            if node.expr.check_type != BoolType:
                error(node.lineno, "Expression in while statement must evaluate to bool")
        self.visit(node.truebranch)
        self.environment.pop()

    def visit_For_loop(self,node):
        print 'For_loop'
        node.scope_level = self.environment.scope_level()
#        if node.scope_level > 1:
#            error(node.lineno, "Nested functions not implemented")
#            return
        self.environment.push(node)
        self.visit(node.name)
        print 'Visited name'
        self.environment.add_root(node.name.name, node)
        self.visit(node.discrete_range)
        if hasattr(node.name, "check_type") and hasattr(node.discrete_range, "check_type"):
            if node.name.check_type == node.discrete_range.check_type :
                node.check_type = BoolType
            else :
                error(node.lineno, "Expression in for statement must evaluate to bool")
        self.environment.pop()

    def visit_Doubledot_range(self,node):
        node.scope_level = self.environment.scope_level()
        self.visit(node.left)
        self.visit(node.right)
        if hasattr(node.left, "check_type") and hasattr(node.right, "check_type"):
            if node.left.check_type == node.right.check_type :
                node.check_type = node.left.check_type

    def visit_Name_tick(self,node):
        if node.expression != None :
            self.visit(node.expression)
        node.check_type = self.environment.lookup(node.name)

    def visit_ConstDeclaration(self,node):
        print 'Constant'
        print self.environment.scope_level()
        node.scope_level = self.environment.scope_level()
        # 1. Check that the constant name is not already defined
        if self.environment.lookup(node.name) is not None:
            error(node.lineno, "Attempted to redefine const '{}', not allowed".format(node.name))
        # 2. Add an entry to the symbol table
        self.environment.add_local(node.name, node)
        self.visit(node.expr)
        node.check_type = node.expr.check_type

    def visit_Block(self,node):
        global counter
        print 'Block'
        if node.label ==  None :
            while self.environment.lookup(counter) is not None :
                counter+=1
            node.label = counter
            counter+=1
        else:
            if self.environment.lookup(node.label) is not None:
                error(node.lineno, "Attempted to redefine label, not allowed".format(node.label))
                return
            if node.id!=None and node.label != node.id :
                error(node.lineno, "Label does not match".format(node.label))
        self.environment.push(node)
        self.environment.add_local(node.label, node)
        for declarations in node.decl:
            self.visit(declarations)
        self.visit(node.block)
        self.environment.pop()

    def visit_FuncStatement(self, node):
        print 'FuncStatement'
        print self.environment.scope_level()
        # 1. Check that the variable name is not already defined
        node.scope_level = self.environment.scope_level()
#        if node.scope_level > 1:
#            error(node.lineno, "Nested functions not implemented")
#            return
        self.environment.push(node)
        if self.environment.lookup(node.name) is not None:
            error(node.lineno, "Attempted to redefine func '{}', not allowed".format(node.name))
            return
        if node.id!=None and node.name != node.id :
            error(node.lineno, "Label does not match".format(node.name))
        # 2. Add an entry to the symbol table, and also create a nested symbol
        # table for the function statement
        self.environment.add_root(node.name, node)
        # 3. Propagate the returntype as a checktype for the function, for 
        # use in function call checking and return statement checking
        self.visit(node.returntype)
        if hasattr(node.returntype, "check_type"):
            node.check_type = node.returntype.check_type
        self.visit(node.parameters)
        for declarations in node.decl_part:
            self.visit(declarations)
        self.visit(node.statements)
        self.environment.pop()

    def visit_FuncParameterList(self, node):
        print 'FuncParameterList'
        print self.environment.scope_level()
        for parameter in node.parameters:
            self.visit(parameter)
        print 'List done'

    def visit_FuncParameter(self, node):
        print 'FuncParameter'
        print self.environment.scope_level()
        self.environment.add_local(node.name, node)
        node.scope_level = self.environment.scope_level()
        print node.typename
        self.visit(node.typename)
        node.check_type = node.typename.check_type

    def visit_FuncCall(self, node):
        print 'FuncCall'
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot call function from outside function body; see main() for entry point")
            return
        sym = self.environment.lookup(node.name)
        if not sym:
            self.environment.prnt()
            error(node.lineno, "Function name '{}' not found".format(node.name))
            return
        if not isinstance(sym, FuncStatement):
            error(node.lineno, "Tried to call non-function '{}'".format(node.name))
            return

    def visit_FuncCallArguments(self, node):
        print 'FuncCallArguments'
        print self.environment.scope_level()
        for argument in node.arguments:
            self.visit(argument)

    def visit_ReturnStatement(self, node):
        print 'ReturnStatemnt'
        print self.environment.scope_level()
#        if node.expr==None :
#    vim         print 'None abdcjab'
#        if self.environment.peek().return_type()==None :
#            print 'bsdhbajbdsb'
#        if node.expr==None and self.environment.peek().return_type()==None :
#            return       
        self.visit(node.expr)
        if self.environment.peek().return_type() != node.expr.check_type:
            error(node.lineno, "Type of return statement expression does not match declared return type for function")
            return

    def visit_ExitStatement(self,node):
        if node.expr != None :
            self.visit(node.expr)
        if node.expr.check_type != BoolType:
            error(node.lineno, "Expression in if statement must evaluate to bool")

    def visit_PrintStatement(self, node):
        print 'PrintStatement'
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot use print statement outside function body")
            return
        self.visit(node.expr)

    def visit_VarDeclaration(self,node):
        print 'Var'
        print self.environment.scope_level()
        # 1. Check that the variable name is not already defined
        if self.environment.look(node.name) is not None:
            error(node.lineno, "Attempted to redefine var '{}', not allowed".format(node.name))
            return
        # 2. Add an entry to the symbol table
        self.environment.add_local(node.name, node)
        # 3. Check that the type of the expression (if any) is the same
        self.visit(node.typename)
        # propagate check_type from Typename up to Var declaration
        if hasattr(node.typename, "check_type"):
            node.check_type = node.typename.check_type
        # 4. If there is no expression, set an initial value for the value
        self.visit(node.expr)
        if node.expr is None:
            default = node.check_type.default
            node.expr = Literal(default)
            node.expr.check_type = node.check_type
        node.scope_level = self.environment.scope_level()

    def visit_Typename(self,node):
        print 'Typename'
        print self.environment.scope_level()
        # 1. Make sure the typename is valid and that it's actually a type
        print node.name
        sym = self.environment.lookup(node.name)
        print sym
#        if not isinstance(sym, ExprType):
 #           error(node.lineno, "{} is not a valid type".format(node.name))
 #           return
        node.check_type = sym

    def visit_Location(self,node):
        print 'Location'
        print self.environment.scope_level()
        # 1. Make sure the location is a valid variable or constant value
        sym = self.environment.lookup(node.name)
        if not sym:
            error(node.lineno, "name '{}' not found".format(node.name))
        # 2. Assign the type of the location to the node
        node.check_type = sym.check_type

    def visit_LoadLocation(self, node):
        print 'LoadLocation'
        print 'Problem lies here'
#        print node.location.name
        print self.environment.scope_level()
        # 1. Make sure the loaded location is valid
        sym = self.environment.lookup(node.location.name)
        if not sym:
            error(node.lineno, "name '{}' not found".format(node.location.name))
            return
        # 2. Assign the appropriate type
        if isinstance(sym, ExprType):
            error(node.lineno, "cannot use {} outside of variable declarations".format(sym.typename))
            return
        check_type = sym.check_type
        if check_type is None:
            error(node.lineno, "Using unrecognized type {}".format(valtype))
        node.check_type = check_type

    def visit_Literal(self,node):
        print 'Literal'
        print self.environment.scope_level()
        # Attach an appropriate type to the literal
        valtype = type(node.value)
        check_type = self.typemap.get(valtype, None)
        if check_type is None:
            error(node.lineno, "Using unrecognized type {}".format(valtype))
        node.check_type = check_type

    def visit_Subprog_body(self,node):
        print 'Subprog'
        

# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------

def check_program(node):
    '''
    Check the supplied program (in the form of an AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(node)

if __name__ == '__main__':
    import lexer
    import parser
    import sys
    from errors import subscribe_errors
    pars = parser.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = pars.parse(open(sys.argv[1]).read())
        # Check the program
        check_program(program)
        #program.environment.prnt()
            
