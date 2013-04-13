from loo import IntType, FloatType, StringType, BoolType, CharType, ArrayType, AccessType, EnumType, RecordType, ExprType
import ast
import exprblock
counter = 0
endcounter = 0
env = None
class ActivationRecord:
    def __init__(self):
        self.rec =[]
        self.type = {}
        self.size = {'Int': 4, 'Float':8}
    def store(self, Name, Type):
        self.rec += [Name]
        self.type[Name] = Type
    def index(self, name):
        for i in xrange(len(self.rec)):
            if self.rec[i] == name: return i
        return -1
    def length(self):
        return len(self.rec)

    def get(self, Name):
        count = 0
        for i in xrange(len(self.rec)):
            if self.rec[i] != Name:
                count += self.size[self.type[self.rec[i]]]
        return count
    

class Stack:
    def __init__(self):
        self.env = []
        #self.activationRecord = ActivationRecord()
    def push(self, x):
        self.env += [x]   
    def pop(self):
        if len(self.env) == 0:
            raise RuntimeError()
        val = self.env[-1]
        self.env = self.env[0:-1]
        return val
    def peek(self):
        return self.env[-1]


                
activationStack = Stack()
class GenerateCode(ast.NodeVisitor):
    '''
    Node visitor class that creates 3-address encoded instruction sequences.
    '''
    program = ''
    #activationStack = Stack()
    def new_temp(self,type):
        name = "%s_%d" % (type.typename,self.temp_count)
        self.temp_count += 1
        return name

    def visit_Goal_symbol(self,node):
        # Reset the sequence of instructions and temporary count
        self.code=''
        self.program = self.code
        self.temp_count = 0
        # Visit all of the statements in the program
        self.visit(node.compilation)
        self.code=node.compilation.code+'li $v0 10\nsyscall\n'
        program = self.code
    # You must implement visit_Nodename methods for all of the other
    # AST nodes.  In your code, you will need to make instructions
    # and append them to the self.code list.
    #
    # One sample method follows

    def visit_Compilation(self,node):
        #print node.program
        node.code=''
        for progra in node.program :
            #if isinstance(progra,FuncStatement):
            self.visit(progra)
            node.code+=progra.code

    def visit_FuncStatement(self,node):
        node.code ='.text\n'
        if sys.argv[1][0:sys.argv[1].index(".adb")]==node.name:
            node.code+='.globl main\nmain:\n'
        node.code+=node.name+':\n'
        #node.code='.data\n'
        ar = ActivationRecord()
        if node.parameters is not None:
            for args in node.parameters.parameters:
                #self.visit(args)
                #node.code+=args.code
                ar.store(args.name, args.typename.name)
            z=len(node.parameters.parameters)
        else :
            z=0
        for vardecl in node.decl_part:
            #self.visit(vardecl)
            #node.code+=vardecl.code
            ar.store(vardecl.name, vardecl.typename.name)
            node.code += 'addiu $sp $sp -4\n'
        z+=len(node.decl_part)
        activationStack.push(ar)
        
        
        node.code+='move $fp $sp\nsw $ra 0($sp)\naddiu $sp $sp -4\n'
        self.visit(node.statements)
        node.code+=node.statements.code
        node.code+='lw $ra 4($sp)\naddiu $sp $sp '+str(4*z+8)+'\n'
        node.code+='lw $fp 0($sp)\njr $ra\n'
        activationStack.pop()

    def visit_VarDeclaration(self,node):
        node.code = node.name+': '
        checktype=node.typename.check_type.typename
        if checktype=='integer':
            node.code+=' .word 1\n'
        elif checktype=='character':
            node.code+=' .byte 1\n'
        elif checktype=='string':
            node.code+=' .asciiz ""\n'
        elif checktype=='float':
            node.code+=' .float 0.0\n'

    def visit_FuncParameter(self,node):
        node.code = node.name+': '
        checktype=node.typename.check_type.typename
        if checktype=='integer':
            node.code+=' .word 1\n'
        elif checktype=='character':
            node.code+=' .byte 1\n'
        elif checktype=='string':
            node.code+=' .asciiz ""\n'
        elif checktype=='float':
            node.code+=' .float 0.0\n'

    def visit_Literal(self,node):
        if node.check_type.typename=='float':
            inst = 'li.s $f0 '+str(node.value)+'\n'
        else: 
            inst = 'li $a0 '+str(node.value)+'\n'
        node.code=inst

    def visit_Unaryop(self,node):
        checktype=node.check_type.typename
        self.visit(node.expr)
        instruction = node.check_type.unary_opcodes[node.op]
        if checktype=='float':
            inst = instruction+'$f0 $f0\n'
        else:
            inst = instruction+'$a0 $a0\n'
        node.code=inst

    def visit_LoadLocation(self, node):
        if hasattr(node,'check_type'): checktype=node.check_type.typename
        #inst = None
        #if checktype=='float':
        #    inst = 'l.s $f0 '+node.location.name+'\n'
        #elif  checktype=='string':
        #    inst = 'la $a0 '+node.location.name+'\n'
        #else :
        inst = 'lw $a0 '+str(4 * (activationStack.peek().length() - activationStack.peek().index(node.location.name)))+'($fp)\n'
        node.code = inst
        # Save the name of the temporary variable where the value was placed 

    def visit_Binop(self, node):
        self.visit(node.left)
        node.code = node.left.code
        checktype=node.check_type.typename
        if checktype=='float':
            node.code+='s.s $f0 0($sp)\naddiu $sp $sp -4\n'
        else :
            node.code+='sw $a0 0($sp)\naddiu $sp $sp -4\n'
        self.visit(node.right)
        node.code+=node.right.code
        if checktype=='float':
            node.code+='l.s $f1 4($sp)\n'
        else :
            node.code+='lw $t1 4($sp)\n'
        instruction = node.check_type.binary_opcodes[node.op]
        if checktype=='float':
            inst = instruction+' $f0 $f1 $f0\naddiu $sp $sp 4\n'
        else :
            inst = instruction+' $a0 $t1 $a0\naddiu $sp $sp 4\n'
        node.code+=inst

    def visit_Relop(self, node):
        self.visit(node.left)
        node.code=node.left.code
        checktype=node.check_type.typename
        if checktype=='float':
            node.code+='s.s $f0 0($sp)\naddiu $sp $sp -4\n'
        else:
            node.code+='sw $a0 0($sp)\naddiu $sp $sp -4\n'
        self.visit(node.right)
        node.code+=node.right.code
        if checktype=='float':
            node.code+='l.s $f1 4($sp)\n'
        else:
            node.code+='lw $t1 4($sp)\n'
        instruction = node.left.check_type.rel_opcodes[node.op]
        if checktype=='float':
            inst = instruction+' $f0 $f1 $a0\naddiu $sp $sp 4\n'
        else:
            inst = instruction+' $a0 $t1 $a0\naddiu $sp $sp 4\n'
        node.code+=inst


    def visit_ConstDeclaration(self, node):
        self.visit(node.expr)
        if node.scope_level == 0:
            opcode = "newvar_global"
        else:
            opcode = "newvar_local"
        inst = (opcode, node.expr.gen_location, node.name)
        node.code=inst

    def visit_Statements(self,node):
        node.code=''
        for statement in node.statements:
            self.visit(statement)
            node.code+=statement.code

    def visit_AssignmentStatement(self, node):
        self.visit(node.expr)
        node.code=node.expr.code
        if node.expr.check_type.typename=='float':
            inst = "s.s $a0 "+node.location.name+'\n'
        elif node.expr.check_type.typename=='integer':

            inst = "sw $a0 "+str(4 * (activationStack.peek().length() - activationStack.peek().index(node.location.name)))+'($fp)\n'
        node.code+=inst

    def visit_ExitStatement(self, node):
        node.code=''
        if node.expr != None :
            self.visit(node.expr)
            node.code+=node.expr.code
            if node.name != None :
                node.code+='beq $a0 1 '
            else :
                node.code+='beq $a0 1 '
        else :
            node.code+='b '
        if node.name.location.name != None :
            node.code+=node.name.location.name+'\n'
        else :
            node.code+='el\n'

    def visit_ReturnStatement(self,node):
        node.code=''
        if (node.expr != None):
            self.visit(node.expr)
            node.code+=node.expr.code
        node.code+='lw $ra 4($sp)\naddiu $sp $sp 12\nlw $fp 0($sp)\njr $ra\n'

    def visit_GotoStatement(self,node):
        node.code='b '+node.name.location.name+'\n'

    def visit_ProcCall(self,node):
        node.code='sw $fp 0($sp)\naddiu $sp $sp -4\njal '+node.name.location.name+'\n'

    def visit_FuncCall(self,node):
        if node.name == 'put':
            checktype = node.arguments.arguments[0].check_type.typename
            self.visit(node.arguments.arguments[0])
            node.code=node.arguments.arguments[0].code
            if checktype=='integer':
                node.code+='li $v0 1\n'
            elif checktype=='character':
                node.code+='li $v0 11\n'
            elif checktype=='string':
                node.code+='li $v0 4\n'
            elif checktype=='float':
                node.code+='li $v0 2'
            node.code += 'syscall\n'
        else:
            node.code='sw $fp 0($sp)\naddiu $sp $sp -4\n'
            for argument in node.arguments.arguments:
                self.visit(argument)
                node.code+=argument.code
                node.code+='sw $a0 0($sp)\naddiu $sp $sp -4\n'
            node.code+='jal '+node.name+'\n'

    def visit_PrintStatement(self, node):
        self.visit(node.expr)
        inst = ("print", node.expr.gen_location)
        node.code=inst

    def visit_IfStatement(self, node):
        #print("visiting %r" % node)
        global counter
        global endcounter
        self.visit(node.expr)
        node.code=node.expr.code
        counter+=1
        tempcounter = counter
        node.code+='beq $a0 0 l'+str(tempcounter)+'\n'
        self.visit(node.truebranch)
        node.code+=node.truebranch.code
        counter+=1
        tempcounter2=counter
        node.code+='j l'+str(tempcounter2)+'\n'
        node.code+='l'+str(tempcounter)+':\n'
        if node.falsebranch is not None:
            self.visit(node.falsebranch)
            node.code+=node.falsebranch.code
        node.code+='l'+str(tempcounter2)+':\n'

    def visit_CaseStatement(self,node):
        global counter
        global endcounter
        self.visit(node.condition)
        node.code=node.condition.code
        node.code+='sw $a0 0($sp)\naddiu $sp $sp -4\n'
        counter+=1
        tempcounter=counter
        if node.alternatives.alternatives is not None:
            for alternative in node.alternatives.alternatives :
                self.visit(alternative)
                node.code+=alternative.code
                node.code+='j l'+str(tempcounter)+'\n'
        node.code+='el'+str(endcounter)+':\nl'+str(tempcounter)+':\n'
        endcounter+=1
        node.code+='addiu $sp $sp 4\n'

    def visit_Alternative(self,node):
        global counter
        global endcounter
        node.code='el'+str(endcounter)+':\n'
        endcounter+=1
        counter+=1
        tempcounter=counter
        for choice in node.choices.choices:
            if choice=='others':
                node.code+='j l'+str(tempcounter)+'\n'
            else:
                self.visit(choice)
                node.code+=choice.code
                node.code+='lw $t1 4($sp)\nbeq $a0 $t1 l'+str(tempcounter)+'\n'
        node.code+='j el'+str(endcounter)+'\nl'+str(tempcounter)+':\n'
        self.visit(node.statements)
        node.code+=node.statements.code

