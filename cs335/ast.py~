class AST(object):
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


class Compilation(AST):
    _fields = ['program']

    def append(self,stmt):
        self.program.append(stmt)

    def __len__(self):
        return len(self.program)


class Literal(AST):
    _fields = ['value']          

class Typename(AST):
    _fields = ['name']          

class Location(AST):
    _fields = ['name']          

class LoadLocation(AST):
    _fields = ['location']          

class Unaryop(AST):
    _fields = ['op','expr']           

class Binop(AST):
    _fields = ['op','left','right']          
    
class Relop(AST):
    _fields = ['op','left','right']          
    
class AssignmentStatement(AST):
    _fields = ['location','expr']          

class ArrayAssignmentStatement(AST):
    _fields = ['location','args','expr']          

class PrintStatement(AST):
    _fields = ['expr']          
    
class Statements(AST):
    _fields = ['statements']          

    def append(self,stmt):
        self.statements.append(stmt)

    def __len__(self):
        return len(self.statements)


class Goal_symbol(AST):
    _fields = ['compilation']          

class VarDeclaration(AST):
    _fields = ['name','typename','expr','length']          
  
class TypeDeclaration(AST):
     _fields = ['name', 'expr', 'type_completion']   

class Integer_type(AST):
    _fields = ['range_spec', 'expression']

class Float_type(AST):
    _fields = ['expression', 'range_spec_opt']

class Fixed_type(AST):
    _fields = ['expression_1', 'range_spec_opt', 'expression_2']

class Access_type_subtype(AST):
    _fields = ['modifier', 'subtype_ind']

class Access_type_subprog(AST):
    _fields = ['prot_opt', 'formal_part_opt', 'mark']
     
class Unconstr_array(AST):
    _fields = ['index_s','aliased','subtype_ind']
    
class Constr_array(AST):
    _fields = ['index_constraint','aliased','subtype_ind']

class Record(AST):
    _fields = ['tagged',' limited','record_def']

class Enum(AST):
    _fields = ['enum_id']
    
    def append(self,stmt):
        self.enum_id.append(stmt)

    def __len__(self):
        return len(self.enum_id) 

class ComponentDeclaration(AST):
    _fields = ['comp_decls']

    def append(self,comp_decl):
        self.comp_decls = self.comp_decls + comp_decl

    def __len__(self):
        return len(self.comp_decls)

 
class Index_s(AST):
    _fields = ['index_s']
    
    def append(self,stmt):
        self.index_s.append(stmt)

    def __len__(self):
        return len(self.index_s)

class IfStatement(AST):
    _fields = ['expr', 'truebranch', 'falsebranch']

class CaseStatement(AST):
    _fields = ['condition','alternatives']

class Alternatives(AST):
    _fields = ['alternatives']

    def append(self,alternate):
        self.alternatives.append(alternate)

    def __len__(self):
        return len(self.alternatives)

class Alternative(AST):
    _fields = ['choices','statements']

class Choices(AST):
    _fields = ['choices']

    def append(self,choice):
        self.choices.append(choice)
    
    def __len__(self):
        return len(self.choices)

class WhileStatement(AST):
    _fields = ['label','expr', 'truebranch','id']

class LoopStatement(AST):
    _fields = ['condition','truebranch']

class For_loop(AST):
    _fields = ['name','reverse','discrete_range']

class Doubledot_range(AST):
    _fields = ['left','right']

class Name_tick(AST):
    _fields = ['name','expression']

class Block(AST):
    _fields = ['label','decl','block','id']

class FuncStatement(AST):
    _fields = ['name', 'returntype', 'parameters','decl_part','statements','id']

class FuncParameterList(AST):
    _fields = ['parameters']

    def append(self,stmt):
        self.parameters = self.parameters + stmt

    def __len__(self):
        return len(self.parameters)

class FuncParameter(VarDeclaration):
    pass

class TypeDeclaration(VarDeclaration):
    pass

class SubTypeDeclaration(VarDeclaration):
    pass

class FuncCall(AST):
    _fields = ['name','arguments']

class ProcCall(AST):
    _fields = ['name']

class Value_s(AST):
    _fields = ['arguments']

    def append(self,stmt):
        self.arguments.append(stmt)

    def __len__(self):
        return len(self.arguments)

class ReturnStatement(AST):
    _fields = ['expr']

class ExitStatement(AST):
    _fields = ['name','expr']

class GotoStatement(AST):
    _fields = ['name']


class NodeVisitor(object):
    def visit(self,node):
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None
    
    def generic_visit(self,node):
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)
def flatten(top):
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
