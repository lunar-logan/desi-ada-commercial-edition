from errors import error
from ast import *
from loo import IntType, FloatType, StringType, BoolType, CharType, ArrayType, AccessType, EnumType, RecordType, ExprType
from pprint import pprint

counter = 0
class SymbolTable(dict):
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
            "boolean": BoolType,
            "character": CharType,
            "array": ArrayType,
            "enumeration": EnumType,
            "record": RecordType,
            "access": AccessType
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
            return BoolType

    def inside_function(self):
        return self.environment.scope_level() > 1

    def visit_Program(self,node):
        print 'Program'
        print self.environment.scope_level()
        node.environment = self.environment
        node.symtab = self.environment.peek()
        for statement in node.statements.statements:
            self.visit(statement)
            if isinstance(statement, AssignmentStatement):
                self.environment.add_local(statement.location.name, statement.expr)

    def visit_Unaryop(self,node):
        print 'Unaryop'
        print self.environment.scope_level()
        self.visit(node.expr)
        check_type = self.check_type_unary(node, node.op, node.expr)
        node.check_type = check_type

    def visit_Binop(self,node):
        print 'Binaryop'
        print self.environment.scope_level()
        self.visit(node.left)
        self.visit(node.right)
        check_type = self.check_type_binary(node, node.op, node.left, node.right)
        node.check_type = check_type

    def visit_Relop(self,node):
        self.visit(node.left)
        self.visit(node.right)
        check_type = self.check_type_rel(node, node.op, node.left, node.right)
        node.check_type = check_type
        print check_type

    def visit_Integer_type(self, node):
        print 'Integer_type'
        print node.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot define an integer '{}' outside function body".format(node.location.name))
            return
        if node.range_spec is not None:
            self.visit(node.range_spec)
        else:
            self.visit(node.expression)

    def visit_Float_type(self, node):
        node.scope_level = self.environment.scope_level()
        if node.range_spec_opt is not None:
            self.visit(node.range_spec_opt)
        self.visit(node.expression)

    def visit_Access_type_subtype(self, node):
        self.visit(node.subtype_ind)

    def visit_Access_type_subprog(self, node):
        if node.formal_part_opt is not None:
            for parameter in node.formal_part_opt.parameters:
                self.visit(parameter)
        self.visit(node.mark)

    def visit_Fixed_type(self, node):
        node.scope_level = self.environment.scope_level()
        if node.range_spec_opt is not None:
            self.visit(node.range_spec_opt)
        self.visit(node.expression_1)
        self.visit(node.expression_2)

    def visit_Unconstr_array(self,node):
        print 'Unconstrained Array'
        for index in node.index_s.index_s :
            self.visit(index)
        self.visit(node.subtype_ind)
        node.check_type = node.subtype_ind.check_type

    def visit_Constr_array(self,node):
        print 'Constrained Array'
        for drange in node.index_constraint :
            if drange[0] is not None :
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
        sym = self.environment.lookup(node.location.name)
        if not sym:
            error(node.lineno, "name '{}' not defined".format(node.location.name))
        if sym.typename.check_type == EnumType :
            print node.expr.location.name
            print sym.length.enum_id
            if node.expr.location.name not in sym.length.enum_id :
                error(node.lineno,"Not an enum values")
        else :
            if isinstance(node.expr,list):
                for e in node.expr :
                    self.visit(e)
                if len(node.expr) != len((sym.length.record_def)[0].comp_decls) :
                    error(node.lineno, "Length does not match")
                else :
                    for i in range(0,len(node.expr)):
                        if ((sym.length.record_def)[0].comp_decls)[i].typename.check_type != (node.expr)[i].check_type :
                            error(node.lineno, "Type doesn't match")
            else :
                self.visit(node.expr)
        if isinstance(sym, VarDeclaration):
            if hasattr(sym, "check_type") and hasattr(node.expr, "check_type"):
                declared_type = sym.check_type
                value_type = node.expr.check_type
                if declared_type != value_type:
                    error(node.lineno, "Cannot assign {} to {}".format(value_type, declared_type))
                    return
        if hasattr(node.location, "check_type") and hasattr(node.expr, "check_type"):
            declared_type = node.location.check_type
            value_type = node.expr.check_type
            if declared_type != value_type:
                error(node.lineno, "Cannot assign {} to {}".format(value_type, declared_type))

    def visit_ArrayAssignmentStatement(self,node):
        print 'ArrayAssignment'
        print node.location.name
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot assign variable '{}' outside function body".format(node.location.name))
            return
        sym = self.environment.lookup(node.location.name)
        if not sym:
            error(node.lineno, "name '{}' not defined".format(node.location.name))
        else :
            self.visit(node.args)
            self.visit(node.expr)
            print 'Visited expression'
            if isinstance(sym, VarDeclaration):
                if hasattr(sym.length.subtype_ind, "check_type") and hasattr(node.expr, "check_type"):
                    declared_type = sym.length.subtype_ind.check_type
                    value_type = node.expr.check_type
                    if declared_type != value_type:
                        error(node.lineno, "Cannot assign {} to {}".format(value_type, declared_type))
                        return
            if hasattr(sym.length.subtype_ind, "check_type") and hasattr(node.expr, "check_type"):
                declared_type = sym.length.subtype_ind.check_type
                value_type = node.expr.check_type
                if declared_type != value_type:
                    error(node.lineno, "Cannot assign {} to {}".format(value_type, declared_type))
                    return

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
        for al in node.alternatives.alternatives :
            self.visit(al)
            if hasattr(node.condition,'check_type') and hasattr(al,'check_type') :
                if node.condition.check_type  != al.check_type :
                    error(node.lineno, "Type of condition and choice should match")
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
        for ch in range(1,(len(node.choices.choices))) :
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
            else :
                error(node.lineno,"Type does not match")
    def visit_Name_tick(self,node):
        self.visit(node.name)
        if node.expression != None :
            self.visit(node.expression)
        if hasattr(node.name,'check_type'):
            node.check_type = node.name.check_type

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
        node.scope_level = self.environment.scope_level()
