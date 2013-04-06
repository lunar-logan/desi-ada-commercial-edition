# exprpygen.py
'''
Project 4 (part 2):
===================
This part of the project requires a working version of exprcode.py. Go 
work on that first.

Emit three-address code as a single Python function.   In this file, you must
write code that emits 3-address intermediate code as runnable Python code.
To do this, have your program create a Python function like this:

     def main(frame=None):
          if frame is None:
              frame = {}
          # Instructions follow
          ...

For each instruction such as:

        ('add', 'int_1','int_2','int_3')

generate Python code like this:

        int_3 = int_1 + int_2

For load and store operations involving variables, use the frame dictionary
for storage. For example, the instructions:

        ('load','varname','target')
        ('store','source','varname')

Should become:

        target = frame['varname']
        frame['varname'] = source
'''

# STEP 1:  The file codegen.py has a generator base class useful for writing code emitters
# Go look at the source, the come back here.
#

from codegen import CodeEmitter
import exprblock

# STEP 2: Implement the code emitter
#
# Fill in the methods of this class to emit output code.  You will mostly be
# writing a bunch of a one-line methods.

class ExprPyCodeEmitter(CodeEmitter):
    '''
    Emit runnable Python code from 3-address intermediate code.  The make_code()
    method is the entry point.  You must implement a collection of methods of
    the form emit_opcode().
    '''

    # You must implement methods of the form emit_opcode for all of the
    # opcodes used in the 3-address intermediate code.  One example follows:
    def emit_loadi(self,value,target):
         '''
         Load an immediate (literal) value
         '''
         # Sample.  Return a string representing a line of output source code
         return "%s = %r" % (target, value)

    def emit_load(self,name,target):
         '''
         Load the value of a variable
         '''
         return "%s = frame[%r]" % (target, name)

    def emit_newvar_local(self,source,name):
         '''
         Create a new variable
         '''
         return "frame[%r] = %s" % (name, source)

    def emit_store_local(self,source,name):
         '''
         Store a value into a variable
         '''
         return "frame[%r] = %s" % (name, source)

    def emit_add(self,left,right,target):
         '''
         target = left + right
         '''
         return "%s = %s + %s" % (target, left, right)

    def emit_sub(self,left,right,target):
         '''
         target = left - right
         '''
         return "%s = %s - %s" % (target, left, right)

    def emit_mul(self,left,right,target):
         '''
         target = left * right
         '''
         return "%s = %s * %s" % (target, left, right)

    emit_imul = emit_mul
    emit_fmul = emit_mul

    def emit_gt(self,left,right,target):
         '''
         target = left > right
         '''
         return "%s = %s > %s" % (target, left, right)

    def emit_gte(self,left,right,target):
         '''
         target = left >= right
         '''
         return "%s = %s >= %s" % (target, left, right)

    def emit_lt(self,left,right,target):
         '''
         target = left < right
         '''
         return "%s = %s < %s" % (target, left, right)

    def emit_lte(self,left,right,target):
         '''
         target = left <= right
         '''
         return "%s = %s <= %s" % (target, left, right)

    def emit_eq(self,left,right,target):
         '''
         target = left == right
         '''
         return "%s = %s == %s" % (target, left, right)

    def emit_neq(self,left,right,target):
         '''
         target = left != right
         '''
         return "%s = %s != %s" % (target, left, right)

    def emit_land(self,left,right,target):
         '''
         target = left && right
         '''
         return "%s = %s and %s" % (target, left, right)

    def emit_lor(self,left,right,target):
         '''
         target = left || right
         '''
         return "%s = %s or %s" % (target, left, right)

    def emit_idiv(self,left,right,target):
         '''
         target = left / right     (with integer truncation)
         '''
         return "%s = %s // %s" % (target, left, right)

    def emit_fdiv(self,left,right,target):
         '''
         target = left / right     (floating point)
         '''
         return "%s = %s / %s" % (target, left, right)

    def emit_uadd(self,source,target):
         '''
         target = +source
         '''
         return "%s = +%s" % (target, source)

    def emit_uneg(self,source,target):
         '''
         target = -source
         '''
         return "%s = -%s" % (target, source)

    def emit_not(self,source,target):
         '''
         target = !source
         '''
         return "%s = not %s" % (target, source)

    def emit_print(self,source):
         '''
         print source
         '''
         return "print(%s)" % (source)

class BlockCodeEmitter(exprblock.BlockVisitor):
    def __init__(self):
        self.emitter = ExprPyCodeEmitter()
        self.lines = lines = []
        self.level = 0
        self.emit("def main(frame=None):")
        self.indent()
        self.emit("if frame is None: frame = {}")

    def get_code(self):
        return "\n".join(self.lines)

    def prnt(self):
        print(self.get_code())

    def calctab(self):
        self.tab = self.level * 4 * " "

    def indent(self):
        self.level += 1

    def dedent(self):
        self.level -= 1

    def emit(self, line):
        self.calctab()
        self.lines.append("%s%s" % (self.tab, line))

    def visit_BasicBlock(self,block):
        for line in self.emitter.process(block.instructions):
            self.emit(line)

    def visit_IfBlock(self,block):
        # Emit an if statement
        self.visit_BasicBlock(block)
        # Emit a jump around the else-branch (if there is one)
        self.emit("if %s:" % block.condvar)
        self.indent()
        self.visit(block.truebranch)
        if block.falsebranch:
            self.dedent()
            self.emit("else:")
            self.indent()
            self.visit(block.falsebranch)
        self.dedent()

    def visit_WhileBlock(self,block):
        # Emit a conditional jump around the if-branch
        self.emit("while 1:")
        self.indent()
        self.visit_BasicBlock(block)
        self.emit("if not %s: break" % block.condvar)
        self.visit(block.truebranch)
        self.dedent()
        # Emit a jump around the else-branch (if there is one)



# STEP 3: Testing
#
# Try running this program on the input file good.e
#
#    bash % python exprpygen.py good.e > a.py
#    bash % python a.py
#    ... verify correct output ...
#

# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------

def emit_pycode(imcode):
    emitter = BlockCodeEmitter()
    emitter.visit(code)
    emitter.prnt()

if __name__ == '__main__':
    import exprlex
    import exprparse
    import exprcheck
    import exprcode

    import sys
    from errors import subscribe_errors, errors_reported
    lexer = exprlex.make_lexer()
    parser = exprparse.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        # Check the program
        exprcheck.check_program(program)
        # If no errors occurred, generate code
        if not errors_reported():
            code = exprcode.generate_code(program)
            emit_pycode(code)
            print("if __name__ == '__main__':")
            print("     main()")

