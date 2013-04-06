from loo import IntType, FloatType, StringType, BoolType, CharType, ArrayType, AccessType, EnumType, RecordType, ExprType
import ast
import exprblock

class GenerateCode(ast.NodeVisitor):
    '''
    Node visitor class that creates 3-address encoded instruction sequences.
    '''
    program = ''
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
        node.code='.data\n'
        for args in node.parameters.parameters:
            self.visit(args)
            node.code+=args.code
        for vardecl in node.decl_part:
            self.visit(vardecl)
            node.code+=vardecl.code
        node.code+='.text\n'
        self.visit(node.statements)
        node.code+=node.statements.code

    def visit_VarDeclaration(self,node):
        node.code = node.name+': '
        if node.typename.check_type.typename=='integer':
            node.code+=' .word 1\n'
        elif node.typename.check_type.typename=='character':
            node.code+=' .byte 1\n'
        elif node.typename.check_type.typename=='string':
            node.code+=' .asciiz\n'

    def visit_FuncParameter(self,node):
        node.code = node.name+': '
        if node.typename.check_type.typename=='integer':
            node.code+=' .word 1\n'
        elif node.typename.check_type.typename=='character':
            node.code+=' .byte 1\n'
        elif node.typename.check_type.typename=='string':
            node.code+=' .asciiz\n'

    def visit_Literal(self,node):
        inst = 'li $a0 '+str(node.value)+'\n'
        node.code=inst

    def visit_Unaryop(self,node):
        self.visit(node.expr)
        instruction = node.check_type.unary_opcodes[node.op] 
        inst = instruction+'$a0 $a0\n'
        node.code=inst

    def visit_LoadLocation(self, node):
        inst = 'lw $a0 '+node.location.name+'\n'
        node.code = inst
        # Save the name of the temporary variable where the value was placed 

    def visit_Binop(self, node):
        self.visit(node.left)
        node.code = node.left.code
        node.code+='sw $a0 0($sp)\naddiu $sp $sp -4\n'
        self.visit(node.right)
        node.code+=node.right.code
        node.code+='lw $t1 4($sp)\n'
        instruction = node.check_type.binary_opcodes[node.op]
        inst = instruction+' $a0 $t1 $a0\naddiu $sp $sp 4\n'
        node.code+=inst

    def visit_Relop(self, node):
        self.visit(node.left)
        node.code=node.left.code
        node.code+='sw $a0 0($sp)\naddiu $sp $sp -4\n'
        self.visit(node.right)
        node.code+=node.right.code
        node.code+='lw $t1 4($sp)\n'
        instruction = node.left.check_type.rel_opcodes[node.op]
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
        inst = "sw $a0 "+node.location.name+'\n'
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
        node.code+='lw $ra 4($sp)\naddiu $sp $sp 4\nlw $fp 0($sp)\njr $ra\n'

    def visit_GotoStatement(self,node):
        node.code='b '+node.name.location.name+'\n'

    def visit_ProcCall(self,node):
        node.code='sw $fp 0($sp)\naddiu $sp $sp -4\njal '+node.name.location.name+'\n'

    def visit_FuncCall(self,node):
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
        check.check_program(program)
        # If no errors occurred, generate code
        if not errors_reported():
            code = generate_code(program)
            print code
            # Emit the code sequence
            JumpGenerator().visit(code)
            #for inst in code:
            #    print(inst)