#        if node.scope_level > 1:
#            error(node.lineno, "Nested functions not implemented")
#            return
        self.environment.push(node)
        if self.environment.lookup(node.name) is not None:
            error(node.lineno, "Attempted to redefine func '{}', not allowed".format(node.name))
            return
        else :
            if node.id!=None and node.name != node.id :
                error(node.lineno, "Label does not match".format(node.name))
            self.environment.add_root(node.name, node)
            if node.returntype is not None :
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

    def visit_FuncParameter(self, node):
        print 'FuncParameter'
        print self.environment.scope_level()
        self.environment.add_local(node.name, node)
        node.scope_level = self.environment.scope_level()
        print node.typename
        self.visit(node.typename)
        node.check_type = node.typename.check_type

    def visit_ProcCall(self, node):
        print 'ProcCall'
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot call function from outside function body; see main() for entry point")
            return
        self.visit(node.name)

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
        else :
            node.check_type = sym.check_type
        if not isinstance(sym, FuncStatement):
            error(node.lineno, "Tried to call non-function '{}'".format(node.name))
            return
        if len(sym.parameters.parameters) != len(node.arguments.arguments):
            error(node.lineno, "Number of arguments for call to function '{}' do not match function parameter declaration on line {}".format(node.name, sym.lineno))
        if node.arguments is not None:
            self.visit(node.arguments)
        argerrors = False
        for arg, parm in zip(node.arguments.arguments, sym.parameters.parameters):
            if arg.check_type != parm.typename.check_type:
                error(node.lineno, "Argument type '{}' does not match parameter type '{}' in function call to '{}'".format(arg.check_type.typename, parm.check_type.typename, node.name))
                argerrors = True
            if argerrors:
                return
            arg.parm = parm


    def visit_Value_s(self, node):
        print 'FuncCallArguments'
        print self.environment.scope_level()
        for argument in node.arguments:
            if isinstance(argument,tuple):
                if argument[0] is not None :
                    self.visit(argument[0])
                if argument[1] is not None :
                    self.visit(argument[1])
                if hasattr(argument[0],'check_type') :
                    node.check_type = argument[0].check_type
                elif hasattr(argument[1],'check_type') :
                    node.check_type = argument[1].check_type
            else :
                self.visit(argument)
                if hasattr(node,'check_type') :
                    node.check_type = argument.check_type

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
        self.visit(node.name)
        if node.expr != None :
            self.visit(node.expr)
        if node.expr.check_type != BoolType:
            error(node.lineno, "Expression in if statement must evaluate to bool")

    def GotoStatement(self,node):
        self.visit(node.name)

    def visit_PrintStatement(self, node):
        print 'PrintStatement'
        print self.environment.scope_level()
        if not self.inside_function():
            error(node.lineno, "Cannot use print statement outside function body")
            return
        self.visit(node.expr)

    def visit_SubTypeDeclaration(self,node):
        print 'SubType'
        print node.name
        print self.environment.scope_level()
        if self.environment.look(node.name) is not None:
            error(node.lineno, "Attempted to redefine var '{}', not allowed".format(node.name))
        else :
            p=self.environment.lookup(node.typename.name)
            if isinstance(p,TypeDeclaration) :
                node.expr = p.expr
                node.typename = p.typename
                self.visit(node.typename)
                if node.length is not None :
                    self.visit(node.length)
                if node.expr is not None :
                    self.visit(node.expr)
                self.environment.add_local(node.name, node)
                if hasattr(node.typename, "check_type"):
                    node.check_type = node.typename.check_type
            else :
                error(node.lineno, "Type is not valid")
            '''if node.expr is None:
                default = node.check_type.default
                node.expr = Literal(default)
                node.expr.check_type = node.check_type'''
        node.scope_level = self.environment.scope_level()

    def visit_TypeDeclaration(self,node):
        print 'Type'
        print node.name
        print self.environment.scope_level()
        if self.environment.look(node.name) is not None:
            error(node.lineno, "Attempted to redefine var '{}', not allowed".format(node.name))
        else :
            self.visit(node.typename)
            if node.length is not None :
                self.visit(node.length)
            if node.expr is not None :
                self.visit(node.expr)
            self.environment.add_local(node.name, node)
            if hasattr(node.typename, "check_type"):
                node.check_type = node.typename.check_type
            '''if node.expr is None:
                default = node.check_type.default
                node.expr = Literal(default)
                node.expr.check_type = node.check_type'''
        node.scope_level = self.environment.scope_level()

    def visit_VarDeclaration(self,node):
        print 'Var'
        print node.name
        print self.environment.scope_level()
        if self.environment.look(node.name) is not None:
            error(node.lineno, "Attempted to redefine var '{}', not allowed".format(node.name))
        else :
            p=self.environment.lookup(node.typename.name)
            if isinstance(p,TypeDeclaration) :
                node.expr = p.expr
                node.length = p.length
                node.typename = p.typename
            else :
                if node.length is not None :
                    self.visit(node.length)
                if node.expr is not None :
                    self.visit(node.expr)
            self.visit(node.typename)
            self.environment.add_local(node.name, node)
            if hasattr(node.typename, "check_type"):
                node.check_type = node.typename.check_type
            '''if node.expr is None:
                default = node.check_type.default
                node.expr = Literal(default)
                node.expr.check_type = node.check_type'''
        node.scope_level = self.environment.scope_level()

    def visit_Typename(self,node):
        print 'Typename'
        print self.environment.scope_level()
        sym = self.environment.lookup(node.name)
        node.check_type = sym
        if not isinstance(sym, ExprType):
            error(node.lineno, "{} is not a valid type".format(node.name))
            return

    def visit_Location(self,node):
        print 'Location'
        print self.environment.scope_level()
        sym = self.environment.lookup(node.name)
        if not sym:
            error(node.lineno, "name '{}' not found".format(node.name))
        node.check_type = sym.check_type

    def visit_LoadLocation(self, node):
        print 'LoadLocation'
        print self.environment.scope_level()
        sym = self.environment.lookup(node.location.name)
        if not sym:
            error(node.lineno, "name '{}' not found".format(node.location.name))
            return
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
        valtype = type(node.value)
        check_type = self.typemap.get(valtype, None)
        if check_type is None:
            error(node.lineno, "Using unrecognized type {}".format(valtype))
        if check_type==StringType and len(node.value)==1 :
            check_type = CharType
        node.check_type = check_type



def check_program(node):
    checker = CheckProgramVisitor()
    checker.visit(node)

if __name__ == '__main__':
    import lexer
    import anuragparser
    import sys
    from errors import subscribe_errors
    pars = anuragparser.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = pars.parse(open(sys.argv[1]).read())
        check_program(program)
            