# STEP 3: Testing
# 
# Try running this program on the input file good.e and viewing
# the resulting 3-address code sequence.
#
#     bash % python exprcode.py good.e
#     ... look at the output ...
#

# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------
def generate_code(node):
    '''
    Generate three-address code from the supplied AST node.
    '''
    gen = GenerateCode()
    gen.visit(node)
    return gen.code

class JumpGenerator(exprblock.BlockVisitor):
    def visit_BasicBlock(self,block):
        print("Block:[%s]" % block)
        for inst in block.instructions:
            print("    %s" % (inst,))
        print("")

    def visit_IfBlock(self,block):
        # Emit a conditional jump around the if-branch
        #inst = ('if', block.condvar)
        #block+=inst)
        self.visit_BasicBlock(block)
        if block.falsebranch:
            pass
            # Emit a jump around the else-branch (if there is one)
            #inst = ('else',)
            #block.truebranch+=inst)
        self.visit(block.truebranch)
        if block.falsebranch:
            self.visit(block.falsebranch)

    def visit_WhileBlock(self,block):
        # Emit a conditional jump around the if-branch
        #inst = ('while', block.condvar)
        #block+=inst)
        self.visit_BasicBlock(block)
        self.visit(block.truebranch)


if __name__ == '__main__':
    import lexer
    import parser 
    import check
    import sys
    from errors import subscribe_errors, errors_reported
    lexer = lexer.make_lexer()
    parser = parser.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        # Check the program
        env = check.check_program(program)
        # If no errors occurred, generate code
        if not errors_reported():
            code = generate_code(program)
            print code
            # Emit the code sequence
            JumpGenerator().visit(code)
            #for inst in code:
            #    print(inst)
